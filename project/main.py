# project/main.py
import os
import joblib
import pandas as pd
import numpy as np
from flask import Blueprint, render_template, request, flash, url_for, redirect # current_app removed
from flask_login import login_required, current_user # logout_user removed
# werkzeug.security import removed as password handling is in model/auth
from . import db # For potential future use, not directly used in these routes now
from .models import User # Only User needed here for current_user context
import traceback

main = Blueprint('main', __name__)

# --- ML Artifact Loading (Keep as is) ---
ml_model = None
ml_training_columns = None
ML_ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pcos_app_files')
MODEL_PATH = os.path.join(ML_ARTIFACTS_DIR, 'pcos_logistic_model_v_test_update.joblib')
TRAINING_COLS_PATH = os.path.join(ML_ARTIFACTS_DIR, 'training_logistic_columns_v_test_update.joblib')

print(f"DEBUG main.py: Expected MODEL_PATH: {MODEL_PATH}")
print(f"DEBUG main.py: Expected TRAINING_COLS_PATH: {TRAINING_COLS_PATH}")

def load_ml_artifacts():
    global ml_model, ml_training_columns
    print("--- Attempting to load LOGISTIC ML artifacts ---")
    try:
        if not os.path.exists(MODEL_PATH): print(f"FATAL: Model NOT FOUND: {MODEL_PATH}"); return False
        if not os.path.exists(TRAINING_COLS_PATH): print(f"FATAL: Cols NOT FOUND: {TRAINING_COLS_PATH}"); return False
        ml_model = joblib.load(MODEL_PATH)
        ml_training_columns = joblib.load(TRAINING_COLS_PATH)
        print(f"Loaded LOGISTIC model. Type: {type(ml_model)}")
        print(f"Loaded {len(ml_training_columns)} training columns: {ml_training_columns}")
        print("--- LOGISTIC ML artifacts loaded ---")
        return True
    except Exception as e: print(f"FATAL loading LOGISTIC artifacts: {e}"); traceback.print_exc(); return False

if not load_ml_artifacts(): print("CRITICAL WARNING: LOGISTIC ML artifacts failed to load.")


# --- Routes ---
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='PCOS Symptom Insights - Advanced Model',
                           prediction_result=None, request=request)

@main.route('/profile', methods=['GET']) # Only GET for displaying profile info
@login_required
def profile():
    # Basic profile display, no image, no password change form here
    return render_template('profile.html',
                           title=f"{current_user.username}'s Profile",
                           user=current_user)

# REMOVED /change_password route

