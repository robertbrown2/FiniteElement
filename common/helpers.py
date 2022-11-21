def connIndex(conn):
  # Find the minimum index in a list of lists
  minVal = conn[0][0]
  for elem in conn:
    minVal = min(minVal, min(elem))
  return minVal

def sameLines(line1, line2):
  # Determine if two lists have the same nodes, even if they are in a different order
  # Specifically for lists that have two elements
  if (line1[0]==line2[0] and line1[1]==line2[1]):
    return True
  elif (line1[0]==line2[1] and line1[1]==line2[0]):
    return True
  else:
    return False

def whichLine(newLine, lineList, multiple=False):
  # Find the index of a line from a list of lines
  # Returns -1 if not found
  lines = []
  for i, oldLine in enumerate(lineList):
    if (sameLines(newLine, oldLine)):
      if (multiple):
        lines.append(i)
      else:
        return i
  if (multiple and len(lines)>0):
    return lines
  
  return None
