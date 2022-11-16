def LST_B(xElem, yElem, xi, eta, type2D='planeStress'):
  """
  Find the B Matrix for a triangular element with six nodes.
  B = Q4_B(xElem, yElem, xi, eta, type2D)
  ---------
    Input
  ---------
  xElem: (list) - x values of nodes
  yElem: (list) - y values of nodes
  xi: (float) - location at which to calculate B matrix
  eta: (float) - location at which to calculate B matrix
  ----------
    Output
  ----------
  B: (3x12 array) - B matrix
  """
  from numpy import array, linalg, zeros
  from .LST_shapeFunctions import LST_shapeDerivatives, LST_shapeFunctions
  from .LST_J import LST_J
  
  [dpsidxi, dpsideta] = LST_shapeDerivatives(xi, eta)

  Jinv = linalg.inv(LST_J(xElem, yElem, xi, eta))
  
  if (type2D == 'axisymmetric'):
    psi = LST_shapeFunctions(xi, eta)
    B = zeros((4, 12))
    for i in range(6):
      dpsidxy = Jinv @ array([dpsidxi[i], dpsideta[i]])
      B[0, 2*i  ] = dpsidxy[0]
      B[1, 2*i+1] = dpsidxy[1]
      B[2, 2*i  ] = psi[i] / (array(xElem) @ array(psi))
      B[3, 2*i  ] = dpsidxy[1]
      B[3, 2*i+1] = dpsidxy[0]
  else:
    B = zeros((3, 12))
    for i in range(6):
      dpsidxy = Jinv @ array([dpsidxi[i], dpsideta[i]])
      B[0, 2*i  ] = dpsidxy[0]
      B[1, 2*i+1] = dpsidxy[1]
      B[2, 2*i  ] = dpsidxy[1]
      B[2, 2*i+1] = dpsidxy[0]

  return array(B)
