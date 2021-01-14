import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pyfenstein3d'))
print(sys.path)
sys.path.insert(0, path)
print(sys.path)