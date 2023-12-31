import math
import CreateNN
import numpy as np

def sigmoid(x):
  if x<-500:
    return 0
  else:
    return 1 / (1 + math.exp(-x))

def sigmoid_all(X):
  result = []
  for i in X:
    result += [[sigmoid(i)]]
  return np.array(result)

def NN(red,entradas):
    num_capas = len(red)
    entradas = np.array(entradas)
    entradas = np.reshape(entradas,(len(entradas),1))
    y = sigmoid_all(np.matmul(red[0].W,entradas) + red[0].B)
    for i in range(1, num_capas):
      y = sigmoid_all(np.matmul(red[i].W,y) + red[i].B)
    return y
