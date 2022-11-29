def meshRefine(xnode, ynode, conn, lineLoads, faceLoads, constraints):
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
  from .buildMidpointConstraint import buildMidpointConstraint
  LineList = []
  if (lineLoads != None):
    lineLoadList = []
    for lLoad in lineLoads:
      lineLoadList.append(lLoad[0])
      
  lineLoadsNew = []
  constraintsNew = constraints.copy()
  connNew = []
  xnodeNew = xnode.copy()
  ynodeNew = ynode.copy()
  index = connIndex(conn)
  
  # Grab all nodes that have constraints
  if (constraints != None):
    constraintNodes = []
    for c in constraints:
      constraintNodes.append(c[0])
  else:
    constraintNodes = None
   
  
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
        if (iLine == None):
          xmid = (xnode[line[0]-index] + xnode[line[1]-index])/2
          ymid = (ynode[line[0]-index] + ynode[line[1]-index])/2
          iLine = len(LineList)
          LineList.append(line)
          xnodeNew.append(xmid)
          ynodeNew.append(ymid)
          
          if (constraintNodes.count(line[0])>0 and constraintNodes.count(line[1])>0):
            for i, cNode in enumerate(constraintNodes):
              if (cNode == line[0]):
                c1 = constraints[i]
              if (cNode == line[1]):
                c2 = constraints[i]
            constraintsNew.append(buildMidpointConstraint(c1, c2, iLine + len(xnode) + index))
          
        lineNodes.append(iLine+len(xnode)+index)
        if (lineLoads != None):
          loadLines = whichLine(line, lineLoadList, multiple=True)
          
          if (loadLines != None):
            for loadLine in loadLines:
              load = lineLoads[loadLine]
              if (line[0] == lineLoadList[loadLine][0]):
                line1 = [line[0], iLine + len(xnode) + index]
                line2 = [iLine + len(xnode) + index, line[1]]
              else:
                line1 = [line[1], iLine + len(xnode) + index]
                line2 = [iLine + len(xnode) + index, line[0]]
              try:
                if (len(load[2])==2):
                  triload = load[2]
                  triload1 = [triload[0], (triload[0]+triload[1])/2]
                  triload2 = [(triload[0]+triload[1])/2, triload[1]]
                  lineLoadsNew.append([line1, load[1], triload1])
                  lineLoadsNew.append([line2, load[1], triload2])
                else:
                  print('Line load is a list with ', len(load[2]), 'items.')
                  print('Line load should either be a float or a list with 2 items.')
                  raise Exception
                  
              except TypeError:
                # This is a float
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
  faceLoadsNew = None
  
  
  return [xnodeNew, ynodeNew, connNew, lineLoadsNew, faceLoadsNew, constraintsNew]
