from numpy import sqrt, floor, linspace, arange, arctan2, sin, cos
from matplotlib.pyplot import figure, plot, annotate, text, Normalize, colorbar, xlabel, ylabel
from matplotlib.cm import jet, viridis, cividis, ScalarMappable

def find_min_index(conn):
  """
  Usage - find_min_index(conn)
  Determine the minimum index in a list of lists
  input - conn (list of lists)
  output - minval (integer, usually 0 or 1)
  """
  minval = 100
  for elem in conn:
    for node in elem:
      if node < minval:
        minval = node
  return minval

def get_color(i, sigmaMax, colormap):
  """
  Usage - get_color(i, sigmaMax, colormap)
  Convert a value (sigmaMax[i]) to a percentage value between
  the provided min and max values.
  If sigmaMax[i] = min(sigmaMax), output will be 0.
  If sigmaMax[i] = max(sigmaMax), output will be 1.
  """
  if max(sigmaMax) == None:
    return colormap(0)
  val = sigmaMax[i]
  smax = max(sigmaMax)
  smin = min(sigmaMax)
  diff = smax-smin
  x = (val-smin)/diff*1.0
  colorVal = colormap(float(x)) #scalarMap.to_rgba(x)
  return colorVal

def convXiEta(theta, x0, y0, xd):
  """
  Usage - convXiEta(theta, x0, y0, xd)
  Converts values from x and y (globa) coordinates to
  xi and eta (local) coordinates.
  Input: theta - angle formed by endpoints compared to x-axis
         x0 - x position of first node in element
         y0 - y position of first node in element
         xd - deformed position and rotation of nodes:
               [x1, x2, y1, y2, th1, th2]
  Output: xi1, xi2 - deformed xi locations of nodes (local)
                   - scaled such that undeformed xi values are 0 and L
          eta1, eta2 - deformed eta locations of nodes (local)
  """
  xp1 = xd[0]-x0
  yp1 = xd[2]-y0
  xp2 = xd[1]-x0
  yp2 = xd[3]-y0
  C = cos(theta)
  S = sin(theta)
  xi1 = xp1*C + yp1*S
  eta1 = yp1*C - xp1*S
  xi2 = xp2*C + yp2*S
  eta2 = yp2*C - xp2*S
  return xi1, eta1, xi2, eta2

def convXY(theta, x0, y0, xip, etap):
  """
  Usage - convXY(theta, x0, y0, xip, etap)
  Convert list of xi and eta points to x and y.
  input: theta - undeformed angle in global frame
         x0, y0 - x and y position of first node in global frame
         xip, etap - xi and eta values of points for plotting
  output: xp, yp - x and y values of points for plotting
  """
  C = cos(theta)
  S = sin(theta)
  xpp = xip*C - etap*S
  ypp = etap*C + xip*S
  xp = xpp + x0
  yp = ypp + y0
  return xp, yp

def beam_shape(xud, xd, np):
  """
  Usage - beam_shape(xud, xd, np)
  Takes undeformed and deformed nodal values and returns
  beam shape for plotting in global coordinates.
  input: xud - undeformed nodal values [x1, x2, y1, y2]
         xd  - deformed nodal values, including rotation
               [xd1, xd2, yd1, yd2, th1, th2]
         np  - number of points for plotting
  output: x and y points for plotting
  """
  dx = xud[1]-xud[0]
  dy = xud[3]-xud[2]
  theta = arctan2(dy, dx)
  L = sqrt(dx**2+dy**2)

  # convert deformed shape to xi and eta coordinates
  xi1, eta1, xi2, eta2 = convXiEta(theta, xud[0], xud[2], xd)
  th1 = xd[4]
  th2 = xd[5]
  x = linspace(0, 1, num=np)
  xip = xi1*(1-x) + xi2*(x)
  psi1 = 2*x**3-3*x**2+1
  psi2 = -2*x**3+3*x**2
  psi3 = x**3-2*x**2+x
  psi4 = x**3-x**2
  etap = eta1*psi1 + eta2*psi2 + th1*psi3 + th2*psi4
  #thp = eta1*(6*x**2-6*x)+eta2*(-6*x**2+6*x)+th1*(3*x**2-4*x+1)+th2*(4*x**2-2*x)

  return convXY(theta, xud[0], xud[2], xip, etap)

# ------------------------------
# Plotting starts here
# ------------------------------

