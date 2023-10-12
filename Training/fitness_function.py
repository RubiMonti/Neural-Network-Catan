import CreateNN
import catan
from table import *
from game import *
from pygame.locals import *

def fitness_function_GA_NN(instance,x,x_idx):
    recompensa = 0
    red = CreateNN.CreateNN(x, [4, 10],279,17)
    for i in range(100):
        result = catan.game_of_catan(red)
        if (result > 9):
            recompensa += 1
    print("La recompensa de esta solución es: ", recompensa)
    return recompensa