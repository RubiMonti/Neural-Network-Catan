import CreateNN
import catan
from table import *
from game import *
from pygame.locals import *

def fitness_function_GA_NN(instance,x,x_idx):
    recompensa = 0
    # print(len(x))
    # print(x[:54160])
    # print("#########################\n\tRed\n################################")
    red = CreateNN.CreateNN(x, [4, 10],279,17)
    red_1 = 0
    red_2 = 0
    red_3 = 0
    red_5 = 0
    red_7 = 0
    red_8 = 0
    red_10 = 0
    red_11 = 0
    red_12 = 0
    red_16 = 0
    # print("#########################\n\tRed 1\n################################")
    # red_1 = CreateNN.CreateNN(x[2005:3130], [4, 10],279,1)
    # print("#########################\n\tRed 2\n################################")
    # red_2 = CreateNN.CreateNN(x[3130:4255], [4, 10],279,1)
    # print("#########################\n\tRed 3\n################################")
    # red_3 = CreateNN.CreateNN(x[4255:5380], [4, 10],279,1)
    # print("#########################\n\tRed 5\n################################")
    # red_5 = CreateNN.CreateNN(x[5380:6505], [4, 10],279,1)
    # print("#########################\n\tRed 7\n################################")
    # red_7 = CreateNN.CreateNN(x[6505:7630], [4, 10],279,1)
    # print("#########################\n\tRed 8\n################################")
    # red_8 = CreateNN.CreateNN(x[7630:8760], [4, 10],279,2)
    # print("#########################\n\tRed 10\n################################")
    # red_10 = CreateNN.CreateNN(x[8760:9885], [4, 10],279,1)
    # print("#########################\n\tRed 11\n################################")
    # red_11 = CreateNN.CreateNN(x[9885:11015], [4, 10],279,2)
    # print("#########################\n\tRed 12\n################################")
    # red_12 = CreateNN.CreateNN(x[11015:12382], [4, 10],337,3)
    # print("#########################\n\tRed 16\n################################")
    # red_16 = CreateNN.CreateNN(x[12382:], [4, 10],406,2)
    for i in range(100):
        result = catan.game_of_catan(red,red_1,red_2,red_3,red_5,red_7,red_8,red_10,red_11,red_12,red_16)
        if (result > 9):
            recompensa += 1
    print("La recompensa de esta solución es: ", recompensa)
    return recompensa