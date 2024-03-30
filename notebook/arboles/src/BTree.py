class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    # Función para imprimir el árbol
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)

    # Función de inserción
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:  # Si el nodo está lleno
            temp = BTreeNode()
            self.root = temp
            # Insertar el nodo anterior como hijo de la nueva raíz
            temp.child.insert(0, root)
            self.split_child(temp, 0)  # Dividir la raíz
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    # Función para insertar en un nodo que no está lleno
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = (k, None)
        else:
            while i >= 0 and k < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i][0]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    # Función para dividir un hijo
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t) - 1]
        y.keys = y.keys[0:(t - 1)]
        if not y.leaf:
            z.child = y.child[t:(2 * t)]
            y.child = y.child[0:t]


# Creación del árbol B y ejemplo de inserción
b_tree = BTree(3)  # Un árbol B con grado mínimo 3
for i in range(10):
    b_tree.insert(i)
b_tree.print_tree(b_tree.root)
