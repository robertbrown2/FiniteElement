def LST_stiffness(xElem, yElem, xi, eta, D, thickness=None, type2D='planeStress'):
  """
  Calculate the stiffness matrix for a Q4 element
  Usage - K = Q4_stiffness(xElem, yElem, xi, eta, D, thickness)
  ---------
    Input
  ---------
  xElem - (list) x locations of nodes
  yElem - (list) y locations of nodes
  xi - (float) position in unmapped element
  eta - (float) position in unmapped element
  D - (array) constituitive matrix
  thickness - (float) thickness of element in third dimension
  """
  from numpy import array, linalg, transpose
  from .LST_B import LST_B
  from .LST_J import LST_J
  from .LST_shapeFunctions import LST_shapeFunctions
  
  B = LST_B(xElem, yElem, xi, eta, type2D)
  if (type2D == 'axisymmetric'):
    psi = LST_shapeFunctions(xi, eta)
    thickness = 2*pi*(array(xElem) @ array(psi))
  Area = linalg.det(LST_J(xElem, yElem, xi, eta))
  return Area*thickness*(transpose(B)@D@B)
