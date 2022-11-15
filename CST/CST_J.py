def CST_J(x1, x2, x3, y1, y2, y3):
  """
  Defines the Jacobian for a Constant Strain Triangle element.
  Usage: CST_J(x1, x2, x3, y1, y2, y3)
  Returns a 2x2 array.
  """
  from numpy import array
  # psi1 = 1 - xi - eta
  # psi2 = xi
  # psi3 = eta
  
  dpsi1dxi = -1
  dpsi2dxi = 1
  dpsi3dxi = 0
  dpsi1deta = -1
  dpsi2deta = 0
  dpsi3deta = 1

  # J = [[dx/dxi,  dy/dxi ],
  #      [dx/deta, dy/deta]]

  # x = x1 * psi1 + x2 * psi2 + x3 * psi3

  dxdxi  =  dpsi1dxi * x1 +  dpsi2dxi * x2 +  dpsi3dxi * x3
  dxdeta = dpsi1deta * x1 + dpsi2deta * x2 + dpsi3deta * x3
  dydxi  =  dpsi1dxi * y1 +  dpsi2dxi * y2 +  dpsi3dxi * y3
  dydeta = dpsi1deta * y1 + dpsi2deta * y2 + dpsi3deta * y3

  J = array([[ dxdxi,  dydxi],
             [dxdeta, dydeta]])
  return J
