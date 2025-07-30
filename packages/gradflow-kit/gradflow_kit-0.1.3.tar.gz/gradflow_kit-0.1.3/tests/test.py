import pytest
from micrograd import Node, draw_dot

def test_node_operations():
    # Test addition
    a = Node(2.0)
    b = Node(3.0)
    c = a + b
    assert c.data == 5.0
    assert c.grad == 0.0
    c._back()
    assert a.grad == 1.0
    assert b.grad == 1.0

    # Test subtraction
    d = a - b
    assert d.data == -1.0
    assert d.grad == 0.0
    d._back()
    assert a.grad == 1.0
    assert b.grad == -1.0

    # Test multiplication
    e = a * b
    assert e.data == 6.0
    assert e.grad == 0.0
    e._back()
    assert a.grad == 3.0
    assert b.grad == 2.0

    # Test division
    f = a / b
    assert f.data == pytest.approx(2/3, rel=1e-5)
    assert f.grad == 0.0
    
    f._back()
    assert a.grad == 1/3
    assert b.grad == -2/3
    
    # Test power
    g = a ** 2
    assert g.data == 4.0
    assert g.grad == 0.0
    g._back()
    assert a.grad == 4.0
    
    # Test negation
    h = -a
    assert h.data == -2.0
    assert h.grad == 0.0
    h._back()
    assert a.grad == -1.0

def test_node_trace():
    a = Node(2.0)
    b = Node(3.0)
    c = a + b
    d = c * 2.0
    e = d / 4.0

    dot = draw_dot(e, format='svg')
    assert isinstance(dot, str)  # Check if dot is a string (SVG format)
    
    # Check if the nodes and edges are correctly represented in the dot string
    assert 'digraph' in dot
    assert 'node' in dot
    assert 'edge' in dot
    assert 'data' in dot
    assert 'grad' in dot
    assert 'mark' in dot
    assert 'actn' in dot
    assert 'kids' in dot
    
if __name__ == "__main__":
    pytest.main()
