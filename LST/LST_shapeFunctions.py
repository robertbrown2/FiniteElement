def LST_shapeFunctions(xi, eta):
  """
  [psi1, psi2, psi3, psi4, psi5, psi6] = LST_shapeFunctions(xi, eta)
  Return the shape function values at a given xi and eta.
  """
  psi1 = 1 - 3*xi - 3*eta + 2*xi**2 + 4*xi*eta + 2*eta**2
  psi2 = -xi + 2*xi**2
  psi3 = -eta + 2*eta**2
  psi4 = 4*xi*eta
  psi5 = 4*eta - 4*eta**2 - 4*xi*eta
  psi6 = 4*xi - 4*xi**2 - 4*xi*eta
  
  return [psi1, psi2, psi3, psi4, psi5, psi6]


def LST_shapeDerivatives(xi, eta):
  """
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)
  Find the derivatives of the shape functions with respect to xi and eta.
  
  """
  dpsidxi = []
  dpsideta = []
  dpsidx = []
  dpsidy = []

  dpsidxi.append(-3 + 4*xi + 4*eta) #dpsi1/dxi
  dpsidxi.append(4*xi - 1) #dpsi2/dxi
  dpsidxi.append(0) #dpsi3/dxi
  dpsidxi.append(4*eta) #dpsi4/dxi
  dpsidxi.append(-4*eta)
  dpsidxi.append(4 - 8*xi - 4*eta)

  dpsideta.append(-3 + 4*xi + 4*eta) #dpsi1/deta
  dpsideta.append(0) #dpsi2/deta
  dpsideta.append(4*eta - 1) #dpsi3/deta
  dpsideta.append(4*xi) #dpsi4/deta
  dpsideta.append(4 - 8*eta - 4*xi)
  dpsideta.append(-4*xi)

  return [dpsidxi, dpsideta]
