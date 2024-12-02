def nDOF(type2D):
  """
  Diffusion has 1 DOF (T / concentration)
  Other solids currently have 2 DOF
  """
  if (type2D == 'diffusion'):
    return 1
  else:
    return 2
