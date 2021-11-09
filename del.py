import os

del_path = os.path.join(os.path.dirname(__file__), 'uploads')

for f in os.listdir(del_path):
    os.remove(os.path.join(del_path, f))