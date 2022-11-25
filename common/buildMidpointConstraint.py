def buildMidpointConstraint(constraint1, constraint2, node3):
  """
  Create a new constraint on the midpoint node of a line.
  constraint1 and constraint2 are the two nodal constraints
  node3 is the node associated with the midpoint.
  """
  #from ..common.parseConstraint import parseConstraint
  #cx1, cy1, dx1, dy1, n1 = parseConstraint(constraint1)
  #cx2, cy2, dx2, dy2, n2 = parseConstraint(constraint2)
  c3 = ''
  d3 = []
  
  c1types = constraint1[1]
  c2types = constraint2[1]
  d1vals = constraint1[2]
  d2vals = constraint2[2]
  
  for i1, c1type in enumerate(c1types):
    for i2, c2type in enumerate(c2types):
      if (len(c1types)>1):
        d1 = d1vals[i1]
      else:
        d1 = d1vals
      if (len(c2types)>1):
        d2 = d2vals[i2]
      else:
        d2 = d2vals
      if (c1type == c2type):
        c3+=c1type
        d3.append((d1+d2)/2)
  if (len(c3) > 1):
    return [node3, c3, d3]
  elif (len(c3) == 1):
    return [node3, c3, d3[0]]
  else:
    return None
