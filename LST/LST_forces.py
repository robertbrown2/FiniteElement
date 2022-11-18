def LST_findMidpointFromLine(line, conn, output='midpoint'):
  """
  Find an midpoint associated with a line.
  """
  from .LST_midpointNode import LST_midpointNode
  
  elemList = []
  for elem in conn:
    flag = [False, False]
    for node in elem:
      if (node == line[0]):
        flag[0] = True
      if (node == line[1]):
        flag[1] = True
 
    if (flag[0] and flag[1]): # Both nodes on line are in element
      if (output == 'midpoint'):
        # Find which node in element matches each line node      
        if (line[0] == elem[0]):
          n1 = 0
        elif (line[0] == elem[1]):
          n1 = 1
        else:
          n1 = 2
    
        if (line[1] == elem[0]):
          n2 = 0
        elif (line[1] == elem[1]):
          n2 = 1
        else:
          n2 = 2

        # Get midpoint node associated with line  
        midpoint = LST_midpointNode(n1, n2)
        return elem[midpoint]
      elif (output == 'element'):
        # return element number
        return elem
      else:
        print('output variable not recognized in findMidpointFromLine')
        raise Exception
  return None

def LST_forces(xnode, ynode, conn, nDOF=2, pointLoads=None, lineLoads=None, faceLoads=None):
  """
  Create the force vector from a list of point loads, line loads, and face loads.
  """
  from numpy import zeros, sqrt
  from ..common.helpers import connIndex
  from ..common.isElemOnLeft import isElemOnLeft
  index = connIndex(conn)
  forces = zeros(len(xnode)*nDOF)
  if (pointLoads != None):
    for pLoad in pointLoads:
      dof = pLoad[0]*2 - 2*index
      if (pLoad[1]=='x'):
        forces[dof] = pLoad[2]
      elif (pLoad[1] == 'y'):
        forces[dof+1] = pLoad[2]
      elif (pLoad[1] == 'xy'):
        forces[dof] = pLoad[2][0]
        forces[dof+1] = pLoad[2][1]
      else:
        print("Unrecognized force in LST_forces")
        raise Exception
  
  if (lineLoads != None):
    for lLoad in lineLoads:
      i1 = lLoad[0][0]
      i2 = LST_findMidpointFromLine(lLoad[0], conn, 'midpoint')
      i3 = lLoad[0][1]
      if (i2 == None):
        print('could not find midpoint on line connecting nodes:', i1, i3)
        raise Exception
      

      dir = lLoad[1]
      f = lLoad[2]
      dx = xnode[i3-index] - xnode[i1-index]
      dy = ynode[i3-index] - ynode[i1-index]
      L = sqrt(dx**2 + dy**2)

      if (type(f) == type(1) or type(f) == type(1.0)):
        # Rectangular Load - F = int(psi*f, 0, L)
        frect = L*f
        ftri = 0
      elif (len(f) == 2):
        # Triangular Load
        frect = f[0]
        ftri = f[1]-f[0]
      else:
        print('Load not recognized in LST_forces')
        raise Exception

      F1 = frect*L/6 + ftri*L*0
      F2 = frect*L*2/3 + ftri*L/3
      F3 = frect*L/6 + ftri*L/6

      if (dir == 'x'):
        F1x = F1
        F2x = F2
        F3x = F3
        F1y = 0
        F2y = 0
        F3y = 0
      elif (dir == 'y'):
        F1x = 0
        F2x = 0
        F3x = 0
        F1y = F1
        F2y = F2
        F3y = F3
      elif (dir == 't'):
        # force is in direction from 1->2
        F1x = F1 * dx/L
        F2x = F2 * dx/L
        F3x = F3 * dx/L
        F1y = F1 * dy/L
        F2y = F2 * dy/L
        F3y = F3 * dy/L
      elif (dir == 'n'):
        # force is in direction outward from element
        elem = LST_findMidpointFromLine(lLoad[0], conn, 'element')
        left = isElemOnLeft(xnode, ynode, elem, [i1, i3], index)
        if (left):
          # normal points to right
          F1x =   F1 * dy/L
          F2x =   F2 * dy/L
          F3x =   F3 * dy/L
          F1y = - F1 * dx/L
          F2y = - F2 * dx/L
          F3y = - F3 * dx/L
        else:
          F1x = - F1 * dy/L
          F2x = - F2 * dy/L
          F3x = - F3 * dy/L
          F1y =   F1 * dx/L
          F2y =   F2 * dx/L
          F3y =   F3 * dx/L
      forces[2*(i1-index)] += F1x
      forces[2*(i2-index)] += F2x
      forces[2*(i3-index)] += F3x
      forces[2*(i1-index)+1] += F1y
      forces[2*(i2-index)+1] += F2y
      forces[2*(i3-index)+1] += F3y

  if (faceLoads != None):
    print('faceLoads not yet implemented in LST_forces!')
    raise Exception
    #for fLoad in faceLoads:
    #  elem = conn[fLoad[0]-index]
    #  dir = fLoad[1]
    #  f = fLoad[2]
  return forces
