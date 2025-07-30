import math

class Node:
    def __init__(self, data, children = (), _op = '', mark = ''):
        self.data = data
        self.grad = 0.0
        self.kids = children
        self.actn = _op
        self.mark = mark
        self._back = lambda: None
        
    def __repr__(self):
        return f"Node({self.data}, {self.kids}, '{self.actn}', '{self.mark}')"

    def __str__(self):
        return f"Node: {self.data}, Action: {self.actn}, Mark: {self.mark}, Children: {self.kids}"

    def __len__(self):
        return len(self.kids)
    
    def __getitem__(self, i):
        return self.kids[i]
    
    def __setitem__(self, i, v):
        self.kids[i] = v
        
    def __delitem__(self, i):
        del self.kids[i]
        
    def __iter__(self):
        return iter(self.kids)
    
    def __contains__(self, item):
        return item in self.kids
    
    def __call__(self, *args, **kwargs):
        return self.data(*args, **kwargs)
    
    def __add__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        if not isinstance(other, Node):
            raise TypeError(f"Cannot add {type(other)} to Node")
        out = Node(self.data + other.data, (self, other), '+')

        def _back():
           self.grad += 1.0 * out.grad
           other.grad += 1.0 * out.grad
        out._back = _back
        
        return out

    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        if not isinstance(other, Node):
            raise TypeError(f"Cannot subtract {type(other)} from Node")
        out = Node(self.data - other.data, (self, other), '-')

        def _back():
            self.grad -= 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._back = _back

        return out

    def __rsub__(self, other):
        return self - other
    
    def __mul__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        if not isinstance(other, Node):
            raise TypeError(f"Cannot multiply {type(other)} with Node")
        out = Node(self.data * other.data, (self, other), '*')

        def _back():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._back = _back

        return out

    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        if not isinstance(other, Node):
            raise TypeError(f"Cannot divide {type(other)} by Node")
        out = Node(self.data / other.data, (self, other), '/')

        def _back():
            self.grad += (1 / other.data) * out.grad
            other.grad -= (self.data / other.data**2) * out.grad
        out._back = _back

        return out

    def __rtruediv__(self, other):
        return self / other

    def __pow__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        if not isinstance(other, Node):
            raise TypeError(f"Cannot exponentiate {type(other)} with Node")
        return Node(self.data ** other.data, (self, other), '**')

    def __neg__(self):
        return Node(-self.data, (self,), 'neg')

    def tanh(self):
        x = self.data
        t = (math.exp(2*x) - 1) / (math.exp(2*x) + 1)
        out = Node(t, (self,), 'tanh')

        def _back():
            self.grad += (1 - t**2) * out.grad

        out._back = _back
        return out
    
    def backward(self):
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v.kids:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1.0
        for v in reversed(topo):
            v._back()
        return self.grad