from .faceArea import faceArea, lineLength
from .quadPoints import quadPoints
from ..LST.LST_shapeFunctions import LST_shapeFunctions
from numpy import zeros, array

# ---------------------------------------------------------------------------

def convectionBC(bc, xBC, yBC, thickness, precision=5):
  '''
  Create stiffness matrix and force vector for a convection boundary condition.
  '''
  if not (len(xBC) == 6 and bc.geom == 'face') and not (len(xBC) ==3 and bc.geom == 'line'):
    print('len(xBC) = ', len(xBC), ', bc.geom = ', bc.geom)
    raise Exception('Problem in convectionBC: LST elements implemented')
  if (bc.geom == 'line'):
    # Find the convection stiffness and force for a line
    
    L = lineLength(xBC, yBC)  
    
    # Set up shape functions, x, and y as functions of xi
    psi1 = lambda xi: LST_shapeFunctions(xi, 0)[0]
    psi2 = lambda xi: LST_shapeFunctions(xi, 0)[5]
    psi3 = lambda xi: LST_shapeFunctions(xi, 0)[1]
    x = lambda xi: psi1(xi)*xBC[0] + psi2(xi)*xBC[1] + psi3(xi)*xBC[2]
    y = lambda xi: psi1(xi)*yBC[0] + psi2(xi)*yBC[1] + psi3(xi)*yBC[2]
    
    # Set up Tinf as a function of xi
    if (bc.VarType('value') == 'const'):
      Tinf = lambda xi: bc.value
    elif (bc.VarType('value') == 'poly'):
      Tinf = lambda xi: bc.value(xi)
    elif (bc.VarType('value') == 'func'):
      Tinf = lambda xi: bc.value(x(xi), y(xi))
    else:
      print ('bc.VarType("value") = ', bc.VarType("value"))
      raise Exception('Problem in convectionBC: bc.value must be a constant, NumPy polynomial, or function')
    
    # Set up h as a function of xi
    if (bc.VarType('coefficient') == 'const'):
      h = lambda xi: bc.coefficient
    elif (bc.VarType('coefficient') == 'poly'):
      h = lambda xi: bc.coefficient(xi)
    elif (bc.VarType('coefficient') == 'func'):
      h = lambda xi: bc.coefficient(x(xi), y(xi))
    else:
      raise Exception('Problem in convectionBC: bc.value must be a constant, NumPy polynomial, or function')
    
    # perform integration of forces and stiffness matrix using Gaussian quadrature
    qP = quadPoints('line', precision)
    kbc = zeros([3, 3])
    forces = zeros(3)
    for k, xi in enumerate(qP.points):
      for i, pi in enumerate([psi1, psi2, psi3]):
        forces[i] += L*thickness*h(xi)*Tinf(xi)*pi(xi)*qP.weights[k]
        for j, pj in enumerate([psi1, psi2, psi3]):
          kbc[i, j] += L*thickness*h(xi)*pi(xi)*pj(xi)*qP.weights[k]
  elif (bc.geom == 'face'):
    # Find the convection stiffness and force on a face
    
    # Set up shape functions, x, and y as functions of xi
    psi = lambda xi, eta: LST_shapeFunctions(xi, eta)
    x = lambda xi, eta: array(psi(xi, eta))@array(xBC)
    y = lambda xi, eta: array(psi(xi, eta))@array(yBC)
    Area = faceArea(xBC, yBC)

    # Set up Tinf as a function of xi
    if (bc.VarType('value') == 'const'):
      Tinf = lambda xi, eta: bc.value
    elif (bc.VarType('value') == 'func'):
      Tinf = lambda xi, eta: bc.value(x(xi, eta), y(xi, eta))
    else:
      raise Exception('Problem in convectionBC: for faces, bc.value must be a constant or function')
    
    # Set up h as a function of xi
    if (bc.VarType('coefficient') == 'const'):
      h = lambda xi, eta: bc.coefficient
    elif (bc.VarType('coefficient') == 'func'):
      h = lambda xi, eta: bc.coefficient(x(xi, eta), y(xi, eta))
    else:
      raise Exception('Problem in convectionBC: for faces, bc.value must be a constant or function')
    
    # perform integration of forces and stiffness matrix using Gaussian quadrature
    qP = quadPoints('triangle', precision)
    kbc = zeros([6, 6])
    forces = zeros(6)
    for k, xieta in enumerate(qP.points):
      xi, eta = xieta
      for i in range(0, 6):
        forces[i] += Area*h(xi, eta)*Tinf(xi, eta)*psi(xi, eta)[i]*qP.weights[k]
        for j in range(0, 6):
          kbc[i, j] += Area*h(xi, eta)*psi(xi, eta)[i]*psi(xi, eta)[j]*qP.weights[k]
  return kbc, forces

