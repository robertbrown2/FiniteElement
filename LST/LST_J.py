def LST_J(xElem, yElem, xi, eta):
  """
  Find the Jacobian for a triangular element with six nodes.
  J = LST_J(xElem, yElem, xi, eta)
  3
  | \
  |   \
  |     \
  |       \
  1 ------  2 
  ---------
    Input
  ---------
  xElem: (list) - x values of nodes
  yElem: (list) - y values of nodes
  xi: (float) - location at which to calculate Jacobian
  eta: (float) - location at which to calculate Jacobian
  ----------
    Output
  ----------
  J: (2x2 array) - Jacobian matrix
  """
  from numpy import array
  from .LST_shapeFunctions import LST_shapeDerivatives
  
  [dpsidxi, dpsideta] = LST_shapeDerivatives(xi, eta)

  # J = [[dx/dxi,  dy/dxi ],
  #      [dx/deta, dy/deta]]

  # x = x1 * psi1 + x2 * psi2 + x3 * psi3 + x4 * psi4
  
  dxdxi  =  array(xElem) @ array(dpsidxi)
  dxdeta =  array(xElem) @ array(dpsideta)
  dydxi  =  array(yElem) @ array(dpsidxi)
  dydeta =  array(yElem) @ array(dpsideta)

  J = array([[ dxdxi,  dydxi],
             [dxdeta, dydeta]])
  return J
