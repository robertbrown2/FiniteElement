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

def CST_B(x1, x2, x3, y1, y2, y3):
  """
  Defines the B Matrix for a Constant Strain Triangle element.
  Usage: CST_B(x1, x2, x3, y1, y2, y3)
  Returns a 3x6 array.
  """
  from numpy import array, linalg
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

def get_color(val, min, max, colormap):
  """
  Defines the element color based on a colormap.
  Usage: get_color(val, min, max, colormap)
  Returns a color for matplotlib.pyplot
  """
  diff = max-min
  if (diff == 0):
    x = 0.5
  else:
    x = (val-min)/diff*1.0
  colorVal = colormap(float(x)) #scalarMap.to_rgba(x)
  return colorVal

def CST_plot(xList, yList, conn, u, sigmaMax, stressUnit="", lengthUnit="", cmapString="jet", scaling=None):
  """
  Plots a completed simulation using CST elements.
  Usage: CST_plot(xList, yList, conn, u, sigmaMax, stressUnit, lengthUnit, cmapString)
  xList - (array - nnode) list of x positions of nodes
  yList - (array - nnode) list of y positions of nodes
  conn  - (array - nElem by 3) connectivity array or list of lists.  Each "row" should have three nodes.
  u     - (array - nnode*2) solution to FEA problem - ordered [u1, v1, u2, v2 ...]
  sigmaMax - (array - nElem) Maximum stress on each node (this will color each element)
  stressUnit: (string) Stress unit for display in plot.  Typically "Pa" or "psi".  Defaults to ""
  lengthUnit: (string) Length unit for display in plot.  Typically "m" or "in".  Defaults to ""
  cmapString: (string) Name of desired colormap.  Defaults to "jet"
  scaling: (float) Factor used for displacement in plot.  If None, will be calculated in function.
  """
  from matplotlib import pyplot
  from matplotlib import cm
  from matplotlib import colors
  #from matplotlib import colorbar
  from matplotlib import figure
  from numpy import array, sqrt, floor, arange

  colormap=pyplot.get_cmap(cmapString)
  # must be defined: 
  # xList - list of x points [nNode]
  # yList - list of y points [nNode]
  # conn - connectivity of nodes to elements [nElem, 2]
  # u - deformation vector [nNode x 2]
  # sigmaMax - 

  # should be defined, but default values are available
  # stressUnit - 'Pa' or 'psi' (defaults to '')
  # lengthUnit - 'm' or 'in' (defaults to '')
  # colormap - try jet, plasma, viridis, cividis, or others

  # Set values for stressUnit, lengthUnit, and colormap if they are not defined

  fig = figure.Figure(figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')

  dxmax = max(xList)-min(xList)
  dymax = max(yList)-min(yList)
  rmax = sqrt(dxmax**2+dymax**2)
  if scaling == None:
    factor = max(floor(rmax/(25*max(u))), 1)
  else:
    factor = scaling
  for i, x in enumerate(xList):
    y = yList[i]
    pyplot.annotate(i+1, (x+.01*rmax, y))
  for i, nodes in enumerate(conn):
    i1 = nodes[0]-1
    i2 = nodes[1]-1
    i3 = nodes[2]-1
    xi1 = xList[i1]
    xi2 = xList[i2]
    xi3 = xList[i3]
    yi1 = yList[i1]
    yi2 = yList[i2]
    yi3 = yList[i3]
  
    line1,  = pyplot.plot([xi1, xi2, xi3, xi1], [yi1, yi2, yi3, yi1], 'o-k')
  for i, nodes in enumerate(conn):
    n1 = 2*nodes[0]-2
    n2 = 2*nodes[0]-1
    n3 = 2*nodes[1]-2
    n4 = 2*nodes[1]-1
    n5 = 2*nodes[2]-2
    n6 = 2*nodes[2]-1
    i1 = nodes[0]-1
    i2 = nodes[1]-1
    i3 = nodes[2]-1
    xi1 = xList[i1]
    xi2 = xList[i2]
    xi3 = xList[i3]
    yi1 = yList[i1]
    yi2 = yList[i2]
    yi3 = yList[i3]
    xdi1 = xList[i1] + u[n1]*factor
    xdi2 = xList[i2] + u[n3]*factor
    xdi3 = xList[i3] + u[n5]*factor
    ydi1 = yList[i1] + u[n2]*factor
    ydi2 = yList[i2] + u[n4]*factor
    ydi3 = yList[i3] + u[n6]*factor
    #X = Matrix([[xdi1, ydi1], [xdi2, ydi2], [xdi3, ydi3]])
    cval = get_color(sigmaMax[i], min(sigmaMax), max(sigmaMax), colormap)
    #cval = get_color(stress_VM[i], min(stress_VM), max(stress_VM))
    t1, = pyplot.fill([xdi1, xdi2, xdi3], [ydi1, ydi2, ydi3], color = cval)
  pyplot.xlabel('x ['+lengthUnit+']')
  pyplot.ylabel('y ['+lengthUnit+']')
  #legend([line1, line2], ['original', 'deformed x ' + str(factor)])
  #mshow(cmap='viridis')
  pyplot.text(min(xList)-.15*(dxmax), max(yList)+ (dymax)*.12, 'Deformation scaled by ' + str(int(factor)) + 'x', fontsize=8)
  pyplot.text(min(xList)+.35*(dxmax), max(yList)+ (dymax)*.12, 'Max stress = %8.3e ' % max(sigmaMax) + stressUnit, fontsize=8)
  pyplot.text(min(xList)+.85*(dxmax), max(yList)+ (dymax)*.12, 'Min stress = %8.3e ' % min(sigmaMax) + stressUnit, fontsize=8)

  nValues = arange(0, 30)
  cnorm = colors.Normalize(vmin = min(sigmaMax), vmax = max(sigmaMax))
  scmap = cm.ScalarMappable(norm=cnorm, cmap=colormap)
  scmap.set_array(nValues)
  cbar = pyplot.colorbar(scmap)
  cbar.set_label('Max element stress ['+stressUnit+']')
