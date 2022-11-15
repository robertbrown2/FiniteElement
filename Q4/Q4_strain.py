def Q4_strain(x1234, y1234, u, xi, eta, type2D, output=None):
  from numpy import array
  from .Q4_B import Q4_B
  """
  Output the strain at a point in the quadrilateral.
  Usage: eps = array([epsx, epsy, tauxy]) = Q4_strain(x1234, y1234, u, xi, eta)
  ---------
    Input
  ---------
  x1234 - (list) x locations of nodes
  y1234 - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4]
  xi, eta - (float) location on unmapped element
  ----------
    Output
  ----------
  eps: (array) contains [epsx, epsy, tauxy]
  epsx: (float) normal strain in x direction
  epsy: (float) normal strain in y direction
  tauxy: (float) shear strain
  """

  B = Q4_B(x1234, y1234, xi, eta, type2D)
  eps = B @ array(u)
  if (output == None):
    return eps
  elif (output == 'epsx'):
    return eps[0]
  elif (output == 'epsy'):
    return eps[1]
  elif (output == 'gammaxy'):
    return eps[2]
  else:
    print('Error in Q4_strain: output not recognized')
    raise Exception
