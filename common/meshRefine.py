from numpy.polynomial import polynomial
from math import factorial

def lineExists(line2node, l2n):
  for i, l2ni in enumerate(line2node):
    if l2ni[0] == l2n[0] and l2ni[1] == l2n[1]:
      return i
    if l2ni[1] == l2n[0] and l2ni[0] == l2n[1]:
      return i
  return -1

# ----------------------------------------------------------------

def cellExists(conn, c2n):
  c2ns = sorted(c2n)
  for i, c2ni in enumerate(conn):
    if sorted(c2ni) == c2ns:
      return i
  return -1

# ----------------------------------------------------------------

def buildc2lAndl2n(conn):
  # lines are always 0 indexed, as they will be internal
  # nodes are indexed as defined by user
  conn2line = []
  line2node = []
  lineCount = 0
  
  for elem in conn:
    l2n=[0, 0, 0]
    l2n[0] = [elem[0], elem[1]]
    l2n[1] = [elem[1], elem[2]]
    l2n[2] = [elem[2], elem[0]]
    c2l = []
    for l2ni in l2n:
      lineNum = lineExists(line2node, l2ni)
      if lineNum == -1:
        line2node.append(l2ni)
        c2l.append(lineCount)
        lineCount += 1
      else:
        c2l.append(lineNum)
    conn2line.append(c2l)
    
  return conn2line, line2node
        
# -----------------------------------------------
def split_poly(p):
  coefs = p.coef
  pd = p.copy()
  p1coefs = []
  p2coefs = []
  for i, c in enumerate(coefs):
    p1coefs.append(c/(2**i))
    p2coefs.append(pd(0.5)/(2**i * factorial(i)))
    pd = polynomial.Polynomial(polynomial.polyder(pd.coef))
  return polynomial.Polynomial(p1coefs), polynomial.Polynomial(p2coefs)

