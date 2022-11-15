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
  elif (type2D == 'axisymmetric'):
    D = E / ((1 + nu)*(1 - 2*nu)) * array([
                             [1-nu, nu, nu, 0],
                             [nu, 1-nu, nu, 0],
                             [nu, nu, 1-nu, 0],
                             [0, 0, 0, (1-2*nu)/2]
                            ])
  else:
    print('type2D must be "planeStress", "planeStrain", or "axisymmetric".  Was instead: ', type2D)
    raise Exception

  return D

def LST_midpoints(x123, y123):
  xbar = sum(x123)/3
  ybar = sum(y123)/3
  x456 = []
  y456 = []
  for i in range(3):
    dx = xbar - x123[i]
    dy = ybar - y123[i]
    x456.append(xbar + 0.5*dx)
    y456.append(ybar + 0.5*dy)
  
  return [x456, y456]

def LST_shapeFunctions(xi, eta):
  """
  [psi1, psi2, psi3, psi4, psi5, psi6] = LST_shapeFunctions(xi, eta)
  Return the shape function values at a given xi and eta.
  """
  psi1 = 1 - 3*xi - 3*eta + 2*xi**2 + 4*xi*eta + 2*eta**2
  psi2 = -xi + 2*xi**2
  psi3 = -eta + 2*eta**2
  psi4 = 4*xi*eta
  psi5 = 4*eta - 4*eta**2 - 4*xi*eta
  psi6 = 4*xi - 4*xi**2 - 4*xi*eta
  
  return [psi1, psi2, psi3, psi4, psi5, psi6]


def LST_shapeDerivatives(xi, eta):
  """
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)
  Find the derivatives of the shape functions with respect to xi and eta.
  
  """
  dpsidxi = []
  dpsideta = []
  dpsidx = []
  dpsidy = []

  dpsidxi.append(-3 + 4*xi + 4*eta) #dpsi1/dxi
  dpsidxi.append(4*xi - 1) #dpsi2/dxi
  dpsidxi.append(0) #dpsi3/dxi
  dpsidxi.append(4*eta) #dpsi4/dxi
  dpsidxi.append(-4*eta)
  dpsidxi.append(4 - 8*xi - 4*eta)

  dpsideta.append(-3 + 4*xi + 4*eta) #dpsi1/deta
  dpsideta.append(0) #dpsi2/deta
  dpsideta.append(4*eta - 1) #dpsi3/deta
  dpsideta.append(4*xi) #dpsi4/deta
  dpsideta.append(4 - 8*eta - 4*xi)
  dpsideta.append(-4*xi)

  return [dpsidxi, dpsideta]

