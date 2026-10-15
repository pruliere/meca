import fedoo as fd
import functions
import numpy as np

n_cells_x = 1
n_cells_y = 1

# build mesh
mesh = functions.generate_composite_mesh(n_cells_x, n_cells_y, size=100, radius=40, nr=11, nt=11)

### build an heterogeneous constitutive law
material1 = fd.constitutivelaw.ElasticIsotrop(2e4, 0.3)
material2 = fd.constitutivelaw.ElasticIsotrop(1e5, 0.3)

material = fd.constitutivelaw.Heterogeneous(
    (material1, material2), ("matrix", "inclusion")
)
# the set of elemenst "matrix" and "inclusion" are defined in the object mesh
# and can directly be used in the boundary conditions.

###
### TO DO :
### Define the adapted modeling space
###

wf = fd.weakform.StressEquilibrium(material)

###
### TO DO : 
### Build the problem "pb" and apply CL
###

pb.solve()

res = pb.get_results(assembly, ['Stress', 'Strain', 'Disp'])
# res.plot('Stress', 'XX')
volume = mesh.bounding_box.volume

# Compute the mean stress
mean_stress = [mesh.integrate_field(
    res['Stress',comp])/volume for comp in ['XX', 'YY', 'XY']
]

###
### TO DO : 
### Also compute the mean strain field in 2D
###

###
### TO DO :
### Make 3 simulations with different BC (with a loop for instance)
### save the mean_stress and mean_strain for each load case
### and compute the homogeneized stiffness matrix
###
