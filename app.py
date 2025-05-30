from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Load trained model and scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Extract and convert form data
            features = [
                int(request.form.get("HighBP", 0)),   
                int(request.form.get("HighChol", 0)),  
                int(request.form.get("CholCheck", 0)),  
                float(request.form.get("BMI", 0)),   
                int(request.form.get("Smoker", 0)),  
                int(request.form.get("Stroke", 0)),  
                int(request.form.get("Diabetes", 0)),  
                int(request.form.get("PhysActivity", 0)),  
                int(request.form.get("Fruits", 0)),  
                int(request.form.get("Veggies", 0)),  
                int(request.form.get("HvyAlcoholConsump", 0)),  
                int(request.form.get("AnyHealthcare", 0)),  
                int(request.form.get("NoDocbcCost", 0)),  
                int(request.form.get("GenHlth", 0)),  
                int(request.form.get("MentHlth", 0)),  
                int(request.form.get("PhysHlth", 0)),  
                int(request.form.get("DiffWalk", 0)),  
                int(request.form.get("Sex", 0)),  
                int(request.form.get("Age", 0)),  
                int(request.form.get("Education", 0)),  
                int(request.form.get("Income", 0)),  
            ]

            # Convert to NumPy array and scale
            features = np.array([features])
            features_scaled = scaler.transform(features)

            # Make prediction
            prediction = model.predict(features_scaled)[0]
            result = "Likely to have heart disease Please consult your doctor" if prediction == 1 else "Unlikely to have heart disease"

            # Check if request is AJAX
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"result": result})  # ✅ Return JSON for AJAX

            return render_template("user_interface2.html", result=result)  # Normal render

        except Exception as e:
            error_message = f"Error: {str(e)}"
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"result": error_message})  # Return JSON for AJAX errors
            
            return render_template("user_interface2.html", result=error_message)

    return render_template("user_interface2.html", result="")

if __name__ == "__main__":
    app.run(debug=True)




# python app.py
# To run the Flask app, use the command:




