def LST_mesh(xnode, ynode, CSTconn):
  """
  Usage - LST_mesh(xnode, ynode, CSTconn)
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
  """
  from ..common.helpers import connIndex, whichLine
  LSTLineList = []
  LSTconn = []
  LSTxnode = xnode.copy()
  LSTynode = ynode.copy()
  index = connIndex(CSTconn)
  for elem in CSTconn:
    lines = []
    lines.append([elem[1], elem[2]]) # line for node 4 (between 2 and 3)
    lines.append([elem[2], elem[0]]) # line for node 5 (between 1 and 3)
    lines.append([elem[0], elem[1]]) # line for node 6 (between 1 and 2)
    iLines = []
    LSTelem = elem.copy()
    for line in lines:
      iLine = whichLine(line, LSTLineList)
      if (iLine == -1):
        xmid = (xnode[line[0]-index] + xnode[line[1]-index])/2
        ymid = (ynode[line[0]-index] + ynode[line[1]-index])/2
        iLine = len(LSTLineList)
        LSTLineList.append(line)
        LSTxnode.append(xmid)
        LSTynode.append(ymid)
      LSTelem.append(iLine+len(xnode)+index)
    LSTconn.append(LSTelem)
  return [LSTxnode, LSTynode, LSTconn]
