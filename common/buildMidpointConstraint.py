def buildMidpointConstraint(constraint1, constraint2, node3):
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
