def Q4_stiffness(x1234, y1234, xi, eta, D, thickness=None, type2D='planeStress'):
  """
  Calculate the stiffness matrix for a Q4 element
  Usage - K = Q4_stiffness(x1234, y1234, xi, eta, D, thickness)
  ---------
    Input
  ---------
  x1234 - (list) x locations of nodes
  y1234 - (list) y locations of nodes
  xi - (float) position in unmapped element
  eta - (float) position in unmapped element
  D - (array) constituitive matrix
  thickness - (float) thickness of element in third dimension
  """
  from numpy import array
  from .Q4_B import Q4_B
  from .Q4_shapeFunctions import Q4_shapeFunctions
  B = Q4_B(x1234, y1234, xi, eta, type2D)
  if (type2D == 'axisymmetric'):
    psi = Q4_shapeFunctions(xi, eta)
    thickness = 2*pi*(array(x1234) @ array(psi))
  return Q4_area(x1234, y1234)*thickness*(transpose(B)@D@B)
