import fedoo as fd
import numpy as np

# Parameters
L = 100  #
n_nodes = 11  # number of nodes
bc_type = 1  # 1 for displacement BC, 2 for stress BC

# Build mesh
mesh = fd.mesh.rectangle_mesh(n_nodes, n_nodes, 0, L, 0, L)

# Create a 2D modeling space
fd.ModelingSpace("2Dstress")

# Unidirectional composite material law
ldc = fd.constitutivelaw.CompositeUD(
    Vf=0.6,  # fiber volume fraction
    E_f=250000,  # fiber elasticity modulus
    E_m=3500,  # matrix elasticity modulus
    nu_f=0.33,  # fiber Poisson ratio
    nu_m=0.3,  # matrix Poisson ratio
    angle=45,  # inplane orientation angle in degree
)

# Set the equation and problem to solve (static equilibrium)
wf = fd.weakform.StressEquilibrium(ldc)
assembly = fd.Assembly(wf, mesh)

# Extract node sets for boundary conditions
left = mesh.find_nodes("X", mesh.bounding_box.xmin)
right = mesh.find_nodes("X", mesh.bounding_box.xmax)

# Apply boundary conditions
if bc_type == 1:
    pb = fd.problem.Linear(assembly)
    pb.bc.add("Dirichlet", left, "DispX", 0)  # clamped on left
    pb.bc.add("Dirichlet", right, "DispX", 100)  # x displacement on right
else:  # bc_type == 2
    # apply pressure on the right and left boundaries
    # rigid body motion are not constrained
    pressure1 = fd.constraint.Pressure.from_nodes(mesh, right, -1e5)
    pressure2 = fd.constraint.Pressure.from_nodes(mesh, left, -1e5)
    pb = fd.problem.Linear(assembly + pressure1 + pressure2)

# Solve
pb.solve()

# Extract and plot some results
res = pb.get_results(assembly, ["Stress", "Strain", "Disp"])

# Plot von-mises stress
res.plot("Strain", "XX", "Node")
# 'Node' is used to average field values at nodes

# Plot XX stress component :
# res.plot('Stress', 'XX')

# Get the XX stress values at nodes (numpy array)
# stress_xx = res['Stress', 'XX', 'Node']
