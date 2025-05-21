from flask import Flask, request, jsonify
from flask_cors import CORS # For handling Cross-Origin Resource Sharing
import joblib
import pandas as pd
import numpy as np
import os # For path joining, good practice

app = Flask(__name__)
CORS(app) # This will allow requests from your frontend (running on a different port)

# --- Global variables to hold the loaded model, preprocessor, and columns ---
model = None
preprocessor = None
training_columns = None # This is crucial!

# Determine the directory of the current script to load artifacts reliably
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'pcos_model.joblib')
PREPROCESSOR_PATH = os.path.join(BASE_DIR, 'pcos_preprocessor.joblib')
TRAINING_COLS_PATH = os.path.join(BASE_DIR, 'training_columns.joblib')


def load_artifacts():
    """Load the trained model, preprocessor, and training columns."""
    global model, preprocessor, training_columns
    try:
        model = joblib.load(MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        training_columns = joblib.load(TRAINING_COLS_PATH) # Load the expected columns
        
        if not isinstance(training_columns, list):
            print(f"Error: 'training_columns.joblib' did not load a Python list. Loaded type: {type(training_columns)}")
            exit()
            
        print("Model, preprocessor, and training columns loaded successfully.")
        print(f"Number of training columns expected: {len(training_columns)}")
        # print(f"Expected training columns: {training_columns}") # Uncomment for debugging
        
    except FileNotFoundError as e:
        print(f"Error loading artifacts: {e}. Make sure .joblib files are in the correct path: {BASE_DIR}")
        exit() # Exit if artifacts can't be loaded
    except Exception as e:
        print(f"An unexpected error occurred while loading artifacts: {e}")
        exit()

@app.route('/predict_pcos', methods=['POST'])
def predict_pcos_endpoint():
    global model, preprocessor, training_columns

    if model is None or preprocessor is None or training_columns is None:
        return jsonify({'error': 'Model, preprocessor, or training columns not loaded. Check server logs.'}), 500

    try:
        frontend_data = request.get_json()
        if not frontend_data:
            return jsonify({'error': 'No input data provided'}), 400

        print(f"Received frontend data: {frontend_data}") # Log received data

        # --- Prepare the input data for the preprocessor ---
        # The input DataFrame MUST have the same columns in the same order
        # as the DataFrame used to FIT the preprocessor.

        # Create a dictionary for the input row, ensuring all training columns are present
        # and mapping frontend keys to the model's expected feature names.
        input_values_for_df = {}
        
        # --- !!! IMPORTANT MAPPING SECTION !!! ---
        # Map keys from your frontend form to the actual column names in training_columns.joblib
        # This is where you translate what the user types into what your model understands.
        # Example: if frontend sends "age" but model expects "Age (yrs)"
        
        # Example frontend_data keys (you'll get these from your HTML form names):
        # "age", "cycle_regularity", "weight_gain", "hair_growth", "skin_darkening",
        # "hair_loss", "pimples", "fast_food", "cycle_length_days", "height_cm", "weight_kg", "blood_group_code"
        
        # This loop ensures we construct the DataFrame row with all expected columns
        for model_col_name in training_columns:
            value_from_frontend = None
            
            # --- Start of explicit mapping based on assumed frontend keys ---
            if model_col_name == 'Age (yrs)':
                value_from_frontend = frontend_data.get('age') # Assuming frontend sends 'age'
                if value_from_frontend is not None:
                    try: value_from_frontend = float(value_from_frontend)
                    except ValueError: value_from_frontend = np.nan
            elif model_col_name == 'Cycle(R/I)':
                value_from_frontend = frontend_data.get('cycle_regularity') # e.g., "Irregular", "Regular"
            elif model_col_name == 'Weight gain(Y/N)':
                value_from_frontend = frontend_data.get('weight_gain') # e.g., "Yes", "No"
            elif model_col_name == 'hair growth(Y/N)':
                value_from_frontend = frontend_data.get('hair_growth')
            elif model_col_name == 'Skin darkening (Y/N)':
                value_from_frontend = frontend_data.get('skin_darkening')
            elif model_col_name == 'Hair loss(Y/N)':
                 value_from_frontend = frontend_data.get('hair_loss')
            elif model_col_name == 'Pimples(Y/N)':
                 value_from_frontend = frontend_data.get('pimples')
            elif model_col_name == 'Fast food (Y/N)':
                 value_from_frontend = frontend_data.get('fast_food')
            elif model_col_name == 'Cycle length(days)':
                value_from_frontend = frontend_data.get('cycle_length_days')
                if value_from_frontend is not None:
                    try: value_from_frontend = float(value_from_frontend)
                    except ValueError: value_from_frontend = np.nan
            elif model_col_name == 'Height(Cm)': # Example: if your model used Height and Weight separately
                value_from_frontend = frontend_data.get('height_cm')
                if value_from_frontend is not None:
                    try: value_from_frontend = float(value_from_frontend)
                    except ValueError: value_from_frontend = np.nan
            elif model_col_name == 'Weight (Kg)':
                value_from_frontend = frontend_data.get('weight_kg')
                if value_from_frontend is not None:
                    try: value_from_frontend = float(value_from_frontend)
                    except ValueError: value_from_frontend = np.nan
            elif model_col_name == 'Blood Group': # Assuming Blood Group in training_columns is the one that was one-hot encoded
                value_from_frontend = frontend_data.get('blood_group_code') # e.g., "11", "15" sent as string
                                                                          # Your OneHotEncoder should handle string categories
            # Add elif for ALL other columns in your training_columns.joblib
            # ...
            # Example for a feature that might not come from the form directly:
            # elif model_col_name == 'BMI':
            #    # BMI might be calculated from height and weight if not directly input
            #    h = frontend_data.get('height_cm')
            #    w = frontend_data.get('weight_kg')
            #    if h and w:
            #        try:
            #            h_m = float(h) / 100
            #            value_from_frontend = float(w) / (h_m * h_m)
            #        except (ValueError, TypeError, ZeroDivisionError):
            #            value_from_frontend = np.nan
            #    else:
            #        value_from_frontend = np.nan # Or if BMI is a direct input, map it
            else:
                # Default: try to get it directly if no specific mapping (less safe)
                # This assumes frontend key might directly match model_col_name
                value_from_frontend = frontend_data.get(model_col_name)
            # --- End of explicit mapping ---

            input_values_for_df[model_col_name] = [value_from_frontend if value_from_frontend is not None else np.nan]

        # Create a single-row DataFrame
        # The order of columns in input_df MUST match `training_columns`
        try:
            input_df = pd.DataFrame.from_dict(input_values_for_df)
            # Reorder columns to strictly match training_columns order, just in case from_dict changes it
            input_df = input_df[training_columns]
        except Exception as e:
            print(f"Error creating DataFrame from input: {e}")
            print(f"Input data dictionary constructed: {input_values_for_df}")
            return jsonify({'error': f'Error preparing input for model: {e}'}), 400

        print(f"DataFrame for preprocessing (first 5 cols):\n{input_df.iloc[:, :5].to_string()}")
        # print(f"DataFrame dtypes:\n{input_df.dtypes}") # Uncomment for detailed dtype debugging

        # --- Preprocess the input data ---
        processed_input = preprocessor.transform(input_df)
        print(f"Shape of processed input: {processed_input.shape}")

        # --- Make prediction ---
        prediction = model.predict(processed_input)[0]  # Get the single prediction
        prediction_proba = model.predict_proba(processed_input)[0] # Probabilities for [class_0, class_1]

        # --- Format response ---
        pcos_status = "Likely PCOS" if prediction == 1 else "Unlikely PCOS"
        confidence = float(prediction_proba[1]) # Probability of class 1 (PCOS)

        response = {
            'pcos_status': pcos_status,
            'confidence': round(confidence, 3) # Round to 3 decimal places
        }
        print(f"Prediction response: {response}")
        return jsonify(response)

    except KeyError as e:
        print(f"KeyError: Missing expected key in input data from frontend: {e}")
        return jsonify({'error': f'Missing symptom data: {e}. Please ensure all required fields are provided as expected by the backend.'}), 400
    except ValueError as e:
        print(f"ValueError during prediction or data conversion: {e}")
        return jsonify({'error': f'Invalid data format for a symptom: {e}'}), 400
    except Exception as e:
        print(f"An unexpected error occurred during prediction: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for debugging
        return jsonify({'error': f'An internal server error occurred.'}), 500 # Don't expose detailed error to client

if __name__ == '__main__':
    load_artifacts() # Load model and preprocessor when the app starts
    app.run(debug=True, port=5000) # Run on port 5000
