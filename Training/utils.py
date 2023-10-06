class Stack:
    """
    Se crea una clase que contenga una lista que siga la política last-in-first-out (LIFO)
        Push: Mete cosas en la pila
        Pop: Saca el último elemento de la pila
        isEmpty: Comprueba si la pila está vacía
    """
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0