from app.services.gemini_client import generate_response

response = generate_response("Explain SQL in two simple sentences.")

print(response)
