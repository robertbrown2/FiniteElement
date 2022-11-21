def LST_map(xElem, yElem, xi, eta):
  """
  Get the x and y location associated with xi and eta.  Primarily an internal 
  function for Q4_plot and Q4_plotSingle.
  """
  from .LST_shapeFunctions import LST_shapeFunctions
  
  psi = LST_shapeFunctions(xi, eta)
  
  x = 0
  y = 0
  
  for i, p in enumerate(psi):
    x += p*xElem[i]
    y += p*yElem[i]
  
  return([x,y])

def LST_plotSingle(xElem, yElem, u=None, D=None, minMax=None, output='VM', nPlot=10, 
                  colormap='jet', undeformedLines=True, deformedLines=True, scaling=1.0, type2D="planeStress"):
  """
  Plot a single quadrilateral element.
  Usage - fig = Q4_plotSingle(xElem, yElem, u=None, D=None, minMax=None, output='VM', Nplot=10, colormap='jet')
  ---------
    Input
  ---------
  xElem - (list) x locations of nodes
  yElem - (list) y locations of nodes
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
  from matplotlib import pyplot
  from matplotlib import tri
  from .LST_stress import LST_stress
  from .LST_strain import LST_strain
  from .LST_plotSingle import LST_plotSingle
  from .LST_J import LST_J
  
  # Get deformed node locations
  if (u != None):
    xd = []
    yd = []
    for i, x in enumerate(xElem):
      xd.append(x+scaling*u[2*i])
    for i, y in enumerate(yElem):
      yd.append(y+scaling*u[2*i+1])
  else:
    xd = xElem
    yd = yElem

  # Initialize mesh values
  X = []
  Y = []
  Z = []
  for i in range(0, nPlot+1):
    for j in range(0, i+1):
      xi = i/nPlot
      eta = 1-(j/nPlot)
      if (output == 'J'):
        Z.append(linalg.det(LST_J(xElem, yElem, xi, eta)))
      elif (output == 'VM' or output == 'sigx' or output == 'sigy' or output == 'tauxy' or output == 'sig1' or output == 'sig2'):
        Z.append(LST_stress(xElem, yElem, u, xi, eta, D, type2D=type2D, output=output))
      elif (output == 'epsx' or output == 'epsy' or output == 'gammaxy'):
        Z.append(LST_strain(xElem, yElem, u, xi, eta, type2D=type2D, output=output))
      else:
        print('Output type', output, ' not supported')
        raise Exception
      [xval, yval] = LST_map(xd, yd, xi, eta)
      Y.append(yval)
      X.append(xval)
  #triang = tri.Triangulation(X, Y)
  # Plot things
  if (undeformedLines):
    x=[xElem[0], xElem[1], xElem[2], xElem[0]]
    y=[yElem[0], yElem[1], yElem[2], yElem[0]]
    pyplot.plot(x, y, 'k--')
  if (deformedLines):
    pyplot.plot([xd[0], xd[5], xd[1], xd[3], xd[2], xd[4], xd[0]], 
         [yd[0], yd[5], yd[1], yd[3], yd[2], yd[4], yd[0]], 'k')

  if (minMax == None):
    return pyplot.gca().tricontourf(X, Y, Z, cmap=colormap)
  else:
    
    lenMinMax = len(minMax)
    if lenMinMax != 2:
      print('Warning: minMax (in C4_plot) should be a list of two values')

    return pyplot.gca().tricontourf(X, Y, Z, cmap=colormap, vmin=minMax[0], vmax=minMax[1], levels=10)
