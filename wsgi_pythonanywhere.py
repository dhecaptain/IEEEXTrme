import sys
import os

# ===== EDIT THESE LINES =====
# Replace 'YOURUSERNAME' with your PythonAnywhere username
username = 'YOURUSERNAME'
# ============================

# Add your project directory to the sys.path
project_home = f'/home/{username}/ieeextreme'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment
os.chdir(project_home)

# Import flask app
from app import app as application
