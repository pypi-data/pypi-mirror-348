import sys
import os
import google.generativeai as genai

def read_file_content(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def send_to_gemini(prompt):
    genai.configure(api_key="AIzaSyANWUv4peyHpdgOT2d3gVKKaIOBb3p5_kg")
    model = genai.GenerativeModel("gemini-2.0-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"API Error: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: cluster365 <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    prompt = read_file_content(file_path)
    reply = send_to_gemini(prompt)
    print("\nAI Response:\n")
    print(reply)
