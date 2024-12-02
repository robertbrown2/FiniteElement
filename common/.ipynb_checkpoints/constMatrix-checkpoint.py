def constMatrix(E=None, nu=None, type2D='planeStress', k=None):
  """
  Create the constituitive matrix for a 2D solid.
  Usage - D = constMatrix(E, nu, type2D)
  ---------
    Input
  ---------
  E: (float) - Young's modulus of material
  nu: (float) - Poisson's ratio of material
  type2D: (string) - assumption for 2D solid
          'planeStress' - stress in z direction is zero (thin plates)
          'planeStrain' - strain in z direction is zero (thick bodies)
  k: (float) - thermal diffusivity of material
  ----------
    Output
  ----------
  D: (array) - constituitve matrix
  """
  from numpy import array, eye
  if (type2D == 'planeStress'):
    D = E / (1 - nu**2) * array([
                             [1, nu, 0],
                             [nu, 1, 0],
                             [0, 0, (1-nu)/2]
                            ])
  elif (type2D == 'planeStrain'):
    D = E / ((1 + nu)*(1 - 2*nu)) * array([
          [1-nu, nu, 0 ],
          [nu, 1-nu, 0],
          [0, 0, (1-2*nu)/2]
          ])
  elif (type2D == 'axisymmetric'):
    D = E / ((1 + nu)*(1 - 2*nu)) * array([
                             [1-nu, nu, nu, 0],
                             [nu, 1-nu, nu, 0],
                             [nu, nu, 1-nu, 0],
                             [0, 0, 0, (1-2*nu)/2]
                            ])
  elif (type2D == 'diffusion'):
    D = k * eye(2)
  else:
    print('type2D must be "planeStress", "planeStrain", "axisymmetric", or "diffusion".  Was instead: ', type2D)
    raise Exception

  return D
