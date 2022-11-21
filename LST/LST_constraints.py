def LST_constraints(constraints, conn):
  """
  Check along all lines in connectivity to see if constraints fall on a line.
  If so, additionally constrain any nodes in between the constrained nodes.
  Set specified displacements to the average of line endpoint values.
  """
  from .LST_midpointNode import LST_midpointNode
  from ..common.buildMidpointConstraint import buildMidpointConstraint
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
        newCon = buildMidpointConstraint(elemCon[0][1], elemCon[1][1], elem[m1])
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
        newCon = buildMidpointConstraint(elemCon[0][1], elemCon[1][1], elem[m1])
        if (newCon != None):
          LSTconstraints.append(newCon)
      if (conNodes.count(elem[m2]) == 0):
        conNodes.append(elem[m2])
        newCon = buildMidpointConstraint(elemCon[1][1], elemCon[2][1], elem[m2])
        if (newCon != None):
          LSTconstraints.append(newCon)
      if (conNodes.count(elem[m3]) == 0):
        conNodes.append(elem[m3])
        newCon = buildMidpointConstraint(elemCon[0][1], elemCon[2][1], elem[m3])
        if (newCon != None):
          LSTconstraints.append(newCon)
  return LSTconstraints
