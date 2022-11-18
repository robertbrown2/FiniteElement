def isElemOnLeft(xnode, ynode, elem, line):
  """
  Determine if the element is on the left when moving along the line.
  """
  xmid = 0
  ymid = 0
  for node in elem:
    xmid += xnode[node]
    ymid += ynode[node]
  xmid = xmid / len(elem)
  ymid = ymid / len(elem)

  x1 = xnode[line[0]]
  x2 = xnode[line[1]]
  y1 = ynode[line[0]]
  y2 = ynode[line[1]]

  dx1 = x2 - x1
  dxm = xmid - x1
  dy1 = y2 - y1
  dym = ymid - y1

  # cross product of {dx1, dy1} x {dxm, dym}
  if (dx1*dym - dy1*dxm > 0): 
    return True
  else:
    return False
