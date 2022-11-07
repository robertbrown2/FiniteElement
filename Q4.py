def constMatrix(E, nu, type2D):
  """
  Create the constituitive matrix for a 2D solid.

  Usage - D = constMatrix(E, nu, type2D)

  ---------
    Input
  ---------
  E: (float) - Young's modulus of material
  nu: (float) - Poisson's ratio of material
  type2D: (string) - assumption for 2D solid
          'planeStress' - stress in z direction is zero (thin plates)
          'planeStrain' - strain in z direction is zero (thick bodies)

  ----------
    Output
  ----------
  D: (array) - constituitve matrix
  """

  if (type2D == 'planeStress'):
    D = E / (1 - nu**2) * array([
                             [1, nu, 0],
                             [nu, 1, 0],
                             [0, 0, (1-nu)/2]
                            ])
  elif (type2D == 'planeStrain'):
    D = E / ((1 + nu)*(1 - 2*nu)) * array([
          [1-nu, nu, 0 ],
          [nu, 1-nu, 0],
          [0, 0, (1-2*nu)/2]
          ])
  else:
    print('type2D must be either "planeStress" or "planeStrain", was instead: ', type2D)
    raise Exception

  return D

def Q4_shapeFunctions(xi, eta):
  """
  [psi1, psi2, psi3, psi4] = Q4_shapeFunctions(xi, eta)
  Return the shape function values at a given xi and eta.
  """
  psi1 = (1 - xi)*(1 - eta)/4
  psi2 = (1 + xi)*(1 - eta)/4
  psi3 = (1 + xi)*(1 + eta)/4
  psi4 = (1 - xi)*(1 + eta)/4
  
  return [psi1, psi2, psi3, psi4]


def Q4_shapeDerivatives(xi, eta):
  """
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)
  Find the derivatives of the shape functions with respect to xi and eta.
  
  """
  dpsidxi = []
  dpsideta = []
  dpsidx = []
  dpsidy = []

  dpsidxi.append(-(1 - eta)/4) #dpsi1/dxi
  dpsidxi.append( (1 - eta)/4) #dpsi2/dxi
  dpsidxi.append( (1 + eta)/4) #dpsi3/dxi
  dpsidxi.append(-(1 + eta)/4) #dpsi4/dxi

  dpsideta.append(-(1 - xi)/4) #dpsi1/deta
  dpsideta.append(-(1 + xi)/4) #dpsi2/deta
  dpsideta.append( (1 + xi)/4) #dpsi3/deta
  dpsideta.append( (1 - xi)/4) #dpsi4/deta

  return [dpsidxi, dpsideta]

def Q4_map(x1234, y1234, xi, eta):
  """
  Get the x and y location associated with xi and eta.  Primarily an internal 
  function for Q4_plot and Q4_plotSingle.
  """
  
  psi = Q4_shapeFunctions(xi, eta)

  x = 0
  y = 0
  for i, p in enumerate(psi):
    x += p*x1234[i]
    y += p*y1234[i]
  
  return([x,y])

def Q4_area(x1234, y1234):
  """
  Find the area of a quadrilateral.
  A = Q4_area(x1234, y1234)
  
  ---------
    Input
  ---------
  x1234: (list) - x values of nodes
  y1234: (list) - y values of nodes

  ----------
    Output
  ----------
  Area: (float) - area of quad
  """

  dx1 = x1234[2] - x1234[0]
  dx2 = x1234[3] - x1234[1]
  dy1 = y1234[2] - y1234[0]
  dy2 = y1234[3] - y1234[1]

  # area is 1/2 of cross product of [dx1, dy1] and [dx2, dy2]

  #|  i   j  k |
  #| dx1 dy1 0 | = k (dx1*dy2 - dy1*dx2)
  #| dx2 dy2 0 |

  return 0.5 * (dx1*dy2 - dy1*dx2)

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

def Q4_B(x1234, y1234, xi, eta):
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
  # psi1 = (1 - xi)*(1 - eta)/4
  # psi2 = (1 + xi)*(1 - eta)/4
  # psi3 = (1 + xi)*(1 + eta)/4
  # psi4 = (1 - xi)*(1 + eta)/4
  
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)

  Jinv = linalg.inv(Q4_J(x1234, y1234, xi, eta))

  dpsidx = [0]*4
  dpsidy = [0]*4
  B = zeros((3, 8))
  for i in range(4):
    dpsidxy = Jinv @ array([dpsidxi[i], dpsideta[i]])
    B[0, 2*i  ] = dpsidxy[0]
    B[1, 2*i+1] = dpsidxy[1]
    B[2, 2*i  ] = dpsidxy[1]
    B[2, 2*i+1] = dpsidxy[0]

  return array(B)

def Q4_strain(x1234, y1234, u, xi, eta):
  from numpy import array
  """
  Output the strain at a point in the quadrilateral.

  Usage: eps = array([epsx, epsy, tauxy]) = Q4_strain(x1234, y1234, u, xi, eta)
  ---------
    Input
  ---------
  x1234 - (list) x locations of nodes
  y1234 - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4]
  xi, eta - (float) location on unmapped element

  ----------
    Output
  ----------
  eps: (array) contains [epsx, epsy, tauxy]
  epsx: (float) normal strain in x direction
  epsy: (float) normal strain in y direction
  tauxy: (float) shear strain
  """

  B = Q4_B(x1234, y1234, xi, eta)
  return B @ array(u)
  
