def LST_strain(xElem, yElem, u, xi, eta, type2D='planeStress', output=None):
  from numpy import array
  """
  Output the strain at a point in the triangle.
  Usage: eps = array([epsx, epsy, tauxy]) = LST_strain(xElem, yElem, u, xi, eta, type2D='planeStress', output=None)
  ---------
    Input
  ---------
  xElem - (list) x locations of nodes
  yElem - (list) y locations of nodes
  u - (list) deformation of nodes [u1, v2, u2, v2, u3, v3, u4, v4, u5, v5, u6, v6]
  xi, eta - (float) location on unmapped element
  ----------
    Output
  ----------
  eps: (array) contains [epsx, epsy, tauxy]
  epsx: (float) normal strain in x direction
  epsy: (float) normal strain in y direction
  tauxy: (float) shear strain
  """
  from .LST_B import LST_B
  from numpy import any, max

  # If a value in x goes to 0, it breaks the axisymmetric stress.
  if type2D == 'axisymmetric' and any(xElem < max(xElem) * 1e-3):
    for i, x in xElem:
      if xElem[i] < max(xElem) * 1e-3:
        xElem[i] = max(xElem) * 1e-3
  
  B = LST_B(xElem, yElem, xi, eta, type2D)
  
  eps = B @ array(u)
  if (output == None):
    return eps
  elif (output == 'epsx' or output == 'epsr'):
    return eps[0]
  elif (output == 'epsy' or output == 'epsz'):
    return eps[1]
  elif (output == 'gammaxy' or output == 'epsth'):
    return eps[2]
  elif (output == 'gammarz' and type2D == 'axisymmetric'):
    return eps[3]
  else:
    print('Error in Q4_strain: output not recognized')
    raise Exception
