import fedoo as fd

# Parameters
E = 210000  # Young Modulus (MPa)
nu = 0.3  # Poisson ratio
L = 100  # Beam length (mm)
h = 10  # Beam height
w = 10  # Beam width
thickness = 2  # I beam flange and web thickness
size_elm = 0.4  # element size for beam profil
n_nodes=30  # number of nodes along beam axis

# Build Beam mesh
profil = fd.mesh.I_shape_mesh(h, w, thickness, thickness, size_elm)
mesh = fd.mesh.extrude(profil, L, n_nodes)

# Put beam axis along the first dimension
mesh.nodes[:,[0,2]] = mesh.nodes[:,[2,0]]

# Create a 3D modeling space
fd.ModelingSpace("3D")

# Elastic isotropic material law
ldc = fd.constitutivelaw.ElasticIsotrop(E, nu)

# Set the equation and problem to solve (static equilibrium)
wf = fd.weakform.StressEquilibrium(ldc)
assemb = fd.Assembly(wf, mesh)
pb = fd.problem.Linear(assemb)

# Extract node sets for boundary conditions
left = mesh.find_nodes('X', mesh.bounding_box.xmin)
right = mesh.find_nodes('X', mesh.bounding_box.xmax)


# Apply boundary conditions 
pb.bc.add('Dirichlet', left, 'Disp', 0)  # clamped on left
pb.bc.add('Dirichlet', right, 'DispY', -10) # x displacement on right

# Option: apply a constant stress instead of a displacement
# pb.bc.add(fd.constraint.SurfaceForce.from_nodes(mesh, right, [0,-200,0]))

# Solve
pb.solve()

# Extract and plot some results
res = pb.get_results(['Stress', 'Strain', 'Disp'])

# Plot von-mises stress
res.plot('Stress', 'vm', 'Node')
# 'Node' is used to average field values at nodes

# Plot XX stress component :
# res.plot('Stress', 'XX')

# Get the XX stress values at nodes (numpy array)
# stress_xx = res['Stress', 'XX', 'Node']

# Or use the viewer
# fd.viewer(res)
