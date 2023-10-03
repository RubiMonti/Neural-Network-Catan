import catan
import sys
import CreateNN

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        arguments = []
        try:
            with open(filename) as file:
                for line in file:
                    arguments += [float(line)]
            print(arguments)
        except:
            print("Algo ha salido mal")
            sys.exit(-1)
        red = CreateNN.CreateNN(arguments, [4,10],279,17)
        wins = 0
        for i in range(100):
            result = catan.game_of_catan(red,0,0,0,0,0,0,0,0,0,0)
            print(result)
            if result[0] == 10:
                wins += 1
        print("El programa ha tenido un porcentaje de ", wins, "/100.")
