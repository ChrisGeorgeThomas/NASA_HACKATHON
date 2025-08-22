from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")  # make sure index.html is in 'templates' folder

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Parse incoming JSON
        data = request.get_json()
        print("\n--- Incoming Data ---")
        print(data)

        # Build supplies list if available
        initial_supplies = data.get("initialSuppliesKg", {})
        supplies_list = "\n".join(
            [f"- {item}: {amount} kg" for item, amount in initial_supplies.items()]
        ) if isinstance(initial_supplies, dict) else "No supplies provided"

        # Build the prompt for Gemini
        prompt = f"""
You are analyzing a space mission's sustainability.

Mission Details:
- Duration: {data.get('missionDurationMonths', 'N/A')} months
- Crew size: {data.get('crewSize', 'N/A')}
- Habitat volume: {data.get('habitatVolumeM3', 'N/A')} m³
- Orbit: {data.get('orbit', 'N/A')}

Initial Supplies:
{supplies_list}

Task:
1. Estimate waste breakdown and recycling potential.
2. Suggest innovative recycling methods.
3. Identify long-term benefits (reduced resupply launches, resource efficiency).
4. Provide **specific numerical estimates** where possible.
        """

        print("\n--- Prompt Sent to Gemini ---")
        print(prompt)

        # Send to Gemini API
        response = model.generate_content(prompt)

        # Get text safely
        ai_text = response.text if hasattr(response, "text") else "No response from Gemini."

        print("\n--- Gemini Response ---")
        print(ai_text)

        # Send back to frontend
        return jsonify({"analysis": ai_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
