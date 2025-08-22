from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Initialize Flask
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyBb-CgGMmvH2h66M_m05HpPjoAWz6oXLWQ")

@app.route('/')
def index():
    return render_template("index.html")   # this loads your frontend

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        resource_type = data.get("resource")

        if not resource_type:
            return jsonify({"error": "No input provided"}), 400

        # Call Gemini API
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Analyze the recyclability of {resource_type}. Suggest practical recycling methods and possible eco-friendly alternatives."
        response = model.generate_content(prompt)

        return jsonify({
            "analysis": response.text.strip()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
