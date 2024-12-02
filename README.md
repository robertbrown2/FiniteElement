# FiniteElement
Code repository for ENGR 435 at ACU

# Import into Google Colab/JupyterLab
```
from os.path import exists

if (exists('FiniteElement/README.md')):

  print('Import already completed')
  
else:

  !git clone https://github.com/robertbrown2/FiniteElement.git
```
# Usage
## Step 0 - Import
I recommend importing as follows:
```
import numpy as np
import FiniteElement.LST as LST
import FiniteElement.common as FE
```
Obviously, you do you, but the rest of the usage will assume that you followed this.

Note: Q4 is currently defunct, but I haven't deleted the code in case I want to come back and implement it.  Just use triangles for now.

## Step 1 - Mesh
To create a mesh, you need some nodes and a cell-to-node connectivity list.

Nodes are set up in two separate lists: xnode and ynode

The connectivity list should be a list of lists, either nNode x 3 for triangular elements or nNode x 4 for quadrilateral elements.

As an example, a small mesh on a square would appear as follows:
```
xnode = [0, 1, 1, 0, 0.5]
ynode = [0, 0, 1, 1, 0.5]
conn = [[1, 2, 5],
        [2, 3, 5],
        [3, 4, 5],
        [4, 1, 5]]
```

Elements should always be defined counter-clockwise.

## Step 2 - Boundary Conditions
After the mesh is made, boundary conditions can be set up.

Create boundary conditions using the `BC` class, then append them to a list, as follows:
```
bcs = []
bcs.append(FE.BC(geom='line', nodes=[2, 3], kind='convection', value=20, coefficient=1000))
bcs.append(FE.BC(geom='point', nodes=[1], kind='temperature', value=50))
```
The first BC created here will apply convection on the line between nodes 2 and 3.  The `value` is the ambient temperature $T_\infty$ in this case, while the `coefficient` is the film coefficient $h$.

The second BC applies a temperature constraint of $T=50$ to node 1.

You can also apply boundary conditions to a face:
```
bcs.append(FE.BC(geom='face', nodes=[1, 2, 5], kind='flow', value=20))
```

This will apply a total heat flow of 20 to the face.

Other options:
 - `kind='flux'` - applies a heat flux (flow per unit area) to a line or face.  If applied to a line, the thickness is used to calculate the result.
 - Varied loads: NumPy polynomials and user defined functions can also be used for `value` and `coefficient`.  For instance, if you want to calculate the convection heat transfer on a heated flat plate subject to air flow, you can set the `coefficient` as:
```
coefficient = lambda x, y : k_air * 0.0296 * (rho_air * V_air * x / mu_air)**0.8 / x * Pr_air ** (1/3)
```
User defined functions must always use both x and y as variables, even if only one is needed.

If you wanted to set up a triangular load on a line, it is probably easier to use a NumPy polynomial:
```
value = np.polynomial.Polynomial([100, -100])
```
This would set the value on the first node to 100, and the value on the second node to 0.  Essentially, the length of the line is normalized so that value(0) occurs at on the first node and value(1) occurs on the second.

Note that NumPy polynomials can only be used on lines.

## Step 3 (optional) - Refine Mesh
You can refine your mesh as many times as you like.  Every element will be subdivided into 4 equal-area similar elements, and any boundary conditions will be likewise divided to appropriate lines or faces.

Suggested usage is as follows:
```
nRefine = 5
c2l = []
l2n = []

for i in range(nRefine):
  [xnode, ynode, conn, bcs, c2l, l2n] = FE.meshRefine(xnode, ynode, conn, bcs, c2l, l2n)
```

The c2l and l2n lists are cell-to-line and line-to-node lists, respectively.  These are used internally, and should be assigned empty lists prior to refining.

## Step 4 - Create midpoints for LST elements
Once the mesh is refined appropriately, it should be converted to an LST mesh.  This is done through the `LST_mesh` function:
```
[xnode, ynode, conn, l2n, bcs] = LST.LST_mesh(xnode, ynode, conn, c2l, l2n, bcs)
```
## Step 5 - Set up element thickness and constituitive matrices
This can be done essentially at any point prior to this, but we also need to define the thickness and thermal conductivity of each of our elements.  Here's an example:
```
type2D = 'diffusion'

# Define material properties
thermalConductivity = 12
thickness = .1
D = FE.constMatrix(k=thermalConductivity, type2D = type2D)
```

## Step 6 - Create Stiffness Matrix
The stiffness matrix is the core of the process.  Because the element is non-linear, we need to integrate using Gaussian quadrature.  The `FE.quadpoints` function creates a list of appropriate points and weights.  A precision of 3 is sufficient for LST elements.

The `LST.LST_stiffness` function creates a 6x6 element stiffness matrix, based on values calculated at the Gaussian quadrature points supplied.  Once integrated, that matrix is added to the correct locations in the global stiffness matrix in the assembly process.
```
gaussPoints = FE.quadPoints(geom='triangle', precision=3)

# Create global K matrix
nNode = len(xnode)
nDOF = FE.nDOF(type2D)
kg = zeros((nNode*nDOF, nNode*nDOF))
for i, nodes in enumerate(conn):

  xElem = []
  yElem = []
  # Get x and y locations
  for node in nodes:
    xElem.append(xnode[node-index])
    yElem.append(ynode[node-index])

  k_elem = zeros((6*nDOF, 6*nDOF))
  for i, gP in enumerate(gaussPoints.points):
    weight = gaussPoints.weights[i]
    # Calculate K Matrix
    k_elem += LST.LST_stiffness(xElem, yElem, gP[0], gP[1], D, thickness, type2D) * weight
  
  # Assembly
  iDOF = []
  for node in nodes:
    for j in range(nDOF):
      iDOF.append((node-index)*nDOF + j)

  for j in range(len(iDOF)):
    for k in range(len(iDOF)):
      kg[iDOF[j], iDOF[k]] += k_elem[j, k]
```
## Step 7 - Apply Boundary Conditions
After the stiffness matrix is created, we apply boundary conditions as follows:
```
[kg, forces] = FE.applyBCs(kg, bcs, xnode, ynode, thickness, type2D, index)
```

## Step 8 - Solve
Finally, we solve using NumPy:
```
temperatures = np.linalg.solve(kg, forces)
```

## Step 9 - Plot
And plot with matplotlib:
```
LST.LST_plot(conn, xnode, ynode, temperatures, D, 
             type2D='diffusion', output='T', nPlot = 2, 
             undeformedLines=False, nodeNumbers=False, 
             colormap = 'jet', minMax=[20, 30]
            )
```
 - `output` can be set to `T` for temperature or to `qx` or `qy` for heat flux in the x and y directions.  
 - `nPlot` specifies how many values to plot along each line (2 or 3 is usually sufficient)
 - `undeformedLines` will display the mesh if set to `True`
 - `nodeNumbers` will show all of the node numbers if set to `True`
 - `colormap` chooses the colors used for the plot (standard matplotlib options)
 - `minMax` determines the minimum and maximum values for the colorbar.  If omitted, will automatically be set to the minimum and maximum values in the mesh.