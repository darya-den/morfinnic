import numpy as np

language_codes = {"estonian.txt": np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                  "finnish.txt": np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0]),
                  "ingrian.txt": np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]),
                  "karelian.txt": np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
                  "veps.txt": np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0]),
                  "votic.txt": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0])}

language_class = {"estonian.txt": np.array([1]), "finnish.txt": np.array([2]),
                  "ingrian.txt": np.array([3]), "karelian.txt": np.array([4]),
                  "veps.txt": np.array([5]), "votic.txt": np.array([6])}

n_languages = len(language_codes)
