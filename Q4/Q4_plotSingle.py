def Q4_map(x1234, y1234, xi, eta):
  """
  Get the x and y location associated with xi and eta.  Primarily an internal 
  function for Q4_plot and Q4_plotSingle.
  """
  from .Q4_shapeFunctions import Q4_shapeFunctions
  psi = Q4_shapeFunctions(xi, eta)

  x = 0
  y = 0
  for i, p in enumerate(psi):
    x += p*x1234[i]
    y += p*y1234[i]
  
  return([x,y])

def Q4_plotSingle(x1234, y1234, u=None, D=None, minMax=None, output='VM', Nplot=10, 
                  colormap='jet', undeformedLines=True, deformedLines=True, scaling=1.0, type2D="planeStress"):
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
  from matplotlib.pyplot import contourf, plot
  from .Q4_stress import Q4_stress
  from .Q4_strain import Q4_strain

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
      elif (output == 'VM' or output == 'sigx' or output == 'sigy' or output == 'tauxy' or output == 'sig1' or output == 'sig2'):
        Z[i,j] = Q4_stress(x1234, y1234, u, xi[i,j], eta[i,j], D, type2D=type2D, output=output)
      elif (output == 'epsx' or output == 'epsy' or output == 'gammaxy'):
        eps = Q4_strain(x1234, y1234, u, xi[i,j], eta[i,j], type2D=type2D)
        if (output == 'epsx'):
          Z[i,j] = eps[0]
        elif (output == 'epsy'):
          Z[i,j] = eps[1]
        else:
          Z[i,j] = eps[2]
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
