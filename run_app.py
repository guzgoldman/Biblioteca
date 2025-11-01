import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Try imports to validate environment
try:
    import sqlalchemy
    from db.Conector import Base
    from modelo.Libro import Libro
    from modelo.LibroCategoria import LibroCategoria
    from modelo.Categoria import Categoria
    print("Environment setup successful!")
    print("SQLAlchemy version:", sqlalchemy.__version__)
    print("All models imported correctly")
except ImportError as e:
    print("Error importing dependencies:", str(e))
    print("\nPlease run these commands to set up the environment:")
    print("python -m venv venv")
    print(".\\venv\\Scripts\\Activate.ps1")
    print("python -m pip install -r requirements.txt")
    sys.exit(1)

# If everything is OK, run the main dashboard
from vista.login import LoginWindow

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()