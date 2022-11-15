def Q4_stress(x1234, y1234, u, xi, eta, D, type2D='PlaneStress', output='VM'):
  """
  Calculate the stress on an element at the unmapped location (xi, eta).
  Usage - sigma = Q4_stress(x1234, y1234, u=None, xi, eta, D, output='VM')
  ---------
    Input
  ---------
  x1234 - (list) x locations of nodes
  y1234 - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4]
  xi - (float) position in unmapped element
  eta - (float) position in unmapped element
  D - (array) constituitive matrix
  type2D - (string) simplifying assumption for 2D solid
  output - (string) Plot type:
      'VM' - von Mises stress
      'sigx', 'sigy', or 'tauxy' - normal stress in x or y, or shear stress
      'sig1' or 'sig2' - maximum or minimum principal stress
  ----------
    Output
  ----------
  sigma: (float) stress of requested type
  """
  from numpy import array, sqrt
  from .Q4_strain import Q4_strain

  eps = array(Q4_strain(x1234, y1234, u, xi, eta, type2D))
  sigxy = D @ eps
  if (output == 'sigx'):
    return sigxy[0]
  elif (output == 'sigy'):
    return sigxy[1]
  elif (output == 'tauxy'):
    return sigxy[2]
  else:
    sigx = sigxy[0]
    sigy = sigxy[1]
    tauxy = sigxy[2]
    sig1 = (sigx + sigy)/2 + sqrt((sigx - sigy)**2/2 + tauxy**2)
    sig2 = (sigx + sigy)/2 - sqrt((sigx - sigy)**2/2 + tauxy**2)
    if (type2D == 'planeStrain'):
      sig3 = nu*E/((1+nu)*(1-2*nu)) * (eps[0]+eps[1])
    else:
      sig3 = 0
    if (output == 'sig1'):
      return sig1
    elif (output == 'sig2'):
      return sig2
    elif (output == 'VM'):
      return sqrt(1/2)*sqrt((sig1-sig2)**2 + (sig2-sig3)**2 + (sig3-sig1)**2)
    else:
      print('Variable output in Q4_stress must be sigx, sigy, tauxy, sig1, sig2, or VM')
      raise Exception
