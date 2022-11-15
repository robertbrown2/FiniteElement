def Q4_J(x1234, y1234, xi, eta):
  """
  Find the Jacobian for a quadrilateral element with four nodes.
  J = Q4_J(x1234, y1234, xi, eta)
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
  xi: (float) - location at which to calculate Jacobian
  eta: (float) - location at which to calculate Jacobian
  ----------
    Output
  ----------
  J: (2x2 array) - Jacobian matrix
  """
  from numpy import array
  from Q4.Q4_shapeFunctions import Q4_shapeDerivatives
  
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)

  # J = [[dx/dxi,  dy/dxi ],
  #      [dx/deta, dy/deta]]

  # x = x1 * psi1 + x2 * psi2 + x3 * psi3 + x4 * psi4

  dxdxi  =  array(x1234) @ array(dpsidxi)
  dxdeta =  array(x1234) @ array(dpsideta)
  dydxi  =  array(y1234) @ array(dpsidxi)
  dydeta =  array(y1234) @ array(dpsideta)

  J = array([[ dxdxi,  dydxi],
             [dxdeta, dydeta]])
  return J
