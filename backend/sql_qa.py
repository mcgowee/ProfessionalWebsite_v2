import os
import re
import json
import sqlite3
from typing import Any, Dict, List, Tuple

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# Where your Chinook SQLite DB lives on the VPS
CHINOOK_DB_PATH = os.environ.get("CHINOOK_DB_PATH", os.path.join(os.path.dirname(__file__), "chinook.db"))

# Basic guardrails
MAX_ROWS_DEFAULT = int(os.environ.get("SQL_QA_MAX_ROWS", "50"))
MODEL_DEFAULT = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def _is_select_only(sql: str) -> bool:
    """
    Very conservative SQL safety check:
    - Must start with SELECT or WITH
    - Must not contain any write/DDL keywords
    """
    s = (sql or "").strip().strip(";").lower()

    if not (s.startswith("select") or s.startswith("with")):
        return False

    banned = [
        "insert", "update", "delete", "drop", "alter", "create", "replace",
        "truncate", "attach", "detach", "pragma", "vacuum", "reindex",
        "grant", "revoke"
    ]
    # Word boundary check
    for kw in banned:
        if re.search(rf"\b{kw}\b", s):
            return False

    return True


def _get_schema_text(conn: sqlite3.Connection) -> str:
    """
    Return a compact schema description for prompting the model.
    """
    cur = conn.cursor()
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()

    parts: List[str] = []
    for (tname,) in tables:
        cols = cur.execute(f"PRAGMA table_info({tname})").fetchall()
        # cols: cid, name, type, notnull, dflt_value, pk
        col_desc = ", ".join([f"{c[1]} {c[2]}" for c in cols])
        parts.append(f"{tname}({col_desc})")
    return "\n".join(parts)



def log_debug(msg):
    try:
        with open("/tmp/sql_debug.log", "a") as f:
            f.write(msg + "\n")
    except:
        pass

def sql_qa(question: str, session_id: str, max_rows: int = MAX_ROWS_DEFAULT) -> Dict[str, Any]:
    log_debug(f"sql_qa called with question: {question}")
    
    if not client.api_key:
        log_debug("ERROR: Missing OPENAI_API_KEY")
        return {"error": "Server is missing OPENAI_API_KEY."}


    question = (question or "").strip()
    if not question:
        return {"error": "Missing question."}

    # Read-only SQLite connection
    # uri mode + mode=ro prevents writes even if something slips through
    db_uri = f"file:{CHINOOK_DB_PATH}?mode=ro"
    conn = sqlite3.connect(db_uri, uri=True)
    conn.row_factory = sqlite3.Row

    try:
        schema_text = _get_schema_text(conn)

        system = (
            "You are a senior data analyst. You answer questions about the Chinook SQLite database.\n"
            "You MUST return valid SQLite SQL.\n"
            "Rules:\n"
            "- Return ONLY a JSON object with keys: sql, answer.\n"
            "- sql must be a single SQLite query.\n"
            "- sql must be READ-ONLY: SELECT or WITH only.\n"
            "- Prefer limiting results (LIMIT) when appropriate.\n"
        )

        user = (
            f"SCHEMA:\n{schema_text}\n\n"
            f"QUESTION:\n{question}\n\n"
            f"Return JSON only."
        )

        completion = client.chat.completions.create(
            model=MODEL_DEFAULT,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
        )

        content = completion.choices[0].message.content or ""

        # Attempt to parse JSON response
        # Model might wrap in ```json ... ``` so strip fences.
        content_stripped = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.IGNORECASE)
        try:
            payload = json.loads(content_stripped)
        except Exception as e:
            log_debug(f"JSON Parse Error: {e}, Content: {content}")
            return {"error": "Model did not return valid JSON.", "raw": content}

        sql = (payload.get("sql") or "").strip()
        answer = (payload.get("answer") or "").strip()

        if not sql:
            return {"error": "Model returned empty SQL.", "raw": content}

        if not _is_select_only(sql):
            return {"error": "Rejected unsafe SQL (must be SELECT/WITH only).", "sql": sql}

        # Enforce a LIMIT if missing and query could be large
        sql_lower = sql.lower()
        if "limit" not in sql_lower:
            sql = sql.rstrip(";") + f" LIMIT {max_rows};"

        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchmany(max_rows)
        columns = [d[0] for d in cur.description] if cur.description else []

        # Convert sqlite3.Row to regular dicts
        rows_out = [dict(r) for r in rows]

        return {
            "sql": sql,
            "columns": columns,
            "rows": rows_out,
            "answer": answer or "Done."
        }

    finally:
        conn.close()
