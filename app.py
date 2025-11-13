from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    Present_Price = float(request.form['Present_Price'])
    Kms_Driven = float(request.form['Kms_Driven'])
    Owner = int(request.form['Owner'])
    Year = int(request.form['Year'])

    # Dummy Variables from HTML
    Fuel_Type = request.form['Fuel_Type']
    if Fuel_Type == "Petrol":
        Fuel_Type_Petrol = 1
        Fuel_Type_Diesel = 0
    elif Fuel_Type == "Diesel":
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 1
    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 0   # CNG case

    Seller_Type = request.form['Seller_Type']
    Seller_Type_Individual = 1 if Seller_Type == "Individual" else 0

    Transmission = request.form['Transmission']
    Transmission_Manual = 1 if Transmission == "Manual" else 0

    # Arrange features
    features = np.array([[Present_Price, Kms_Driven, Owner, Year,
                          Fuel_Type_Diesel, Fuel_Type_Petrol,
                          Seller_Type_Individual, Transmission_Manual]])

    prediction = model.predict(features)[0]

    return render_template('index.html', 
                           prediction_text=f"Predicted Selling Price: ₹ {round(prediction, 2)} Lakhs")

if __name__ == "__main__":
    app.run(debug=True)