def meshRefine(xnode, ynode, conn, bcs, conn2line=[], line2node=[]):
  """
  For a triangle, we generate new midpoints, and split each element into four as shown below:
  4
  |\
  | \
  5--3
  |\ |\
  | \| \
  0--1--2
  newline1-6: exterior, CCW from 0 (0-1, 1-2, etc.)
  newline7-9: interior, CCW from 1 (1-3, 3-5, 5-1)
  new elements: [0, 1, 5], [2, 3, 1], [4, 5, 3], [1, 3, 5]
  """
  from .helpers import connIndex

  connNew = []
  if (len(conn2line) == 0):
    conn2line, line2node = buildc2lAndl2n(conn)

  xnodeNew = xnode.copy()
  ynodeNew = ynode.copy()
  index = connIndex(conn)
  faceMap = []
  lineMap = []
  
  line2nodeNew = []
  lineUpdateList = []
  lineCount = 0
  nodeCount = len(xnode)
  if len(xnode) != len(ynode):
    raise Exception('You done goofed in node definition: xnode and ynode must have same number of nodes!')
  
  # Create xnodeNew, ynodeNew, and start line2nodeNew
  for line in line2node:
    i1 = line[0]
    i2 = nodeCount + index
    i3 = line[1]
    xmid = (xnode[line[0]-index] + xnode[line[1]-index])/2
    ymid = (ynode[line[0]-index] + ynode[line[1]-index])/2
    xnodeNew.append(xmid)
    ynodeNew.append(ymid)
    nodeCount += 1
    line2nodeNew.append([i1, i2])
    line2nodeNew.append([i2, i3])
    lineUpdateList.append([lineCount, lineCount + 1])
    lineCount = lineCount + 2
  
  elemCount = 0
  connNew = []
  conn2lineNew = []
  connUpdateList = []
  # Create connNew, conn2lineNew, and finish line2nodeNew
  for i, elem in enumerate(conn):
    node = [-1]*6
    # need to create new connectivity (connNew), add new lines to line2nodeNew,
    # and create conn2lineNew
    
    oldline1 = conn2line[i][0] # connects node[0] and node[2]
    oldline2 = conn2line[i][1] # connects node[2] and node[4]
    oldline3 = conn2line[i][2] # connects node[4] and node[0]
    
    # Step one: get nodes in order (direction same as original)
    node[0] = elem[0]
    node[2] = elem[1]
    node[4] = elem[2]
    
    # find node[1]
    #   let newline1 connect node[0] and node[1]
    #   let newline2 connect node[1] and node[2]
    newline1 = lineUpdateList[oldline1][0]
    node[1] = line2nodeNew[newline1][1]
    # Check newline1 and newline2
    if (line2nodeNew[newline1][0] != node[0]):
      newline2 = newline1
      newline1 = lineUpdateList[oldline1][1]
    else:
      newline2 = lineUpdateList[oldline1][1]
    
    # find node[3]
    #   let newline3 connect node[2] and node[3]
    #   let newline4 connect node[3] and node[4]
    newline3 = lineUpdateList[oldline2][0]
    node[3] = line2nodeNew[newline3][1]
    # Check newline3 and newline4
    if (line2nodeNew[newline3][0] != node[2]):
      newline4 = newline3
      newline3 = lineUpdateList[oldline2][1]
    else:
      newline4 = lineUpdateList[oldline2][1]
    
    # find node[5]
    #   let newline5 connect node[4] and node[5]
    #   let newline6 connect node[5] and node[0]
    newline5 = lineUpdateList[oldline3][0]
    node[5] = line2nodeNew[newline5][1]
    # Check newline5 and newline6
    if (line2nodeNew[newline5][0] != node[4]):
      newline6 = newline5
      newline5 = lineUpdateList[oldline3][1]
    else:
      newline6 = lineUpdateList[oldline3][1]
  
    # Create new elements
    connNew.append([node[0], node[1], node[5]])
    connNew.append([node[2], node[3], node[1]])
    connNew.append([node[4], node[5], node[3]])
    connNew.append([node[1], node[3], node[5]])

    # Create interior lines
    line2nodeNew.append([node[1], node[3]])
    line2nodeNew.append([node[3], node[5]])
    line2nodeNew.append([node[5], node[1]])
    newline7 = lineCount
    newline8 = lineCount + 1
    newline9 = lineCount + 2
    lineCount = lineCount + 3
    
    # Create new conn2line
    conn2lineNew.append([newline1, newline9, newline6])
    conn2lineNew.append([newline3, newline7, newline2])
    conn2lineNew.append([newline5, newline8, newline4])
    conn2lineNew.append([newline7, newline8, newline9])
    
    connUpdateList.append([elemCount, elemCount+1, elemCount+2, elemCount+3])
    elemCount = elemCount + 4

    
  # Sample BCs:
  """
  bcs.append({geom:'point', nodes:1, kind:'temperature', value: 0})
  bcs.append({geom:'line', nodes:[3, 4], kind:'convection', value:50, coefficient:2.5})
  bcs.append({geom:'face', nodes:[1, 2, 3], kind:'heat flow', value:100})
  """
  bcsNew = []
  for bc in bcs:
    if bc.geom == 'point':
      # No change required for point boundary conditions - point names do not change
      bcsNew.append(bc)
    elif bc.geom == 'line':
      # Line boundary conditions should be applied to new child lines
      lineNum = lineExists(line2node, bc.nodes)
      if lineNum == -1:
        raise Exception('You done goofed in bc "nodes": line does not exist in conn')
      else:
        bc1 = bc.copy()
        bc2 = bc.copy()
        
        # Create new lines and swap order if necessary
        if line2node[lineNum][0] == bc.nodes[0]:   # order is same as in line2node
          newLineNum1 = lineUpdateList[lineNum][0]
          newLineNum2 = lineUpdateList[lineNum][1]
        else:                          # order is flipped from line2node
          templineNum1 = lineUpdateList[lineNum][1]
          newline1 = [line2nodeNew[templineNum1][1], line2nodeNew[templineNum1][0]]
          templineNum2 = lineUpdateList[lineNum][0]
          newline2 = [line2nodeNew[templineNum2][1], line2nodeNew[templineNum2][0]]
        
        bc1.nodes=newline1
        bc2.nodes=newline2
        
        if bc.VarType('value') == 'poly':
          # const and func variations do not need changes from splitting
          [poly1, poly2] = split_poly(bc.value)
          bc1.value = poly1
          bc2.value = poly2
        if bc.VarType('coefficient') == 'poly':
          # const and func variations do not need changes from splitting
          [poly1, poly2] = split_poly(bc.coefficient)
          bc1.coefficient = poly1
          bc2.coefficient = poly2
          
        # Flow kind of BC must be split  
        if bc.kind == 'flow':
          bc1.value = bc.value/2
          bc2.value = bc.value/2
          
        bcsNew.append(bc1)
        bcsNew.append(bc2)
    elif bc.geom == 'face':
      # Face boundary conditions should be applied to new child faces
      elemNum = cellExists(conn, bc.nodes)
      if lineNum == -1:
        raise Exception('You done goofed in bc "nodes": cell does not exist in conn')
      else:
        bc1 = bc.copy()
        bc2 = bc.copy()
        bc3 = bc.copy()
        bc4 = bc.copy()
        
        newElems = connUpdateList(elemNum)
        bc1.nodes = connNew[newElems[0]]
        bc2.nodes = connNew[newElems[1]]
        bc3.nodes = connNew[newElems[2]]
        bc4.nodes = connNew[newElems[3]]
        
        # Flow kind of BC must be split  
        if bc.kind == 'flow':
          bc1.value = bc.value/4
          bc2.value = bc.value/4
          bc3.value = bc.value/4
          bc4.value = bc.value/4
        
        bcsNew.append(bc1)
        bcsNew.append(bc2)
        bcsNew.append(bc3)
        bcsNew.append(bc4)
        if bc.VarType('value') == 'poly':
          raise Exception('You done goofed in bc "value": face value cannot be a 1D polynomial')
        if bc.VarType('coefficient') == 'poly':
          raise Exception('You done goofed in bc "coefficient": face value cannot be a 1D polynomial')
    else:
      raise Exception('You done goofed in bc "geom": Geometry type should be "point", "line", or "face"')
  
  
  return [xnodeNew, ynodeNew, connNew, bcsNew, conn2lineNew, line2nodeNew]
