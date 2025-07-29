# Example fuzzy rough model (simplified): frutil/models/owafrs.py
"""
OWAFRS implementation.
"""
import numpy as np

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))


from approximations import FuzzyRoughModel
import numpy as np

class OWAFRS(FuzzyRoughModel):
    def lower_approximation(self):
        raise NotImplementedError
        return np.min(self.similarity_matrix, axis=1)

    def upper_approximation(self):
        raise NotImplementedError
        return np.max(self.similarity_matrix, axis=1)