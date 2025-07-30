# agi_lab/memory/sub_symbolic.py

import numpy as np

class LatentRepresentation:
    """
    Representación subsimbólica (embedding) de conceptos o experiencias.
    """
    def __init__(self, dim=32):
        self.dim = dim
        self.embeddings = {}

    def encode(self, key):
        if key not in self.embeddings:
            self.embeddings[key] = np.random.normal(0, 1, self.dim)
        return self.embeddings[key]

    def similarity(self, key1, key2):
        v1 = self.encode(key1)
        v2 = self.encode(key2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def project(self, key, direction, alpha=0.1):
        """
        Proyecta el embedding hacia una dirección dada (ej. retropropagación simbólica).
        """
        self.embeddings[key] = self.encode(key) + alpha * direction

    def distance(self, key1, key2):
        v1 = self.encode(key1)
        v2 = self.encode(key2)
        return np.linalg.norm(v1 - v2)