def framePlot(conn, xList, yList, u=[None], sigmaMax=[None],
               colormap=jet, stressUnit='Pa', lengthUnit='m', plotType='frame'):
  """
  Usage - framePlot(conn, xList, yList, u=[None], sigmaMax=[None],
               colormap=jet, stressUnit='Pa', lengthUnit='m', type='frame')
  Input: conn - Connectivity matrix.
                List of nElem lists, each of which has 2 node numbers
         xList - list of x locations of nodes
         yList - list of y locations of nodes
         u - list of deformation values.  
             Should have 2 x nNode values for trusses and 3 x nNode for beams
             Order is [u, v] for trusses and [u, v, phi] for beams.
         sigmaMax - list of max compressive/tensile stress for each element (nElem long)
         colormap - can be jet, viridis, or cividis
         stressUnit - unit used for stress values on plot
         lengthUnit - unit used for length values on plot
         plotType - 'frame' or 'truss'
  """

  if max(sigmaMax) != None:
        if len(sigmaMax) != len(conn):
            raise Exception('Length of conn and sigmaMax must match')
  if len(xList) != len(yList):
    raise Exception('Length of xList and yList must match')
    
  if max(u) != None:
    if plotType == 'frame':
        if len(u) != len(xList)*3:
            raise Exception('Length of u must be length of xList * 3 for frames')
    else:
        if len(u) != len(xList)*2:
            raise Exception('Length of u must be length of xList * 2 for trusses')

  fig = figure(num=None, figsize=(8, 5), dpi=200, facecolor='w', edgecolor='k')

  node_index = find_min_index(conn)

  dxmax = max(xList)-min(xList)
  dymax = max(yList)-min(yList)
  rmax = sqrt(dxmax**2+dymax**2)

  for i, nodes in enumerate(conn):
    i1 = nodes[0]-node_index
    i2 = nodes[1]-node_index
    xi1 = xList[i1]
    xi2 = xList[i2]
    yi1 = yList[i1]
    yi2 = yList[i2]
    line1,  = plot([xi1, xi2], [yi1, yi2], 'k-o')
  for i, x in enumerate(xList):
    y = yList[i]
    annotate(i+node_index, (x+.01*rmax, y))

  if max(u) != None:
    maxu = 0
    for uval in u:
      if abs(uval) > maxu:
        maxu = abs(uval)

    factor = floor(rmax*10/(25*maxu))/10
    #print(rmax, maxu, factor)

    for i, nodes in enumerate(conn):
      i1 = nodes[0]-node_index
      i2 = nodes[1]-node_index
      if (plotType == 'frame'):
        nDOF = 3
      else:
        nDOF = 2
      n1 = nDOF*nodes[0]-nDOF*node_index
      n2 = nDOF*nodes[0]-nDOF*node_index + 1
      n3 = nDOF*nodes[0]-nDOF*node_index + 2
      n4 = nDOF*nodes[1]-nDOF*node_index
      n5 = nDOF*nodes[1]-nDOF*node_index + 1
      n6 = nDOF*nodes[1]-nDOF*node_index + 2
      xi1 = xList[i1]
      xi2 = xList[i2]
      yi1 = yList[i1]
      yi2 = yList[i2]
      xdi1 = xList[i1] + u[n1]*factor
      xdi2 = xList[i2] + u[n4]*factor
      ydi1 = yList[i1] + u[n2]*factor
      ydi2 = yList[i2] + u[n5]*factor

      xud = [xi1, xi2, yi1, yi2]

      if (plotType == 'frame'):
        tdi1 = u[n3]*factor
        tdi2 = u[n6]*factor
        xd = [xdi1, xdi2, ydi1, ydi2, tdi1, tdi2]
        xp, yp = beam_shape(xud, xd, 50)

      else:
        xp = [xdi1, xdi2]
        yp = [ydi1, ydi2]

      cval = get_color(i, sigmaMax, colormap)
      line2,  = plot(xp, yp, color=cval)

    text(min(xList)-.1*(dxmax), max(yList)+ (dymax)*.1, 'Deformation scaled by ' + str(factor) + 'x', fontsize=8)

  xlabel(f'x [{lengthUnit}]')
  ylabel(f'y [{lengthUnit}]')
  #legend([line1, line2], ['original', 'deformed x ' + str(factor)])
  #mshow(cmap='viridis')
  if (max(sigmaMax) != None):
    text(min(xList)+.35*(dxmax), max(yList)+ (dymax)*.12, 'Max stress = %8.3e ' % max(sigmaMax) + stressUnit, fontsize=8)
    text(min(xList)+.35*(dxmax), max(yList)+ (dymax)*.07, 'Min stress = %8.3e ' % min(sigmaMax) + stressUnit, fontsize=8)
    nValues = arange(0, 30)
    cnorm = Normalize(vmin = min(sigmaMax), vmax = max(sigmaMax))
    scmap = ScalarMappable(norm=cnorm, cmap=colormap)
    scmap.set_array(nValues)
    cbar = colorbar(scmap)
    cbar.set_label(f'Max element stress [{stressUnit}]')