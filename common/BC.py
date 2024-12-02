from numpy.polynomial import polynomial

class BC:
  """
  Class for boundary condition creation and storage.

  Example construction:
    BC(geom='line', nodes=[1, 2], kind='convection', value=0, coefficient=100)
    
  Has the following attributes:
  geom: should be 'node', 'line', or 'face'
  nodes: should be a list of 1, 2, or 3, nodes
  kind: type of boundary condition (e.g. "convection")
  value: value associated with BC (e.g. T_inf)
        for all geoms: can be specified as a constant value
        for lines: can be specified as a NumPy polynomial on the range [0,1]
        for lines or faces: can be specified as a function name in real space: myVar(x, y)
  coefficient: coefficient associated with BC (e.g. h)
  direction: direction used for forces in structural loads
        can be: 'n' for normal (outward), 't' for tangential (pointed from first node to second)
                'x' for x direction, or 'y' for y direction
  
  """
  def __init__(self, geom, nodes, kind, value=0, coefficient=0, direction='n'):
    # Run checks
    if type(nodes) != type([]):
        raise Exception('Error in BC creation: "nodes" should be a list, even for single points')
    if geom == 'point':
        if len(nodes)!=1:
            raise Exception('Error in BC creation: a "point" BC should have exactly 1 node.')
    elif geom == 'line':
        if len(nodes)!=2:
            raise Exception('Error in BC creation: a "line" BC should have exactly 2 nodes.')
    elif geom == 'face':
        if len(nodes)<3:
            raise Exception('Error in BC creation: a "face" BC should have at least 3 nodes.')
    else:
        raise Exception('Error in BC creation: "geom" must be "point", "line", or "face".')
    
    self.geom = geom
    self.nodes = nodes
    self.kind = kind
    self.value = value
    self.coefficient = coefficient
    self.direction = direction
    #self.valueVarType = None
    #self.coefVarType = None
    
    # Get type of variation for value
    if (type(value) == type(1) or type(value) == type(1.0)):
      pass
    elif (type(value) == type(polynomial.Polynomial(0))):
      pass
    elif (type(value) == type(lambda a:a)):
      pass
    else:
        raise Exception('Error in BC creation: "value" must be a constant value, a numpy polynomial, or a user-defined function.')
    
    # Get type of variation for coefficient
    if (type(coefficient) == type(1) or type(coefficient) == type(1.0)):
      pass
    elif (type(coefficient) == type(polynomial.Polynomial(0))):
      pass
    elif (type(coefficient) == type(lambda a:a)):
      pass
    else:
        raise Exception('Error in BC creation: "coefficient" must be a constant value, a numpy polynomial, or a user-defined function.')

  def __str__(self):
    return f"BC with {self.kind} kind on {self.geom} (nodes {self.nodes}): value={self.value}, coefficient={self.coefficient}."
  def copy(self):
    return BC(geom=self.geom, nodes=self.nodes, kind=self.kind, value=self.value, coefficient=self.coefficient)

  def VarType(self, valOrCoef):
    if (valOrCoef == 'value'):
      check = self.value
    elif (valOrCoef == 'coefficient'):
      check = self.coefficient
    else:
      raise Exception('Error in BC.VarType: can only check value or coefficient')
      
    if (type(check) == type(1) or type(check) == type(1.0)):
      return 'const'
    elif (type(check) == type(polynomial.Polynomial(0))):
      return 'poly'
    elif (type(check) == type(lambda a:a)):
      return 'func'