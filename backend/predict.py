import joblib

# Load the saved model
model = joblib.load("model.pkl")

# Example input (same features as training)
sample = [[50, 2, 0, 1]]

# Make prediction
prediction = model.predict(sample)

print("Prediction:", prediction)