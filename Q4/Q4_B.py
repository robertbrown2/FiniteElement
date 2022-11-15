def Q4_B(x1234, y1234, xi, eta, type2D='planeStress'):
  """
  Find the B Matrix for a quadrilateral element with four nodes.
  B = Q4_B(x1234, y1234, xi, eta)
  4 -------- 3
  |          |
  |          |
  |          |
  |          |
  1 -------- 2 
  ---------
    Input
  ---------
  x1234: (list) - x values of nodes
  y1234: (list) - y values of nodes
  xi: (float) - location at which to calculate B matrix
  eta: (float) - location at which to calculate B matrix
  ----------
    Output
  ----------
  B: (3x8 array) - B matrix
  """
  from numpy import array, linalg, zeros
  from .Q4_J import Q4_J
  from .Q4_shapeFunctions import Q4_shapeDerivatives, Q4_shapeFunctions
  
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)

  Jinv = linalg.inv(Q4_J(x1234, y1234, xi, eta))

  if (type2D == 'axisymmetric'):
    psi = Q4_shapeFunctions(xi, eta)
    B = zeros((4, 8))
    for i in range(4):
      dpsidxy = Jinv @ array([dpsidxi[i], dpsideta[i]])
      B[0, 2*i  ] = dpsidxy[0]
      B[1, 2*i+1] = dpsidxy[1]
      B[2, 2*i  ] = psi[i] / (array(x1234) @ array(psi))
      B[3, 2*i  ] = dpsidxy[1]
      B[3, 2*i+1] = dpsidxy[0]
  else:
    B = zeros((3, 8))
    for i in range(4):
      dpsidxy = Jinv @ array([dpsidxi[i], dpsideta[i]])
      B[0, 2*i  ] = dpsidxy[0]
      B[1, 2*i+1] = dpsidxy[1]
      B[2, 2*i  ] = dpsidxy[1]
      B[2, 2*i+1] = dpsidxy[0]

  return array(B)
