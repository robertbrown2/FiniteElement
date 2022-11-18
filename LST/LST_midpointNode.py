def LST_midpointNode(n1, n2):
  """
  Helper function for LST_constraints and LST_forces
  Determine which node in an element should be used for the midpoint of input nodes
  2
  |\
  | \
  4  3
  |   \
  |    \
  0--5--1
  """
  if (n1 == 0):
    if (n2 == 1):
      return 5
    else: # n2 == 2
      return 4
  elif (n1 == 1):
    if (n2 == 0):
      return 5
    else: # n2 == 1
      return 3
  else: # n1 == 2
    if (n2 == 0):
      return 4
    else: # n2 == 1
      return 3
