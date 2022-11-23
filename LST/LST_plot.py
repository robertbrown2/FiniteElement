def appendTriangles(plotTri, elemTri):
  from numpy import array
  
  
  maxNode = -1
  for tri in plotTri:
    maxNode = max(max(tri), maxNode)
  elemTri += maxNode + 1
  outputTri = concatenate((plotTri, elemTri))
  return outputTri

def LST_plot(conn, xnode, ynode, u=None, D=None, type2D="planeStress", output="J", scaling=None, minMax=None, nPlot=10, 
                  colormap='jet', undeformedLines=True, deformedLines=True, nodeNumbers=True):
  """
  Plot the entire 2D solid.  Defaults to plotting the determinant of the Jacobian on the undeformed mesh.
  Usage (Jacobian) - plotAll(conn, xnode, ynode)
  Usage (Solution) - plotAll(conn, xnode, ynode, u, D, type2D="planeStress", output="J")
  
  ---------
    Input
  ---------
  conn - (list of lists) connectivity matrix - [[n1, n2, ...], [n5, n6, ...], ...]
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
  from matplotlib import tri
  from numpy import sqrt, floor, arange, linspace, array
  from .LST_stress import LST_stress
  from .LST_strain import LST_strain
  from ..common.helpers import connIndex
  from .LST_plotSingle import LST_plotSingle
  
  if (len(u) < 2):
    deformedLines=False
  
  index = connIndex(conn)
  
  # Determine Scaling value
  dxMax = max(xnode) - min(xnode) # these are used for text placement as well
  dyMax = max(ynode) - min(ynode)
  if (len(u) < 2):
    scaling = 1.0
  elif (scaling == None):
    rMax = sqrt(dxMax**2 + dyMax**2)
    uMax = max(max(u), abs(min(u)))
    scaling = max(floor(rMax/(25*uMax)), 1)
  
  fig = figure.Figure(figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
  Xall = []
  Yall = []
  Zall = []
  plotTriangles = []
  for nodes in conn:
    # Find the x and y position of nodes for the local element
    xElem = []
    yElem = []
    for node in nodes:
      xElem.append(xnode[node-index])
      yElem.append(ynode[node-index])
  
    # Define deformation vector for local element
    if (len(u) < 2):
      uElem = None
    else:
      uElem = []
      for node in nodes:
        uElem.append(u[node*2-2])
        uElem.append(u[node*2-1])
          
    [X, Y, Z] = LST_plotSingle(xElem, yElem, uElem, D, minMax, output, nPlot, 
                  colormap, undeformedLines, deformedLines, scaling, type2D=type2D)
    triang = tri.Triangulation(X, Y)
    elemTriangles = triang.triangles
    plotTriangles = appendTriangles(plotTriangles, elemTriangles)
    Xall += X
    Yall += Y
    Zall += Z
  #pyplot.xlabel('x')
  #pyplot.ylabel('y')
  if (minMax==None):
    minMax = [min(Zall), max(Zall)]
    
  pyplot.tricontourf(Xall, Yall, Zall, triangles=plotTriangles, vmin=minMax[0], vmax=minMax[1], levels=linspace(minMax[0], minMax[1], 20), cmap=colormap)
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
    pyplot.text(xAvg - .05*(dx), yMin - (dy)*.15, 'Max stress = %8.3e ' % max(Zall), fontsize=8)
    pyplot.text(xAvg + .4*(dx), yMin - (dy)*.15, 'Min stress = %8.3e ' % min(Zall), fontsize=8)
  if (nodeNumbers):
    for i in range(len(xnode)):
      pyplot.text(xnode[i]+.1, ynode[i]+.1, str(i+index))
  # Create colorbar
  nValues = arange(0, 30)

  if (minMax != None):

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
