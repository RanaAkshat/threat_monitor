from detoxify import Detoxify
import json

print("AI Threat & Toxicity Detector (type 'exit' to quit)\n")

while True:
    text = input("Enter a message: ")
    if text.lower() == "exit":
        break

    try:
        results = Detoxify('original').predict(text)
        print("\n--- Analysis Result ---")
        print(json.dumps(results, indent=2))
        print("------------------------\n")
    except Exception as e:
        print(f"Error: {e}")
