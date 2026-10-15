import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import fedoo as fd


def generate_composite_mesh(n_cells_x, n_cells_y, size=100, radius=40, nr=11, nt=11):
    mesh = fd.mesh.hole_plate_mesh(
        nr=11,
        nt=11,
        length=size,
        height=size,
        radius=radius,
        elm_type="quad4",
        name="Domain",
    )

    mesh.element_sets["matrix"] = np.arange(0, mesh.n_elements)

    mesh_disk = fd.mesh.disk_mesh(radius, 11, 11)
    mesh_disk.element_sets["inclusion"] = np.arange(0, mesh_disk.n_elements)

    mesh = mesh + mesh_disk

    # glue the inclusion to the matrix
    mesh.merge_nodes(np.c_[mesh.node_sets["hole_edge"], mesh.node_sets["boundary"]])

    length = mesh.bounding_box.size_x
    full_mesh = mesh
    for i in range(1, n_cells_x):
        new_mesh = mesh.deepcopy()
        new_mesh.nodes[:, 0] = new_mesh.nodes[:, 0] + i * length
        full_mesh = full_mesh + new_mesh

    mesh = full_mesh
    for i in range(1, n_cells_y):
        new_mesh = new_mesh = mesh.deepcopy()
        new_mesh.nodes[:, 1] = new_mesh.nodes[:, 1] + i * length
        full_mesh = full_mesh + new_mesh

    mesh = full_mesh
    mesh.merge_nodes(mesh.find_coincident_nodes())

    # Definition of the set of nodes for boundary conditions
    mesh.node_sets["left"] = mesh.find_nodes("X", mesh.bounding_box.xmin)
    mesh.node_sets["right"] = mesh.find_nodes("X", mesh.bounding_box.xmax)
    mesh.node_sets["top"] = mesh.find_nodes("Y", mesh.bounding_box.ymax)
    mesh.node_sets["bottom"] = mesh.find_nodes("Y", mesh.bounding_box.ymin)

    return mesh


def generate_laminate_mesh(n_cells_x, n_cells_y, size=100, nx=20, ny=20):
    mesh = fd.mesh.rectangle_mesh(
        nx=11,
        ny=11,
        x_max=size,
        y_max=size,
        elm_type="quad4",
    )

    mesh.element_sets["inclusion"] = mesh.find_elements("Y>30 and Y<70")
    mesh.element_sets["matrix"] = mesh.find_elements("Y<=30 or Y>=70")

    length = mesh.bounding_box.size_x
    full_mesh = mesh
    for i in range(1, n_cells_x):
        new_mesh = mesh.deepcopy()
        new_mesh.nodes[:, 0] = new_mesh.nodes[:, 0] + i * length
        full_mesh = full_mesh + new_mesh

    mesh = full_mesh
    for i in range(1, n_cells_y):
        new_mesh = new_mesh = mesh.deepcopy()
        new_mesh.nodes[:, 1] = new_mesh.nodes[:, 1] + i * length
        full_mesh = full_mesh + new_mesh

    mesh = full_mesh
    mesh.merge_nodes(mesh.find_coincident_nodes())

    # Definition of the set of nodes for boundary conditions
    mesh.node_sets["left"] = mesh.find_nodes("X", mesh.bounding_box.xmin)
    mesh.node_sets["right"] = mesh.find_nodes("X", mesh.bounding_box.xmax)
    mesh.node_sets["top"] = mesh.find_nodes("Y", mesh.bounding_box.ymax)
    mesh.node_sets["bottom"] = mesh.find_nodes("Y", mesh.bounding_box.ymin)

    return mesh


def plot_stiffness(C):

#    plt.rcParams["text.usetex"] = True
#    plt.rcParams["figure.figsize"] = (20, 8)

    n_points = 1000
    phi = np.linspace(
        0, 2 * np.pi, n_points
    )  # the angle of the projection in the xy-plane

    n_1 = np.cos(phi)
    n_2 = np.sin(phi)

    n = np.array([n_1 * n_1, n_2 * n_2, n_1 * n_2]).T
    S = (
        (n @ np.linalg.inv(C)).reshape(n_points, 1, 3) @ n.reshape(n_points, 3, 1)
    ).reshape(-1)

    E = 1.0 / S

    x = E * n_1
    y = E * n_2

    fig = plt.figure()  # Square figure
    plt.axis("equal")

    plt.plot(x, y)

    plt.show()
