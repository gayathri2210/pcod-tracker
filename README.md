# PCOS Insights Platform (pcod-tracker)

A Flask-based web application designed to provide users with preliminary insights into Polycystic Ovary Syndrome (PCOS) based on self-reported symptoms and data. The application utilizes a machine learning model (Logistic Regression) to predict the likelihood of PCOS.

**IMPORTANT DISCLAIMER:** This tool is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.

## Features

*   User authentication (Signup, Login, Logout).
*   Symptom input form for 15 key PCOS-related data points.
*   Prediction of PCOS likelihood using a trained logistic regression model.
*   Display of prediction results (e.g., "Likely PCOS", "Unlikely PCOS") and the model's confidence score.

## Tech Stack

*   **Backend:** Python, Flask
*   **Database ORM:** Flask-SQLAlchemy
*   **Authentication:** Flask-Login
*   **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib
*   **Frontend:** HTML, CSS, JavaScript (Bootstrap 5 likely utilized for styling)
*   **Database (Local):** SQLite
*   **WSGI Server (Production):** Gunicorn (intended)

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   Git

### Installation & Setup

1.  **Clone the repository (if not already done):**
    ```
    git clone https://github.com/gayathri2210/pcod-tracker.git
    cd pcod-tracker
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows (PowerShell/CMD):
        ```
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4.  **Database Setup:**
    The application currently uses `db.create_all()` for a simple SQLite setup (e.g., in an `instance/` folder). Running the app for the first time should create the tables.

5.  **Run the application:**
    ```
    python run.py
    ```
    Access at `http://127.0.0.1:5000` (or as configured).

## Usage

1.  Navigate to the application.
2.  Sign up or Log in.
3.  Use the "Analysis Tool" to input symptoms.
4.  View the prediction.

## Machine Learning Model

*   Trained model and column list are in `project/pcos_app_files/`.
*   Retraining script: `retrain_minimal_pcos_model.py`.



## Deployment

Intended for deployment on platforms like Vercel, requiring a production database (e.g., PostgreSQL) and environment variable configuration. A `vercel.json` file would be needed.

## License

This project is currently unlicensed.
