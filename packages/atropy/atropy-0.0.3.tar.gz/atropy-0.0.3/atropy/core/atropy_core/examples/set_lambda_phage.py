"""Script for setting the initial conditions for the lambda phage model."""

import argparse
import sys

import numpy as np
from scipy.special import factorial

import atropy_core.examples.models.lambda_phage as model
from atropy_core.grid import GridParms
from atropy_core.index_functions import incrVecIndex, tensorUnfold, vecIndexToState
from atropy_core.initial_condition import InitialCondition
from atropy_core.tree import Tree

partition = ["(0 1)((2 3)(4))", "((0 1)(2 3))(4)", "((0 1)(2))(3 4)", "(0 1)(2 3 4)"]

parser = argparse.ArgumentParser(
    prog="set_lambda_phage",
    usage='python3 atropy_core/examples/set_lambda_phage.py --partition "'
    + partition[0]
    + '" --rank 5 5',
    description="This script sets the initial conditions for the lambda phage model.",
)

for i, p in enumerate(partition):
    parser.add_argument(
        "-p" + str(i),
        "--partition" + str(i),
        action="store_const",
        const=p,
        required=False,
        help="Set the partition string to " + p,
        dest="partition",
    )
parser.add_argument(
    "-r",
    "--rank",
    nargs="+",
    type=int,
    required=True,
    help="Specify the ranks of the internal node",
)
args = parser.parse_args()

if args.partition is None:
    print("usage:", parser.usage)
    print(
        parser.prog + ":",
        "error: the following arguments are required: -p[n]/--partition[n], n=0,...,"
        + str(len(partition) - 1),
    )
    sys.exit(1)

partition_str = args.partition
r_out = np.array(args.rank)
n_basisfunctions = np.ones(r_out.size, dtype="int")

# Grid parameters
n = np.array([16, 41, 11, 11, 11])
d = n.size
binsize = np.ones(d, dtype=int)
liml = np.zeros(d)
grid = GridParms(n, binsize, liml)

# Set up the partition tree
tree = Tree(partition_str, grid)
tree.initialize(model.reaction_system, r_out)


# Initial distribution
def multinomial(x):
    abs_x = np.sum(x)
    if abs_x <= 3:
        p0 = (
            factorial(3)
            * (0.05**abs_x)
            * ((1.0 - 5 * 0.05) ** (3 - abs_x))
            / (np.prod(factorial(x)) * factorial(3 - abs_x))
        )
    else:
        p0 = 0.0
    return p0


# Helper function for factorizing a low-rank factor
def factorizeLRFactor(x, node):
    x_tensor = np.zeros(
        (node.child[0].grid.dx(), node.child[1].grid.dx(), node.rankIn())
    )
    for i in range(node.rankIn()):
        x_tensor[:, :, i] = x[:, i].reshape(
            (node.child[0].grid.dx(), node.child[1].grid.dx()), order="F"
        )

    x_mat = tensorUnfold(x_tensor, 0)
    u, _, _ = np.linalg.svd(x_mat, full_matrices=False)
    x0 = u[:, : node.child[0].rankIn()]

    x_mat = tensorUnfold(x_tensor, 1)
    u, _, _ = np.linalg.svd(x_mat, full_matrices=False)
    x1 = u[:, : node.child[1].rankIn()]

    q = np.einsum("ik,jl,ijm", x0, x1, x_tensor)

    return q, x0, x1


p0 = np.zeros(grid.dx())
vec_index = np.zeros(grid.d())
for i in range(grid.dx()):
    state = vecIndexToState(vec_index, grid.liml, grid.binsize)
    p0[i] = multinomial(state + (grid.binsize - 1.0) * 0.5)
    incrVecIndex(vec_index, grid.n, grid.d())

p0_mat = p0.reshape(
    (tree.root.child[0].grid.dx(), tree.root.child[1].grid.dx()), order="F"
)

# SVD of p0
u, s, vh = np.linalg.svd(p0_mat, full_matrices=False)

# Use only the first `r` singular values
x0 = u[:, : tree.root.rankOut()]
q = np.diag(s[: tree.root.rankOut()])
x1 = vh[: tree.root.rankOut(), :].T

# SVD of x0
if partition_str is partition[0]:
    q1, x10, x11 = factorizeLRFactor(x1, tree.root.child[1])

elif partition_str is not partition[3]:
    q0, x00, x01 = factorizeLRFactor(x0, tree.root.child[0])

# Number of basisfunctions
n_basisfunctions = r_out

# Low-rank initial conditions
initial_conditions = InitialCondition(tree, n_basisfunctions)

if partition_str is partition[3]:
    initial_conditions.Q[0][:, :, 0] = q
    initial_conditions.X[0][:] = x0
    initial_conditions.X[1][:] = x1

    x0_sum = np.sum(x0, axis=0)
    x1_sum = np.sum(x1, axis=0)
elif partition_str is partition[0]:
    initial_conditions.Q[0][:, :, 0] = q
    initial_conditions.Q[1][:] = q1
    initial_conditions.X[0][:] = x0
    initial_conditions.X[1][:] = x10
    initial_conditions.X[2][:] = x11

    x10_sum = np.sum(x10, axis=0)
    x11_sum = np.sum(x11, axis=0)
    x0_sum = np.sum(x0, axis=0)
    x1_sum = np.array([x10_sum @ q1[:, :, i] @ x11_sum.T for i in range(r_out[0])])
else:
    initial_conditions.Q[0][:, :, 0] = q
    initial_conditions.Q[1][:] = q0
    initial_conditions.X[0][:] = x00
    initial_conditions.X[1][:] = x01
    initial_conditions.X[2][:] = x1

    x00_sum = np.sum(x00, axis=0)
    x01_sum = np.sum(x01, axis=0)
    x0_sum = np.array([x00_sum @ q0[:, :, i] @ x01_sum.T for i in range(r_out[0])])
    x1_sum = np.sum(x1, axis=0)

norm = x0_sum @ q @ x1_sum.T
print("norm:", norm)

# Print tree and write it to a netCDF file
print(tree)
tree.write()