# ---------------------------------------------------------------------------
def flowBC(bc, xBC, yBC, precision=5):
  '''
  Create force vector for a flow boundary condition.
  '''
  if not (len(xBC) == 6 and bc.geom == 'face') and not (len(xBC) ==3 and bc.geom == 'line'):
    raise Exception('Problem in convectionBC: LST elements implemented')
  if (bc.geom == 'line'):
    # Find the force for a line
    
    L = lineLength(xBC, yBC)  
    
    # Set up Tinf as a function of xi
    if (bc.VarType('value') == 'const'):
      Q = bc.value
    else:
      print ('bc.VarType("value") = ', bc.VarType("value"))
      raise Exception('Problem in convectionBC: bc.value must be a constant for flow')
    forces = [Q/6, 2*Q/3, Q/6]
      
  elif (bc.geom == 'face'):
    # Find the force for a face
    
    Area = faceArea(xBC, yBC)  
    
    # Set up Tinf as a function of xi
    if (bc.VarType('value') == 'const'):
      Q = bc.value
    else:
      print ('bc.VarType("value") = ', bc.VarType("value"))
      raise Exception('Problem in convectionBC: bc.value must be a constant for flow')
    forces = [0, 0, 0, 1/3, 1/3, 1/3]
  return forces

# ---------------------------------------------------------------------------
def fluxBC(bc, xBC, yBC, thickness, precision=5):
  '''
  Create force vector for a flux boundary condition.
  '''
  if not (len(xBC) == 6 and bc.geom == 'face') and not (len(xBC) ==3 and bc.geom == 'line'):
    raise Exception('Problem in convectionBC: LST elements implemented')
  if (bc.geom == 'line'):
    # Find the convection stiffness and force for a line
    
    L = lineLength(xBC, yBC)  
    
    # Set up shape functions, x, and y as functions of xi
    psi1 = lambda xi: LST_shapeFunctions(xi, 0)[0]
    psi2 = lambda xi: LST_shapeFunctions(xi, 0)[5]
    psi3 = lambda xi: LST_shapeFunctions(xi, 0)[1]
    x = lambda xi: psi1(xi)*xBC[0] + psi2(xi)*xBC[1] + psi3(xi)*xBC[2]
    y = lambda xi: psi1(xi)*yBC[0] + psi2(xi)*yBC[1] + psi3(xi)*yBC[2]
    
    # Set up Tinf as a function of xi
    if (bc.VarType('value') == 'const'):
      q = lambda xi: bc.value
    elif (bc.VarType('value') == 'poly'):
      q = lambda xi: bc.value(xi)
    elif (bc.VarType('value') == 'func'):
      q = lambda xi: bc.value(x(xi), y(xi))
    else:
      print ('bc.VarType("value") = ', bc.VarType("value"))
      raise Exception('Problem in convectionBC: bc.value must be a constant, NumPy polynomial, or function')
    
    # perform integration of forces and stiffness matrix using Gaussian quadrature
    qP = quadPoints('line', precision)
    kbc = zeros([3, 3])
    forces = zeros(3)
    for k, xi in enumerate(qP.points):
      for i, pi in enumerate([psi1, psi2, psi3]):
        forces[i] += L*thickness*q(xi)*pi(xi)*qP.weights[k]
        
  elif (bc.geom == 'face'):
    # Find the convection stiffness and force on a face
    
    # Set up shape functions, x, and y as functions of xi
    psi = lambda xi, eta: LST_shapeFunctions(xi, eta)
    x = lambda xi, eta: array(psi(xi, eta))@array(xBC)
    y = lambda xi, eta: array(psi(xi, eta))@array(yBC)
    Area = faceArea(xBC, yBC)

    # Set up Tinf as a function of xi
    if (bc.VarType('value') == 'const'):
      q = lambda xi, eta: bc.value
    elif (bc.VarType('value') == 'func'):
      q = lambda xi, eta: bc.value(x(xi, eta), y(xi, eta))
    else:
      raise Exception('Problem in convectionBC: for faces, bc.value must be a constant or function')
    
    # perform integration of forces and stiffness matrix using Gaussian quadrature
    qP = quadPoints('triangle', precision)
    kbc = zeros([6, 6])
    forces = zeros(6)
    for k, xieta in enumerate(qP.points):
      xi, eta = xieta
      for i in range(0, 6):
        forces[i] += Area*q(xi, eta)*psi(xi, eta)[i]*qP.weights[k]

  return forces