def LST_map(x123, y123, xi, eta):
  """
  Get the x and y location associated with xi and eta.  Primarily an internal 
  function for Q4_plot and Q4_plotSingle.
  """
  if (len(x123) == 3:
    [x456, y456] = LST_midpoints(x123, y123)
    xnodes = x123 + x456
    ynodes = y123 + y456
  else:
    xnodes = x123
    ynodes = y123
  
  psi = LST_shapeFunctions(xi, eta)
  
  x = 0
  y = 0
  
  for i, p in enumerate(psi):
    x += p*xnodes[i]
    y += p*ynodes[i]
  
  return([x,y])

def LST_area(x123, y123):
  """
  Find the area of a triangle.
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

  dx1 = x123[1] - x123[0]
  dx2 = x123[2] - x123[0]
  dy1 = y123[1] - y123[0]
  dy2 = y123[2] - y123[0]

  # area is 1/2 of cross product of [dx1, dy1] and [dx2, dy2]

  #|  i   j  k |
  #| dx1 dy1 0 | = k (dx1*dy2 - dy1*dx2)
  #| dx2 dy2 0 |

  return 0.5 * (dx1*dy2 - dy1*dx2)

def LST_J(x123, y123, xi, eta):
  """
  Find the Jacobian for a triangular element with six nodes.
  J = Q4_J(x123, y123, xi, eta)

  3
  | \
  |   \
  |     \
  |       \
  1 ------  2 

  ---------
    Input
  ---------
  x123: (list) - x values of nodes
  y123: (list) - y values of nodes
  xi: (float) - location at which to calculate Jacobian
  eta: (float) - location at which to calculate Jacobian

  ----------
    Output
  ----------
  J: (2x2 array) - Jacobian matrix
  """
  from numpy import array
  
  [dpsidxi, dpsideta] = LST_shapeDerivatives(xi, eta)

  # J = [[dx/dxi,  dy/dxi ],
  #      [dx/deta, dy/deta]]

  # x = x1 * psi1 + x2 * psi2 + x3 * psi3 + x4 * psi4
  [x456, y456] = LST_midpoints(x123, y123)
  xnodes = x123 + x456
  ynodes = y123 + y456
  
  dxdxi  =  array(xnodes) @ array(dpsidxi)
  dxdeta =  array(xnodes) @ array(dpsideta)
  dydxi  =  array(ynodes) @ array(dpsidxi)
  dydeta =  array(ynodes) @ array(dpsideta)

  J = array([[ dxdxi,  dydxi],
             [dxdeta, dydeta]])
  return J

def LST_B(x123, y123, xi, eta, type2D='planeStress'):
  """
  Find the B Matrix for a triangular element with six nodes.
  B = Q4_B(x123, y123, xi, eta, type2D)

  ---------
    Input
  ---------
  x123: (list) - x values of nodes
  y123: (list) - y values of nodes
  xi: (float) - location at which to calculate B matrix
  eta: (float) - location at which to calculate B matrix

  ----------
    Output
  ----------
  B: (3x12 array) - B matrix
  """
  from numpy import array, linalg, zeros
  
  [dpsidxi, dpsideta] = LST_shapeDerivatives(xi, eta)

  
  [x456, y456] = LST_midpoints(x123, y123)
  xnodes = x123 + x456
  ynodes = y123 + y456
  Jinv = linalg.inv(LST_J(xnodes, ynodes, xi, eta))
  
  if (type2D == 'axisymmetric'):
    psi = LST_shapeFunctions(xi, eta)
    B = zeros((4, 12))
    for i in range(6):
      dpsidxy = Jinv @ array([dpsidxi[i], dpsideta[i]])
      B[0, 2*i  ] = dpsidxy[0]
      B[1, 2*i+1] = dpsidxy[1]
      B[2, 2*i  ] = psi[i] / (array(xnodes) @ array(psi))
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

def LST_strain(x123, y123, u, xi, eta, type2D, output=None):
  from numpy import array
  """
  Output the strain at a point in the triangle.

  Usage: eps = array([epsx, epsy, tauxy]) = LST_strain(x123, y123, u, xi, eta)
  ---------
    Input
  ---------
  x123 - (list) x locations of nodes
  y123 - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4, u5, v5, u6, v6]
  xi, eta - (float) location on unmapped element

  ----------
    Output
  ----------
  eps: (array) contains [epsx, epsy, tauxy]
  epsx: (float) normal strain in x direction
  epsy: (float) normal strain in y direction
  tauxy: (float) shear strain
  """

  B = LST_B(x123, y123, xi, eta, type2D)
  eps = B @ array(u)
  if (output == None):
    return eps
  elif (output == 'epsx'):
    return eps[0]
  elif (output == 'epsy'):
    return eps[1]
  elif (output == 'gammaxy'):
    return eps[2]
  else:
    print('Error in Q4_strain: output not recognized')
    raise Exception
  
def LST_stress(x123, y123, u, xi, eta, D, type2D='PlaneStress', output='VM'):
  """
  Calculate the stress on an element at the unmapped location (xi, eta).

  Usage - sigma = LST_stress(x123, y123, u=None, xi, eta, D, output='VM')
  ---------
    Input
  ---------
  x123 - (list) x locations of nodes
  y123 - (list) y locations of nodes
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

  eps = array(LST_strain(x123, y123, u, xi, eta, type2D))
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

def LST_stiffness(x123, y123, xi, eta, D, thickness=None, type2D='planeStress'):
  """
  Calculate the stiffness matrix for a Q4 element

  Usage - K = Q4_stiffness(x123, y123, xi, eta, D, thickness)

  ---------
    Input
  ---------
  x123 - (list) x locations of nodes
  y123 - (list) y locations of nodes
  xi - (float) position in unmapped element
  eta - (float) position in unmapped element
  D - (array) constituitive matrix
  thickness - (float) thickness of element in third dimension
  """
  from numpy import array
  B = LST_B(x123, y123, xi, eta, type2D)
  if (type2D == 'axisymmetric'):
    psi = LST_shapeFunctions(xi, eta)
    thickness = 2*pi*(array(x1234) @ array(psi))
  Area = linalg.det(LST_J)
  return Area*thickness*(transpose(B)@D@B)

