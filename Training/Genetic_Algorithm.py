import pickle
import numpy as np
import matplotlib.pyplot as plt
# import tensorflow as tf
import pygad as pg
from fitness_function import fitness_function_GA_NN 

NVARS = 1205

# num_genes = #Número de variables a encontrar 
# num_generations = #Número de generaciones
# sol_per_pop = #Número de soluciones (cromosomas) por generación 
# num_parents_mating = #Número de solu<ciones que serán seleccionadas para crear la siguiente generación
# init_range_low = #Límite inferior de las variables
# init_range_high = #Límite superior de las variables
# parent_selection_type = #Método de selección de las soluciones (cromosomas) que se cruzarán
# keep_parents = #Número de soluciones anteriores que mantiene para la generación posterior
# crossover_type = #Método de cruzado entre cromosomas
# mutation_type = #Tipo de mutación
# mutation_percent_genes = #Probabilidad de mutación de una solución o cromosoma

def on_gen(ga_instance):
    print("############################################")
    print("\tGeneration : ", ga_instance.generations_completed)
    print("\tFitness of the best solution :", ga_instance.best_solution()[1])
    print("############################################")

ga_instance = pg.GA(num_generations=100,
                       num_parents_mating=2,
                       fitness_func=fitness_function_GA_NN,
                       sol_per_pop=10,
                       num_genes=NVARS,
                       init_range_low=-4,
                       init_range_high=4,
                       parent_selection_type="rank",
                       keep_parents=1,
                       crossover_type="single_point",
                       mutation_type="random",
                       mutation_percent_genes=10,
                       on_generation=on_gen)

ga_instance.run()
ga_instance.save("Catan")
ga_instance.plot_fitness()

x, x_fitness, x_idx = ga_instance.best_solution()
print('Solución: ' + str(x))
with open('Best_solution.txt', 'w') as f:
    for i in range(len(x)):
        f.write(str(x[i]))
        f.write("\n")
