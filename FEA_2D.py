from numpy import *

def CST_J(x1, x2, x3, y1, y2, y3):
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

def CST_B(x1, x2, x3, y1, y2, y3):
  # psi1 = 1 - xi - eta
  # psi2 = xi
  # psi3 = eta

  dpsi1dxi = -1
  dpsi2dxi = 1
  dpsi3dxi = 0
  dpsi1deta = -1
  dpsi2deta = 0
  dpsi3deta = 1
  
  J = CST_J(x1, x2, x3, y1, y2, y3)

  Jinv = linalg.inv(J)
  # -----------------------------------
  dpsi1dxieta = array([dpsi1dxi,
                       dpsi1deta])
  dpsi1dxy = Jinv @ dpsi1dxieta
  # -----------------------------------
  dpsi2dxieta = array([dpsi2dxi,
                       dpsi2deta])
  dpsi2dxy = Jinv @ dpsi2dxieta
  # -----------------------------------
  dpsi3dxieta = array([dpsi3dxi,
                       dpsi3deta])
  dpsi3dxy = Jinv @ dpsi3dxieta
  #print()
  #print('[dpsi1/dx, dpsi1/dy], [dpsi2/dx, dpsi2/dy], [dpsi3/dx, dpsi3/dy]')
  #print(dpsi1dxy, dpsi2dxy, dpsi3dxy)
  # -----------------------------------
  B = array([[dpsi1dxy[0],     0,       dpsi2dxy[0],     0,       dpsi3dxy[0],      0     ],
             [    0,       dpsi1dxy[1],     0,       dpsi2dxy[1],       0,     dpsi3dxy[1]],
             [dpsi1dxy[1], dpsi1dxy[0], dpsi2dxy[1], dpsi2dxy[0], dpsi3dxy[1], dpsi3dxy[0]]
            ])
  return B
