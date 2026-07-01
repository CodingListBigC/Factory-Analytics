# environment.py

# 1. Configure the matplotlib backend BEFORE importing pyplot
import matplotlib

matplotlib.use("qtagg")

# 2. Explicitly import the tools you need
import numpy as np
import matplotlib.pyplot as plt

# NumPy setting.
np.set_printoptions(suppress=True, precision=2)


# 3. Pack them into an __all__ list or a simple namespace class
# so your main files can access them cleanly without wildcard (*) issues.
class Env:
    np = np
    plt = plt
