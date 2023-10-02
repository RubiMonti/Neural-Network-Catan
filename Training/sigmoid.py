import math
def sigmoid(x):
  if x<-500:
    return 0
  else:
    return 1 / (1 + math.exp(-x))