# ---------------------------------------------------------------------------

def applyBCs(k, bcs, xnode, ynode, thickness, type2D, index):
  
  kbc = k.copy()
  forces = [0]*len(k)
  nDOF = len(k)/len(xnode)
  if type2D == 'diffusion':
    # Check for incompatible kinds
    for bc in bcs:
      if bc.kind == 'temperature' or bc.kind == 'convection' or bc.kind =='flow' or bc.kind == 'flux':
        pass
      else:
        raise Exception('Error when applying BCs: diffusion BCs must be one of: \n "temperature", "convection", "flux", or "flow".')
    # Apply all non-constraint BCs
    for bc in bcs:
      # Calculate area of face
      xElem = []
      yElem = []
      
      for bcnode in bc.nodes:
        xElem.append(xnode[bcnode - index])
        yElem.append(ynode[bcnode - index])

      if bc.kind == 'convection':
        kconv, fconv = convectionBC(bc, xElem, yElem, thickness)
        for i, inode in enumerate(bc.nodes):
          for j, jnode in enumerate(bc.nodes):
            kbc[inode-index, jnode-index] += kconv[i, j]
          forces[inode-index] += fconv[i]
      elif bc.kind == 'flow':
        fflow = flowBC(bc, xElem, yElem)
        for i, inode in enumerate(bc.nodes):
          forces[inode - index] += fflow[i]
      elif bc.kind == 'flux':
        fflux = fluxBC(bc, xElem, yElem, thickness)
        for i, inode in enumerate(bc.nodes):
          forces[inode - index] += fflux[i]
        
    # Apply temperature constraints
    for bc in bcs:
      if bc.kind == 'temperature':  
        for i, bcnode in enumerate(bc.nodes):
          node = bcnode - index
          kbc[node, :] = 0
          kbc[node, node] = 1
          if bc.VarType("value") == 'const':
            forces[node] = bc.value
          elif bc.VarType("value") == 'poly':  # poly only allowed on lines
            forces[node] = bc.value(i/(len(bc.nodes)-1))
          elif bc.VarType("value") == 'func':
            x = xnode[node]
            y = ynode[node]
            forces[node] = bc.value(x, y)
  elif type2D == 'planeStress' or type2D == 'planeStrain':
    raise Exception('planeStress and planeStrain BCs not yet implemented')
  elif type2D == 'axisymmetric':
    raise Exception('axisymmetric BCs not yet implemented')
  else:
    raise Exception('Error when applying BCs: diffusion BCs must be one of: \n "temperature", "convection", "flux", or "flow".')
  return kbc, forces