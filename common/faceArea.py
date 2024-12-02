from numpy import sqrt
def faceArea(x, y):
  '''
  Find the area of a face.
  
  Face could be CST (3 nodes), LST (6 nodes), or Q4 (4 nodes).
  
  For LST, only the first three nodes are used, as the first three are the corners.
  '''
  
  nNode = len(x)
  if nNode == 3 or nNode == 6:
    [x1, x2, x3] = x[0:3]
    [y1, y2, y3] = y[0:3]
    Area = 1/2*(x1*y2 - x2*y1 + x2*y3 - x3*y2 + x3*y1 - x1*y3)
  elif nNode == 4 or nNode == 8:
    [x1, x2, x3, x4] = x[0:4]
    [y1, y2, y3, y4] = y[0:4]
    Area = 1/2*(x1*y2 - x2*y1 + x2*y3 - x3*y2 + x3*y4 - x4*y3 + x4*y1 - x1*y4)
  else:
    raise Exception('Error in faceArea - number of nodes does not match expectations')
  return Area
    
def lineLength(x, y):
  '''
  Find the length of a line.  The first and final nodes must be the endpoints.
  '''
  dx = x[-1] - x[0]
  dy = y[-1] - y[0]
  return sqrt(dx**2 + dy**2)