def Q4_shapeFunctions(xi, eta):
  """
  [psi1, psi2, psi3, psi4] = Q4_shapeFunctions(xi, eta)
  Return the shape function values at a given xi and eta.
  """
  psi1 = (1 - xi)*(1 - eta)/4
  psi2 = (1 + xi)*(1 - eta)/4
  psi3 = (1 + xi)*(1 + eta)/4
  psi4 = (1 - xi)*(1 + eta)/4
  
  return [psi1, psi2, psi3, psi4]

def Q4_shapeDerivatives(xi, eta):
  """
  [dpsidxi, dpsideta] = Q4_shapeDerivatives(xi, eta)
  Find the derivatives of the shape functions with respect to xi and eta.
  
  """
  dpsidxi = []
  dpsideta = []
  dpsidx = []
  dpsidy = []

  dpsidxi.append(-(1 - eta)/4) #dpsi1/dxi
  dpsidxi.append( (1 - eta)/4) #dpsi2/dxi
  dpsidxi.append( (1 + eta)/4) #dpsi3/dxi
  dpsidxi.append(-(1 + eta)/4) #dpsi4/dxi

  dpsideta.append(-(1 - xi)/4) #dpsi1/deta
  dpsideta.append(-(1 + xi)/4) #dpsi2/deta
  dpsideta.append( (1 + xi)/4) #dpsi3/deta
  dpsideta.append( (1 - xi)/4) #dpsi4/deta

  return [dpsidxi, dpsideta]
