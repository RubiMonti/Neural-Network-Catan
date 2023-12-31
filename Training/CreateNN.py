import numpy as np

class Capa:
    def __init__(self,size,prev_size):
        self.size = size
        self.prev_size = prev_size
        self.W = np.zeros((size,prev_size))
        self.B = np.zeros((size, 1))
    
    def size_W(self):
        return np.size(self.W)

    def size_B(self):
        return np.size(self.B)

    def fill_W(self, X):
        for i in range(self.size):
            for j in range(self.prev_size):
                self.W[i,j] = X[i*self.prev_size+j]
    
    def fill_B(self, x):
        for i in range(self.size):
            self.B[i,0] = x[i]

def CreateNN(wb, num_neuronas_ocultas, num_entradas, num_neuronas_salida):
    """
    Función que crea una red neuronal con cualquier número de neuronas y capas ocultas introducidas por parámetros:
        - WB: Valores de los pesos y términos independientes de cada neurona
        - NUM_NEURONAS_OCULTAS: vector con el número de neuronas que hay en cada capa (la longitud del vector indicará el número de capas)
        - NUM_ENTRADAS: numero de entradas de la red_neuronal
        - NUM_NEURONAS_SALIDA: numero de salidas de la red neuronal
    """
    # Contador que irá recorriendo el vector de pesos y terminos independientes
    cont = 0
    num_capas = len(num_neuronas_ocultas)
    red = []
    for i in range(num_capas):
        if i == 0:
            red += [Capa(num_neuronas_ocultas[i], num_entradas)]
        elif i == num_capas - 1:
            red += [Capa(num_neuronas_salida, num_neuronas_ocultas[i-1])]
        else:
            red += [Capa(num_neuronas_ocultas[i], num_neuronas_ocultas[i-1])]
        to_fill = red[i].size_W()
        red[i].fill_W(wb[cont:cont + to_fill])
        cont += to_fill
        to_fill = red[i].size_B()
        red[i].fill_B(wb[cont:cont + to_fill])
        cont += to_fill
    
    return red
