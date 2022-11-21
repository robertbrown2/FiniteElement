def meshRefine(xnode, ynode, conn, lineLoads, faceLoads):
  from .helpers import connIndex, whichLine
  """
  For a triangle, we generate new midpoints, and split each element into four as shown below:
  3
  |\
  | \
  5--4
  |\ |\
  | \| \
  1--6--2
  """
  
  LineList = []
  if (lineLoads != None):
    lineLoadList = []
    for lLoad in lineLoads:
      lineLoadList.append(lLoad[0])
  lineLoadNew = []
  connNew = []
  xnodeNew = xnode.copy()
  ynodeNew = ynode.copy()
  index = connIndex(conn)
  for elem in conn:
    if (len(elem) == 3):
      lines = []
      lines.append([elem[1], elem[2]]) # line for node 4 (between 2 and 3)
      lines.append([elem[2], elem[0]]) # line for node 5 (between 1 and 3)
      lines.append([elem[0], elem[1]]) # line for node 6 (between 1 and 2)
      iLines = []
      
      lineNodes=[]
      for line in lines:
        iLine = whichLine(line, LineList)
        if (iLine == -1):
          xmid = (xnode[line[0]-index] + xnode[line[1]-index])/2
          ymid = (ynode[line[0]-index] + ynode[line[1]-index])/2
          iLine = len(LineList)
          LineList.append(line)
          xnodeNew.append(xmid)
          ynodeNew.append(ymid)
        lineNodes.append(iLine+len(xnode)+index)
        if (lineLoads != None):
          loadLines = whichLine(line, lineLoadList, multiple=True)
          
          if (loadLines != None):
            line1 = [line[0], iLine + len(xnode) + index]
            line2 = [iLine + len(xnode) + index, line[1]]
            for loadLine in loadLines:
              load = lineLoads[loadLine]
              lineLoadsNew.append([line1, load[1], load[2]])
              lineLoadsNew.append([line2, load[1], load[2]])
        
      # 1-6-5
      connNew.append([elem[0], lineNodes[2], lineNodes[1]])
      # 2-4-6
      connNew.append([elem[1], lineNodes[0], lineNodes[2]])
      # 3-5-4
      connNew.append([elem[2], lineNodes[1], lineNodes[0]])
      # 4-5-6
      connNew.append([lineNodes[0], lineNodes[1], lineNodes[2]])
  
  return [xnodeNew, ynodeNew, connNew, lineLoadsNew, faceLoadsNew]
