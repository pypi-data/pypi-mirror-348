# agi_lab/memory/symbolic.py

class SymbolicConcept:
    """
    Representación simbólica de un concepto con relaciones semánticas.
    """
    def __init__(self, name):
        self.name = name
        self.attributes = {}
        self.relations = {}

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def relate(self, other_concept, relation_type):
        if relation_type not in self.relations:
            self.relations[relation_type] = []
        self.relations[relation_type].append(other_concept.name)


class Ontology:
    """
    Ontología algebraica: conjunto jerárquico y semántico de conceptos.
    """
    def __init__(self):
        self.concepts = {}

    def add_concept(self, concept):
        self.concepts[concept.name] = concept

    def find_by_attribute(self, key, value):
        return [c for c in self.concepts.values() if c.attributes.get(key) == value]

    def relate_concepts(self, name1, name2, relation):
        if name1 in self.concepts and name2 in self.concepts:
            self.concepts[name1].relate(self.concepts[name2], relation)

    def __str__(self):
        return "\n".join(f"{c.name}: {c.relations}" for c in self.concepts.values())