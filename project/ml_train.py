# THIS IS YOUR ML TRAINING SCRIPT (pcod.py)

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt # Keep if you have plots you want to see during training
# import seaborn as sns # Keep if you have plots
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score # Add roc_curve if plotting
from imblearn.over_sampling import SMOTE
import joblib
import os # For path joining if you use specific output directories

# --- 1. Load Data & Initial Cleaning ---
print("--- Loading and Initial Cleaning ---")
# (Your existing data loading and initial cleaning code)
# ...
try:
    # Ensure this path is correct for your system
    data = pd.read_excel('C:\\Users\\gayat\\project25\\PCOS_data_without_infertility.xlsx', sheet_name="Full_new")
    print("Data loaded successfully.")
except FileNotFoundError:
    print("ERROR: PCOS_data_without_infertility.xlsx not found. Please check the file path.")
    exit()

data.columns = data.columns.str.strip()
# ... (rest of your initial cleaning: dropping columns, fixing specific values) ...
# Example for problematic numeric cols:
problematic_numeric_cols = ['AMH(ng/mL)', 'II    beta-HCG(mIU/mL)']
# ... (your loop to clean these) ...

if 'PCOS (Y/N)' not in data.columns:
    print("ERROR: Target column 'PCOS (Y/N)' not found in the dataset.")
    exit()
X = data.drop('PCOS (Y/N)', axis=1)
y = data['PCOS (Y/N)']
# ...

# --- 2. Preprocessing ---
print("\n--- Preprocessing: Defining Feature Lists and Pipelines ---")
numerical_features = X.select_dtypes(include=np.number).columns.tolist()
categorical_features = X.select_dtypes(include='object').columns.tolist()

potential_cats_in_numeric = []
if 'Cycle(R/I)' in numerical_features:
    potential_cats_in_numeric.append('Cycle(R/I)')
    numerical_features.remove('Cycle(R/I)')
if 'Blood Group' in numerical_features:
    potential_cats_in_numeric.append('Blood Group')
    numerical_features.remove('Blood Group')
# Ensure Y/N features (even if 0/1 numerically) are treated as categorical for one-hot encoding
yes_no_features_to_categorize = [
    'Weight gain(Y/N)', 'hair growth(Y/N)', 'Skin darkening (Y/N)',
    'Hair loss(Y/N)', 'Pimples(Y/N)', 'Fast food (Y/N)', 'Reg.Exercise(Y/N)',
    'Pregnant(Y/N)' # If this is a Y/N feature
]
for feature_name in yes_no_features_to_categorize:
    if feature_name in numerical_features:
        numerical_features.remove(feature_name)
        if feature_name not in categorical_features:
            categorical_features.append(feature_name)
    elif feature_name in X.columns and feature_name not in categorical_features: # If it was object/other and not yet added
        categorical_features.append(feature_name)

categorical_features.extend(potential_cats_in_numeric)
# Remove duplicates just in case
categorical_features = sorted(list(set(categorical_features)))
numerical_features = sorted(list(set(numerical_features)))


for col in categorical_features:
    if col in X.columns:
        X[col] = X[col].astype(str)

print(f"Final Numerical features for preprocessing: {numerical_features}")
print(f"Final Categorical features for preprocessing: {categorical_features}")

numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Define the preprocessor
preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_features),
    ('cat', categorical_pipeline, categorical_features)
], remainder='passthrough') # 'passthrough' in case some columns are missed, though ideally all are covered.

# --- 3. Splitting Data ---
print("\n--- Splitting Data ---")
all_feature_names_for_preprocessor = X.columns.tolist() # Columns of X before train/test split
print(f"All feature names considered for preprocessor (in order): {all_feature_names_for_preprocessor}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")


# --- 4. FITTING THE PREPROCESSOR AND TRANSFORMING DATA (CRUCIAL STEP) ---
print("\n--- Fitting Preprocessor and Transforming Data ---")
try:
    # Fit the preprocessor on X_train and transform X_train
    # THIS IS WHERE THE PREPROCESSOR LEARNS AND GETS "FITTED"
    X_train_processed = preprocessor.fit_transform(X_train)
    print("Preprocessor FITTED successfully on X_train.")

    # Transform X_test using the ALREADY FITTED preprocessor
    X_test_processed = preprocessor.transform(X_test)
    print("X_test transformed successfully using the fitted preprocessor.")
    print(f"X_train_processed shape: {X_train_processed.shape}")

except ValueError as ve:
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"CRITICAL ValueError during preprocessor fitting/transformation: {ve}")
    print(f"This often means there's a mismatch between your feature lists (numerical/categorical)")
    print(f"and the actual data types in the columns they are supposed to process.")
    print(f"For example, a string value ('Yes') might be in a column designated as 'numerical'.")
    print(f"Check the definitions of 'numerical_features' and 'categorical_features'.")
    print(f"Also check the 'yes_no_features_to_categorize' list.")
    print(f"Exiting script. Please fix the feature definitions before re-running.")
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    exit() # Stop script if preprocessor fitting fails
except Exception as e:
    print(f"AN UNEXPECTED ERROR occurred during preprocessor fitting or transformation: {e}")
    exit() # Stop script


# --- 5. Handling Class Imbalance (SMOTE) ---
print("\n--- Handling Class Imbalance using SMOTE ---")
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_processed, y_train)
# ... (print statements for SMOTE) ...

# --- 6. Training a RandomForestClassifier Model ---
print("\n--- Training RandomForestClassifier Model ---")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced_subsample')
model.fit(X_train_resampled, y_train_resampled)
print("Model training complete.")

# --- 7. Evaluating the Model ---
print("\n--- Evaluating the Model ---")
# ... (your evaluation code: classification_report, confusion_matrix, roc_auc_score) ...
y_pred = model.predict(X_test_processed)
y_pred_proba = model.predict_proba(X_test_processed)[:, 1]
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"\nROC AUC Score: {auc_score:.4f}")


# --- 8. SAVING ARTIFACTS ---
# This section should only be reached if all previous steps, especially preprocessor fitting, were successful.
print("\n--- Saving Artifacts ---")

script_directory = os.path.dirname(os.path.abspath(__file__)) # Saves next to script

# 8.1. Save the trained model
try:
    model_path = os.path.join(script_directory, 'pcos_model.joblib')
    joblib.dump(model, model_path)
    print(f"Trained model saved as {model_path}")
except Exception as e:
    print(f"Error saving model: {e}")

# 8.2. Save the FITTED preprocessor
try:
    preprocessor_path = os.path.join(script_directory, 'pcos_preprocessor.joblib')
    joblib.dump(preprocessor, preprocessor_path) # 'preprocessor' is now the FITTED object
    print(f"Fitted preprocessor saved as {preprocessor_path}")
except Exception as e:
    print(f"Error saving preprocessor: {e}")

# 8.3. Save the list of training column names
try:
    columns_path = os.path.join(script_directory, 'training_columns.joblib')
    joblib.dump(all_feature_names_for_preprocessor, columns_path)
    print(f"Training column names (order for preprocessor) saved as {columns_path}")
except Exception as e:
    print(f"Error saving training columns: {e}")

print("--- ML Training Script Finished ---")
