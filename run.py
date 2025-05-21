# run.py
from project import create_app # Imports from the 'project' folder's __init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
