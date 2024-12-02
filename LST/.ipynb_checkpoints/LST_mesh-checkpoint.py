def LST_mesh(xnode, ynode, CSTconn, conn2line, CSTline2node, CSTbcs):
  """
  Usage - LST_mesh(xnode, ynode, CSTconn, conn2line, line2node)
  Creates additional nodes for LST elements:
    node 4 between 2 and 3
    node 5 between 1 and 3
    node 6 between 1 and 2
  ---------
    Input
  ---------
  xnode - list of x locations of nodes
  ynode - list of y locations of nodes
  CSTconn - connectivity matrix for three node elements
  
  ----------
    Output
  ----------
  LSTxnode - list of x locations of nodes, including line midpoints
  LSTynode - list of y locations of nodes, including line midpoints
  LSTconn - connectivity matrix for six node elements
  LSTline2node - connectivity between lines and LST nodes
  """
  from ..common.helpers import connIndex
  from ..common.meshRefine import lineExists, cellExists, buildc2lAndl2n
  from ..common.BC import BC
  
  if (len(conn2line) == 0):
    conn2line, CSTline2node = buildc2lAndl2n(CSTconn)
  
  index = connIndex(CSTconn)
  
  LSTxnode = xnode.copy()
  LSTynode = ynode.copy()
  LSTline2node = []
  nodeCount = len(xnode)
  
  # Create new nodes on lines and create LSTline2node
  for iline in CSTline2node:
    i1 = iline[0]
    i2 = iline[1]
    xmid = (xnode[i1-index] + xnode[i2-index]) / 2
    ymid = (ynode[i1-index] + ynode[i2-index]) / 2
    LSTxnode.append(xmid)
    LSTynode.append(ymid)
    nodeCount += 1
    LSTline2node.append([i1, nodeCount, i2])
  
  # Create LST connectivity
  LSTLineList = []
  LSTconn = []
  for i, elem in enumerate(CSTconn):
    LSTelem = elem.copy()
    lines = [0]*3
    lines[0] = CSTline2node[conn2line[i][0]]
    lines[1] = CSTline2node[conn2line[i][1]]
    lines[2] = CSTline2node[conn2line[i][2]]
    
    line4 = lineExists(lines, [elem[1], elem[2]])
    line5 = lineExists(lines, [elem[0], elem[2]])
    line6 = lineExists(lines, [elem[0], elem[1]])
    
    node4 = LSTline2node[conn2line[i][line4]][1]# + index
    node5 = LSTline2node[conn2line[i][line5]][1]# + index
    node6 = LSTline2node[conn2line[i][line6]][1]# + index
    
    LSTelem.append(node4)
    LSTelem.append(node5)
    LSTelem.append(node6)
    LSTconn.append(LSTelem)
  
  LSTbcs = []
  for bc in CSTbcs:
    LSTbc = bc.copy()

    bcnodes = bc.nodes
    if len(bcnodes) == 1:
      pass
    elif len(bcnodes) == 2:
      CSTline = lineExists(CSTline2node, [bcnodes[0], bcnodes[1]])
      LSTbc.nodes = LSTline2node[CSTline]
    elif len(bcnodes) == 3:
      CSTelem = cellExists(CSTconn, bcnodes)
      LSTbc.nodes = LSTconn[CSTelem]
    
    LSTbcs.append(LSTbc)
  
  return [LSTxnode, LSTynode, LSTconn, LSTline2node, LSTbcs]
