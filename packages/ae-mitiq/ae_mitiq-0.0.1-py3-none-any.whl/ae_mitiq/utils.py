import itertools
import numpy as np

def full_counts(counts:dict, num_qubits=4):
    all_bitstrings = ["".join(states) for states in itertools.product("01", repeat=num_qubits)]    
    return np.array([counts.get(key, 0) for key in all_bitstrings])

def vector_MAE(predict, target):
    return np.sum(abs(predict-target))/16