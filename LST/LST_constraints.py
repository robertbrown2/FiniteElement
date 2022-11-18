def LST_buildConstraint(constraint1, constraint2, node3):
  """
  Create a new constraint on the midpoint node of a line.
  constraint1 and constraint2 are the two nodal constraints
  node3 is the node associated with the midpoint.
  """
  from ..common.parseConstraint import parseConstraint
  cx1, cy1, dx1, dy1, n1 = parseConstraint(constraint1)
  cx2, cy2, dx2, dy2, n2 = parseConstraint(constraint2)
  cx3 = False
  cy3 = False
  if (cx1 and cx2):
    cx3 = True
    dx3 = (dx1 + dx2)/2
  if (cy1 and cy2):
    cy3 = True
    dy3 = (dy1 + dy2)/2
  
  if (cx3 and not cy3):
    return [node3, 'x', dx3]
  elif (cy3 and not cx3):
    return [node3, 'y', dy3]
  elif (cx3 and cy3):
    return [node3, 'xy', [dx3, dy3]]
  else:
    return None

def LST_constraints(constraints, conn):
  """
  Check along all lines in connectivity to see if constraints fall on a line.
  If so, additionally constrain any nodes in between the constrained nodes.
  Set specified displacements to the average of line endpoint values.
  """
  from .LST_midpointNode import LST_midpointNode
  conNodes = []
  LSTconstraints = constraints.copy()
  for elem in conn:
    elemCon = []
    for i, node in enumerate(elem):
      for con in constraints:
        if (node == con[0]):
          elemCon.append([i, con])
    
    if (len(elemCon) == 2):
      n1 = elemCon[0][0]
      n2 = elemCon[1][0]
      m1 = LST_midpointNode(n1, n2)
      
      if (conNodes.count(elem[m1]) == 0):
        conNodes.append(elem[m1])
        newCon = LST_buildConstraint(elemCon[0][1], elemCon[1][1], elem[m1])
        if (newCon != None):
          LSTconstraints.append(newCon)

    if (len(elemCon) == 3):
      n1 = elemCon[0][0]
      n2 = elemCon[1][0]
      n3 = elemCon[2][0]
      m1 = LST_midpointNode(n1, n2)
      m2 = LST_midpointNode(n2, n3)
      m3 = LST_midpointNode(n1, n3)
      if (conNodes.count(elem[m1]) == 0):
        conNodes.append(elem[m1])
        newCon = LST_buildConstraint(elemCon[0][1], elemCon[1][1], elem[m1])
        if (newCon != None):
          LSTconstraints.append(newCon)
      if (conNodes.count(elem[m2]) == 0):
        conNodes.append(elem[m2])
        newCon = LST_buildConstraint(elemCon[1][1], elemCon[2][1], elem[m2])
        if (newCon != None):
          LSTconstraints.append(newCon)
      if (conNodes.count(elem[m3]) == 0):
        conNodes.append(elem[m3])
        newCon = LST_buildConstraint(elemCon[0][1], elemCon[2][1], elem[m3])
        if (newCon != None):
          LSTconstraints.append(newCon)
  return LSTconstraints
