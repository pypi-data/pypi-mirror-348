# agi_lab/reasoning/neuro_symbolic.py

import numpy as np
from memory.symbolic import Ontology
from memory.sub_symbolic import LatentRepresentation

class NeuroSymbolicBridge:
    """
    Puente entre representaciones simbólicas y subsimbólicas.
    Permite mapear conceptos a vectores y viceversa.
    """
    def __init__(self, dim=32):
        self.ontology = Ontology()
        self.latents = LatentRepresentation(dim)
        self.concept_map = {}  # nombre -> clave en embeddings

    def add_concept(self, concept):
        self.ontology.add_concept(concept)
        self.concept_map[concept.name] = concept.name
        self.latents.encode(concept.name)

    def relate_concepts_semantically(self):
        """
        Crea relaciones de similitud simbólica basadas en embeddings.
        """
        names = list(self.concept_map.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                sim = self.latents.similarity(names[i], names[j])
                if sim > 0.7:  # umbral ajustado para permitir más relaciones
                    self.ontology.relate_concepts(names[i], names[j], "similar")

    def explain_vector(self, vec):
        """
        Devuelve el concepto simbólicamente más cercano a un vector dado.
        """
        best_name = None
        best_score = -float("inf")
        for name in self.concept_map:
            key_vec = self.latents.encode(name)
            score = vec @ key_vec / (np.linalg.norm(vec) * np.linalg.norm(key_vec))
            if score > best_score:
                best_score = score
                best_name = name
        return best_name

    def symbolic_to_vector(self, name):
        return self.latents.encode(name)

    def vector_to_symbolic(self, vec):
        return self.explain_vector(vec)

    def get_ontology(self):
        return self.ontology