# agi_lab/learning/evolutionary.py

import numpy as np

class GeneticOptimizer:
    """
    Optimiza una población de agentes mediante selección, cruce y mutación.
    """
    def __init__(self, population, mutation_rate=0.1, elite_fraction=0.2):
        self.population = population
        self.mutation_rate = mutation_rate
        self.elite_fraction = elite_fraction

    def evaluate(self, env, episodes=1):
        """
        Evalúa cada agente en el entorno y devuelve una lista de scores.
        """
        scores = []
        for agent in self.population:
            total_reward = 0
            for _ in range(episodes):
                obs = env.reset()
                done = False
                while not done:
                    agent.perceive(obs)
                    action = agent.decide()
                    obs, reward, done, _ = env.step(action)
                    agent.learn(reward, done)
                    total_reward += reward
            scores.append(total_reward)
        return np.array(scores)

    def select_elite(self, scores):
        """
        Selecciona los mejores agentes según la fracción de élite.
        """
        elite_size = max(1, int(len(scores) * self.elite_fraction))
        elite_indices = np.argsort(scores)[-elite_size:]
        return [self.population[i] for i in elite_indices]

    def crossover_and_mutate(self, elite):
        """
        Genera una nueva población cruzando y mutando a los élite.
        """
        new_population = []
        while len(new_population) < len(self.population):
            p1, p2 = np.random.choice(elite, 2, replace=True)
            child = p1.evolve(p2)
            new_population.append(child)
        self.population = new_population

    def step(self, env):
        """
        Ejecuta un paso del algoritmo evolutivo: evalúa, selecciona y muta.
        """
        scores = self.evaluate(env)
        elite = self.select_elite(scores)
        self.crossover_and_mutate(elite)
        return scores, elite