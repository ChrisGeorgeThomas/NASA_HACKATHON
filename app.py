from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API (replace with your real API key)
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-pro")

@app.route('/')
def home():
    return open("index.html").read()   # serve your HTML

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_prompt = (
        f"Mission Name: {data['missionName']}, "
        f"Fuel Levels: {data['fuelLevels']}, "
        f"Oxygen Supply: {data['oxygenSupply']}, "
        f"Mission Status: {data['missionStatus']}. "
        f"Please provide an analysis and possible recommendations."
    )

    response = model.generate_content(user_prompt)
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
