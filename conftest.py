import sys
import os

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Optional: Also add src directory if your modules are in a src folder
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