def Q4_stress(x1234, y1234, u, xi, eta, D, type2D='PlaneStress', output='VM'):
  """
  Calculate the stress on an element at the unmapped location (xi, eta).

  Usage - sigma = Q4_stress(x1234, y1234, u=None, xi, eta, D, output='VM')
  ---------
    Input
  ---------
  x1234 - (list) x locations of nodes
  y1234 - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4]
  xi - (float) position in unmapped element
  eta - (float) position in unmapped element
  D - (array) constituitive matrix
  type2D - (string) simplifying assumption for 2D solid
  output - (string) Plot type:
      'VM' - von Mises stress
      'sigx', 'sigy', or 'tauxy' - normal stress in x or y, or shear stress
      'sig1' or 'sig2' - maximum or minimum principal stress

  ----------
    Output
  ----------
  sigma: (float) stress of requested type
  """
  from numpy import array, sqrt

  eps = array(Q4_strain(x1234, y1234, u, xi, eta))
  sigxy = D @ eps
  if (output == 'sigx'):
    return sigxy[0]
  elif (output == 'sigy'):
    return sigxy[1]
  elif (output == 'tauxy'):
    return sigxy[2]
  else:
    sigx = sigxy[0]
    sigy = sigxy[1]
    tauxy = sigxy[2]
    sig1 = (sigx + sigy)/2 + sqrt((sigx - sigy)**2/2 + tauxy**2)
    sig2 = (sigx + sigy)/2 - sqrt((sigx - sigy)**2/2 + tauxy**2)
    if (type2D == 'planeStrain'):
      sig3 = nu*E/((1+nu)*(1-2*nu)) * (eps[0]+eps[1])
    else:
      sig3 = 0
    if (output == 'sig1'):
      return sig1
    elif (output == 'sig2'):
      return sig2
    elif (output == 'VM'):
      return sqrt(1/2)*sqrt((sig1-sig2)**2 + (sig2-sig3)**2 + (sig3-sig1)**2)
    else:
      print('Variable output in Q4_stress must be sigx, sigy, tauxy, sig1, sig2, or VM')
      raise Exception

def Q4_stiffness(x1234, y1234, xi, eta, D, thickness):
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
  B = Q4_B(x1234, y1234, xi, eta)
  return Q4_area(x1234, y1234)*thickness*(transpose(B)@D@B)

def Q4_plotSingle(x1234, y1234, u=None, D=None, minMax=None, output='VM', Nplot=10, 
                  colormap='jet', undeformedLines=True, deformedLines=True, scaling=1.0):
  """
  Plot a single quadrilateral element.
  Usage - fig = Q4_plotSingle(x1234, y1234, u=None, D=None, minMax=None, output='VM', Nplot=10, colormap='jet')
  ---------
    Input
  ---------
  x1234 - (list) x locations of nodes
  y1234 - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4]
  minMax - (list) min and max value of output plot
  D - (array) constituitive matrix
  output - (string) Plot type:
      'VM' - von Mises stress
      'sigx', 'sigy', or 'tauxy' - normal stress in x or y, or shear stress
      'sig1' or 'sig2' - maximum or minimum principal stress
       'J' - determinant of Jacobian matrix
  Nplot - number of points to plot in contour
  colormap - (string) name of colormap
  undeformedLines - (logical) if True, display undeformed lines
  deformedLines - (logical) if True, display deformed lines
  scaling - (float) Ratio of displayed deformation to actual deformation
  """
  from numpy import linalg, meshgrid, linspace, zeros, shape
  from matplotlib.pyplot import contourf

  # Get deformed node locations
  if (u != None):
    xd = []
    yd = []
    for i, x in enumerate(x1234):
      xd.append(x+scaling*u[2*i])
    for i, y in enumerate(y1234):
      yd.append(y+scaling*u[2*i+1])
  else:
    xd = x1234
    yd = y1234

  # Initialize meshgrid values
  [xi, eta] = meshgrid(linspace(-1, 1, Nplot), linspace(-1, 1, Nplot))
  Z = zeros(shape(xi))
  X = zeros(shape(xi))
  Y = zeros(shape(xi))
  
  # Calculate plot values and locations
  for i in range(Nplot):
    for j in range(Nplot):
      if (output == 'J'):
        Z[i,j] = linalg.det(Q4_J(x1234, y1234, xi[i,j], eta[i,j]))
      elif (output == 'VM'):
        Z[i,j] = Q4_stress(x1234, y1234, u, xi[i,j], eta[i,j], D, type2D='PlaneStress', output='VM')
      else:
        print('Output type', output, ' not supported')
        raise Exception
      [X[i,j], Y[i,j]] = Q4_map(xd, yd, xi[i,j], eta[i,j])
  
  # Plot things
  if (undeformedLines):
    x=x1234.copy()
    x.append(x1234[0])
    y=y1234.copy()
    y.append(y1234[0])
    plot(x, y, 'k--')
  if (deformedLines):
    x=xd.copy()
    x.append(xd[0])
    y=yd.copy()
    y.append(yd[0])
    plot(x, y, 'k')

  if (minMax == None):
    return contourf(X, Y, Z, cmap=colormap)
  else:
    
    lenMinMax = len(minMax)
    if lenMinMax != 2:
      print('Warning: minMax (in C4_plot) should be a list of two values')

    return contourf(X, Y, Z, cmap=colormap, vmin=minMax[0], vmax=minMax[1], levels=10)