def LST_plotSingle(x123, y123, u=None, D=None, minMax=None, output='VM', Nplot=10, 
                  colormap='jet', undeformedLines=True, deformedLines=True, scaling=1.0, type2D="planeStress"):
  """
  Plot a single quadrilateral element.
  Usage - fig = Q4_plotSingle(x1234, y1234, u=None, D=None, minMax=None, output='VM', Nplot=10, colormap='jet')
  ---------
    Input
  ---------
  x123 - (list) x locations of nodes
  y123 - (list) y locations of nodes
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
  from matplotlib.pyplot import contourf, plot

  [x456, y456] = LST_midpoints(x123, y123)
  xnodes = x123 + x456
  ynodes = y123 + y456
  
  # Get deformed node locations
  if (u != None):
    xd = []
    yd = []
    for i, x in enumerate(xnodes):
      xd.append(x+scaling*u[2*i])
    for i, y in enumerate(ynodes):
      yd.append(y+scaling*u[2*i+1])
  else:
    xd = xnodes
    yd = ynodes

  # Initialize meshgrid values
  # TODO Fix this
  [xi, eta] = meshgrid(linspace(-1, 1, Nplot), linspace(-1, 1, Nplot))
  Z = zeros(shape(xi))
  X = zeros(shape(xi))
  Y = zeros(shape(xi))
  
  # Calculate plot values and locations
  for i in range(Nplot):
    for j in range(Nplot):
      if (output == 'J'):
        Z[i,j] = linalg.det(LST_J(x123, y123, xi[i,j], eta[i,j]))
      elif (output == 'VM' or output == 'sigx' or output == 'sigy' or output == 'tauxy' or output == 'sig1' or output == 'sig2'):
        Z[i,j] = LST_stress(x123, y123, u, xi[i,j], eta[i,j], D, type2D=type2D, output=output)
      elif (output == 'epsx' or output == 'epsy' or output == 'gammaxy'):
        eps = LST_strain(x123, y123, u, xi[i,j], eta[i,j], type2D=type2D)
        if (output == 'epsx'):
          Z[i,j] = eps[0]
        elif (output == 'epsy'):
          Z[i,j] = eps[1]
        else:
          Z[i,j] = eps[2]
      else:
        print('Output type', output, ' not supported')
        raise Exception
      [X[i,j], Y[i,j]] = LST_map(xd, yd, xi[i,j], eta[i,j])
  
  # Plot things
  if (undeformedLines):
    x=x123.copy()
    x.append(x123[0])
    y=y123.copy()
    y.append(y123[0])
    plot(x, y, 'k--')
  if (deformedLines):
    plot([xd[0], xd[5], xd[1], xd[3], xd[2], xd[4], xd[0]], 
         [yd[0], yd[5], yd[1], yd[3], yd[2], yd[4], yd[0]], 'k')

  if (minMax == None):
    return contourf(X, Y, Z, cmap=colormap)
  else:
    
    lenMinMax = len(minMax)
    if lenMinMax != 2:
      print('Warning: minMax (in C4_plot) should be a list of two values')

    return contourf(X, Y, Z, cmap=colormap, vmin=minMax[0], vmax=minMax[1], levels=10)


def Q4_plot(conn, xnode, ynode, u=None, D=None, type2D="planeStress", output="J", scaling=None, minMax=None, Nplot=10, 
                  colormap='jet', undeformedLines=True, deformedLines=True):
  """
  Plot the entire 2D solid.  Defaults to plotting the determinant of the Jacobian on the undeformed mesh.
  Usage (Jacobian) - plotAll(conn, xnode, ynode)
  Usage (Solution) - plotAll(conn, xnode, ynode, u, D, type2D="planeStress", output="J")
  
  ---------
    Input
  ---------
  conn - (list of lists) connectivity matrix - [[n1, n2, n3, n4], [n5, n6, n7, n8], ...]
  xnode - (list) x locations of nodes
  ynode - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4, ...]
  D - (array) constituitive matrix - should match type2D
  type2D - (string) "planeStress", "planeStrain", or "axisymmetric"
  minMax - (list) min and max value of output plot - omit to have min/max automatically calculated
  output - (string) Plot type:
      'VM' - von Mises stress
      'sigx', 'sigy', or 'tauxy' - normal stress in x or y, or shear stress
      'sig1' or 'sig2' - maximum or minimum principal stress
       'J' - determinant of Jacobian matrix
  Nplot - number of points to plot in contour
  colormap - (string) name of colormap
  undeformedLines - (logical) if True, display undeformed lines
  deformedLines - (logical) if True, display deformed lines - set to False if u is not given
  scaling - (float) Ratio of displayed deformation to actual deformation - choose None for automatic scaling
  """
  from matplotlib import pyplot
  from matplotlib import cm
  from matplotlib import colors
  #from matplotlib import colorbar
  from matplotlib import figure
  from numpy import sqrt, floor, arange
  
  if (len(u) < 2):
    deformedLines=False
  if (minMax == None):
    calcMinMax = True
  
  # Determine Scaling valued
  dxMax = max(xnode) - min(xnode) # these are used for text placement as well
  dyMax = max(ynode) - min(ynode)
  if (len(u) < 2):
    scaling = 1.0
  elif (scaling == None):
    rMax = sqrt(dxMax**2 + dyMax**2)
    uMax = max(max(u), abs(min(u)))
    scaling = max(floor(rMax/(25*uMax)), 1)
  
  if (calcMinMax):
    for nodes in conn:
      # Find the x and y position of nodes for the local element
      x1234 = [xnode[nodes[0]-1], xnode[nodes[1]-1], xnode[nodes[2]-1], xnode[nodes[3]-1]] 
      y1234 = [ynode[nodes[0]-1], ynode[nodes[1]-1], ynode[nodes[2]-1], ynode[nodes[3]-1]]
    
      # Define deformation vector for local element
      if (len(u) < 2):
        uElem = None
      else:
        uElem = []
        for node in nodes:
          uElem.append(u[node*2-2])
          uElem.append(u[node*2-1])
    
      # Calculate the stress at the nodes of the local element
      if (output[0] == 's' or output[0]=='t'):
        sigA = Q4_stress(x1234, y1234, uElem, -1, -1, D, type2D, output)
        sigB = Q4_stress(x1234, y1234, uElem,  1, -1, D, type2D, output)
        sigC = Q4_stress(x1234, y1234, uElem,  1,  1, D, type2D, output)
        sigD = Q4_stress(x1234, y1234, uElem, -1,  1, D, type2D, output)
      else:
        sigA = Q4_strain(x1234, y1234, uElem, -1, -1, type2D, output)
        sigB = Q4_strain(x1234, y1234, uElem,  1, -1, type2D, output)
        sigC = Q4_strain(x1234, y1234, uElem,  1,  1, type2D, output)
        sigD = Q4_strain(x1234, y1234, uElem, -1,  1, type2D, output)
      if (minMax == None):
        minMax=[0, 0]
        minMax[0] = min(sigA, sigB, sigC, sigD)
        minMax[1] = max(sigA, sigB, sigC, sigD)
      else:
        minMax[0] = min(sigA, sigB, sigC, sigD, minMax[0])
        minMax[1] = max(sigA, sigB, sigC, sigD, minMax[1])
  
  fig = figure.Figure(figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
  
  for nodes in conn:
    # Find the x and y position of nodes for the local element
    x1234 = [xnode[nodes[0]-1], xnode[nodes[1]-1], xnode[nodes[2]-1], xnode[nodes[3]-1]] 
    y1234 = [ynode[nodes[0]-1], ynode[nodes[1]-1], ynode[nodes[2]-1], ynode[nodes[3]-1]]
  
    # Define deformation vector for local element
    if (len(u) < 2):
      uElem = None
    else:
      uElem = []
      for node in nodes:
        uElem.append(u[node*2-2])
        uElem.append(u[node*2-1])
          
    Q4_plotSingle(x1234, y1234, uElem, D, minMax, output, Nplot, 
                  colormap, undeformedLines, deformedLines, scaling, type2D=type2D)
  #pyplot.xlabel('x')
  #pyplot.ylabel('y')
  if (output != 'J'):
    xMax = xnode[0]
    xMin = xnode[0]
    yMax = ynode[0]
    yMin = ynode[0]
    
    # Find bounds of plot to help place text
    for i, x in enumerate(xnode):
      xd = xnode[i] + u[2*i]*scaling
      yd = ynode[i] + u[2*i+1]*scaling
      xMax = max(xMax, xd, xnode[i])
      xMin = min(xMin, xd, xnode[i])
      yMax = max(yMax, yd, ynode[i])
      yMin = min(yMin, yd, ynode[i])
    xAvg = (xMax + xMin)/2
    dx = xMax - xMin
    dy = yMax - yMin
    pyplot.text(xAvg - .6*(dx), yMin - (dy)*.15, 'Deformation scaled by ' + str(int(scaling)) + 'x', fontsize=8)
    pyplot.text(xAvg - .05*(dx), yMin - (dy)*.15, 'Max stress = %8.3e ' % minMax[1], fontsize=8)
    pyplot.text(xAvg + .4*(dx), yMin - (dy)*.15, 'Min stress = %8.3e ' % minMax[0], fontsize=8)
  
  # Create colorbar
  nValues = arange(0, 30)
  cnorm = colors.Normalize(vmin = minMax[0], vmax = minMax[1])
  scmap = cm.ScalarMappable(norm=cnorm, cmap=colormap)
  scmap.set_array(nValues)
  cbar = pyplot.colorbar(scmap)
  
  # Label colorbar
  if (output == 'VM'):
    cbar.set_label('Von Mises stress')
  elif (output == 'J'):
    cbar.set_label('Determinant of Jacobian')
  elif (output == 'sigx'):
    cbar.set_label('Normal stress - x')
  elif (output == 'sigy'):
    cbar.set_label('Normal stress - y')
  elif (output == 'tauxy'):
    cbar.set_label('Shear stress - xy')
  elif (output == 'sig1'):
    cbar.set_label('Max normal stress')
  elif (output == 'sig2'):
    cbar.set_label('Min normal stress')