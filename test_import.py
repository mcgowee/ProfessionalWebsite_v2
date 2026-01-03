import sys
print("Python executable:", sys.executable)
try:
    import app
    print("Import 'app' SUCCESS")
except Exception as e:
    print(f"Import 'app' FAILED: {e}")
    import traceback
    traceback.print_exc()

print("-" * 20)

try:
    import azure.cognitiveservices.speech
    print("Import 'azure.cognitiveservices.speech' SUCCESS")
except Exception as e:
    print(f"Import 'azure.cognitiveservices.speech' FAILED: {e}")
    import traceback
    traceback.print_exc()
