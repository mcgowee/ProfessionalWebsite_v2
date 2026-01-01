from transformers import pipeline

# Load pre-trained NLP model (e.g., GPT-2 or another model)
model = pipeline("text-generation", model="gpt2")

def generate_manipulative_response(user_message):
    """
    Generate a manipulative response using NLP techniques.
    """
    prompt = f"Respond as a manipulative person using tactics like Fear, Obligation, or Guilt: {user_message}"
    response = model(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]
