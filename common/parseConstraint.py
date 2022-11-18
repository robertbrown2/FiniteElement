def parseConstraint(c):
  """
  Parse a constraint c, which has the form: [node, type, displacement]
  Output whether the node is constrained in x and y (cx, cy)
  Also output values of specified displacments (dx, dy)
  If cx/cy is False, the corresponding displacement will be None
  """
  dx = None
  dy = None
  if (c[1] == 'x'):
    cx = True
    cy = False
    dx = c[2]
  elif (c[1] == 'y'):
    cx = False
    cy = True
    dy = c[2]
  elif (c[1] == 'xy'):
    cx = True
    cy = True
    dx = c[2][0]
    dy = c[2][1]
  else:
    print('Bad constraint: ', c)
    raise Exception
  return cx, cy, dx, dy, c[0]
