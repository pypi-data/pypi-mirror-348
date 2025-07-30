# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise10 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running Genetic Algorithm Implementation...\n")
    
    # Import required libraries (kept inside function as per pattern)
    import random
    import numpy as np

    # Enhanced fitness function with print
    def fitness_function(x):
        result = x ** 2
        print(f"Calculating fitness for {x:.2f} → {result:.2f}")
        return result

    # Enhanced selection function with print
    def selection(population):
        selected = sorted(population, key=fitness_function, reverse=True)[:2]
        print(f"Selected parents: {[f'{x:.2f}' for x in selected]}")
        return selected

    # Enhanced crossover function with print
    def crossover(parent1, parent2):
        child = (parent1 + parent2) / 2
        print(f"Crossover: ({parent1:.2f} + {parent2:.2f})/2 = {child:.2f}")
        return child

    # Enhanced mutation function with print
    def mutation(child):
        mutation_value = random.uniform(-1, 1)
        mutated = child + mutation_value
        print(f"Mutation: {child:.2f} + {mutation_value:.2f} = {mutated:.2f}")
        return mutated

    # Initialize population
    population = [random.uniform(-10, 10) for _ in range(6)]
    print(f"Initial population: {[f'{x:.2f}' for x in population]}\n")

    # Evolution process with generation tracking
    for generation in range(5):  # 5 generations
        print(f"--- Generation {generation + 1} ---")
        
        # Selection
        parents = selection(population)
        
        # Crossover
        child = crossover(parents[0], parents[1])
        
        # Mutation
        child = mutation(child)
        
        # Add child to population
        population.append(child)
        print(f"Population after adding child: {[f'{x:.2f}' for x in population]}")
        
        # Selection to keep best
        population = selection(population)
        print(f"Population after selection: {[f'{x:.2f}' for x in population]}\n")

    # Final results
    print("\n=== Final Results ===")
    print(f"Final population: {[f'{x:.2f}' for x in population]}")
    best_individual = max(population, key=fitness_function)
    print(f"Best solution found: {best_individual:.2f} (fitness: {fitness_function(best_individual):.2f})")

if __name__ == "__main__":
    run()