# --- PCOS Prediction Route (Keep as is from latest working version) ---
@main.route('/predict_pcos_via_form', methods=['POST'])
@login_required
def predict_pcos_via_form():
    global ml_model, ml_training_columns
    prediction_data_for_template = None 
    submitted_form_data = request.form.to_dict() 
    print(f"\n[PREDICT STEP 0] --- New Prediction Request (Logistic Model) ---")
    print(f"[PREDICT STEP 0] Raw form data received: {submitted_form_data}")

    if not ml_model or not ml_training_columns:
        print("[PREDICT STEP 0] Model/cols not loaded."); flash('Model not available.', 'danger')
        return render_template('index.html', title='PCOS Insights', prediction_result={'error': 'Model unavailable'}, request=request) 
    print(f"[PREDICT STEP 0] Model expects {len(ml_training_columns)} ORIGINAL columns: {ml_training_columns}\n")

    html_input_name_map = {
        'Age (yrs)': 'age_from_form', 'Weight (Kg)': 'weight_from_form', 'BMI': 'bmi_from_form',
        'Cycle length(days)': 'cycle_length_from_form', 'Waist(inch)': 'waist_inch_from_form',
        'AMH(ng/mL)': 'amh_ng_ml_from_form', 'Follicle No. (L)': 'follicle_no_l_from_form',
        'Follicle No. (R)': 'follicle_no_r_from_form', 'Cycle(R/I)': 'cycle_regularity_from_form',
        'Weight gain(Y/N)': 'weight_gain_y_n_from_form', 'hair growth(Y/N)': 'hair_growth_y_n_from_form',
        'Skin darkening (Y/N)': 'skin_darkening_y_n_from_form', 'Hair loss(Y/N)': 'hair_loss_y_n_from_form',
        'Pimples(Y/N)': 'pimples_y_n_from_form', 'Fast food (Y/N)': 'fast_food_y_n_from_form'
    }
    cycle_value_mapping = {"Irregular": "4", "Regular": "2"}
    
    current_input_row = {}
    print("[PREDICT STEP 1] Mapping form data to model's expected ORIGINAL features...")
    for model_col_name in ml_training_columns:
        html_form_key = html_input_name_map.get(model_col_name)
        processed_value = np.nan 
        if not html_form_key: print(f"  FATAL MAP ERROR: No HTML key for '{model_col_name}'.")
        elif model_col_name == 'Cycle(R/I)':
            raw_form_val = submitted_form_data.get(html_form_key) 
            processed_value = cycle_value_mapping.get(raw_form_val, "2") 
            print(f"  Mapped (Cycle): Model='{model_col_name}', HTML Key='{html_form_key}', Raw='{raw_form_val}', Processed='{processed_value}'")
        elif model_col_name == 'Fast food (Y/N)':
            processed_value = "1.0" if html_form_key in submitted_form_data else "0.0"
            print(f"  Mapped (Fast food Y/N): Model='{model_col_name}', HTML Key='{html_form_key}', Key Present: {html_form_key in submitted_form_data}, Processed='{processed_value}'")
        elif model_col_name.endswith('(Y/N)'):
            processed_value = "1" if html_form_key in submitted_form_data else "0"
            print(f"  Mapped (Other Y/N): Model='{model_col_name}', HTML Key='{html_form_key}', Key Present: {html_form_key in submitted_form_data}, Processed='{processed_value}'")
        else: 
            raw_form_val = submitted_form_data.get(html_form_key)
            if raw_form_val is not None and str(raw_form_val).strip() != "":
                try: processed_value = float(raw_form_val)
                except ValueError: processed_value = np.nan
            else: processed_value = np.nan
            print(f"  Mapped (Numeric): Model='{model_col_name}', HTML Key='{html_form_key}', Raw='{raw_form_val}', Processed='{processed_value}'")
        current_input_row[model_col_name] = processed_value
    
    print(f"\n[PREDICT STEP 2] Constructed input row for DataFrame: {current_input_row}\n")
    try:
        input_df = pd.DataFrame([current_input_row])
        input_df_ordered = input_df[ml_training_columns]
    except Exception as e_df: print(f"FATAL ERROR creating DataFrame: {e_df}"); traceback.print_exc(); flash("Data prep error.", "danger"); return render_template('index.html', title='PCOS Insights', prediction_result={'error': 'Data prep error'}, request=request)
    print(f"[PREDICT STEP 3] Final DataFrame sent to LOGISTIC model:\n{input_df_ordered.to_string()}")
    print(f"[PREDICT STEP 3] Dtypes:\n{input_df_ordered.dtypes.to_string()}\n")
    print("[PREDICT STEP 4] Predicting...")
    try:
        prediction_proba = ml_model.predict_proba(input_df_ordered)[0]
    except Exception as e_pred: print(f"FATAL ERROR predict_proba: {e_pred}"); traceback.print_exc(); flash("Prediction engine error.", "danger"); return render_template('index.html', title='PCOS Insights', prediction_result={'error': 'Prediction error'}, request=request)
    print(f"[PREDICT STEP 4] Probabilities: {prediction_proba}")
    PCOS_PROBABILITY_THRESHOLD = 0.30 
    confidence_of_pcos = float(prediction_proba[1])
    pcos_status_text = "Likely PCOS" if confidence_of_pcos >= PCOS_PROBABILITY_THRESHOLD else "Unlikely PCOS"
    print(f"[PREDICT STEP 4.5] Threshold={PCOS_PROBABILITY_THRESHOLD}, P(PCOS)={confidence_of_pcos:.4f}, Status={pcos_status_text}")
    prediction_data_for_template = {'pcos_status': pcos_status_text, 'confidence': confidence_of_pcos}
    flash('Analysis complete!', 'success')
    print(f"[PREDICT STEP 5] Data to template: {prediction_data_for_template}\n")
    return render_template('index.html', title='PCOS Symptom Insights', 
                           prediction_result=prediction_data_for_template, request=request)
