# agi_lab/environments/env_base.py

from abc import ABC, abstractmethod

class AGIEnvironment(ABC):
    """
    Interfaz base para entornos compatibles con agentes de AGI.
    Inspirado en Gym, pero más general para tareas cognitivas simbólicas o conexionistas.
    """

    def __init__(self):
        self.observation_space = None
        self.action_space = None

    @abstractmethod
    def reset(self):
        """
        Reinicia el entorno a su estado inicial y devuelve la primera observación.
        """
        pass

    @abstractmethod
    def step(self, action):
        """
        Ejecuta una acción y devuelve:
        - nueva observación
        - recompensa
        - done (booleano si el episodio termina)
        - info (diccionario opcional)
        """
        pass

    @abstractmethod
    def render(self):
        """
        Representa visualmente el entorno (opcional).
        """
        pass
