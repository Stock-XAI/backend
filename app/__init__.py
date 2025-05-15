import sys
import os

print("[DEBUG] sys.path =", sys.path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))