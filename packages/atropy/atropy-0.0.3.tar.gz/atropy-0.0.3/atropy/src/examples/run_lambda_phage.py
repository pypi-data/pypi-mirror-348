import matplotlib.pyplot as plt
import numpy as np
from atropy_core.index_functions import incrVecIndex, tensorUnfold, vecIndexToState
from atropy_core.output_helper import TimeSeries
from scipy.special import factorial

from atropy.src.generator import Model, Partitioning, run, species

# Partitition p0, rank 5 4
# Snapshot 100, tau 1e-3, final_time 1, rest default

"""
Define variables
"""
S0, S1, S2, S3, S4 = species("S0, S1, S2, S3, S4")


"""
Generate model
"""
model = Model((S0, S1, S2, S3, S4))

a0 = 0.5
a1 = 1.0
a2 = 0.15
a3 = 0.3
a4 = 0.3

b0 = 0.12
b1 = 0.6
b2 = 1.0
b3 = 1.0
b4 = 1.0

c0 = 0.0025
c1 = 0.0007
c2 = 0.0231
c3 = 0.01
c4 = 0.01

### Full reaction generation:

# model.add_reaction(0, S1, {S2: a0 * b0 / (b0 + S2)})
# model.add_reaction(0, S2, {S1: b1 / (b1 + S1), S5: a1 + S5})
# model.add_reaction(0, S3, {S2: a2 * b2 * S2 / (b2 * S2 + 1.0)})
# model.add_reaction(0, S4, {S3: a3 * b3 * S3 / (b3 * S3 + 1.0)})
# model.add_reaction(0, S5, {S3: a4 * b4 * S3 / (b4 * S3 + 1.0)})
# model.add_reaction(S1, 0, {S1: c0 * S1})
# model.add_reaction(S2, 0, {S2: c1 * S2})
# model.add_reaction(S3, 0, {S3: c2 * S3})
# model.add_reaction(S4, 0, {S4: c3 * S4})
# model.add_reaction(S5, 0, {S5: c4 * S5})


### Shorter reaction generation:

model.add_reaction(0, S0, {S1: a0 * b0 / (b0 + S1)})
model.add_reaction(0, S1, {S0: b1 / (b1 + S0), S4: a1 + S4})
model.add_reaction(0, S2, {S1: a2 * b2 * S1 / (b2 * S1 + 1.0)})
model.add_reaction(0, S3, {S2: a3 * b3 * S2 / (b3 * S2 + 1.0)})
model.add_reaction(0, S4, {S2: a4 * b4 * S2 / (b4 * S2 + 1.0)})
model.add_reaction(S0, 0, c0)
model.add_reaction(S1, 0, c1)
model.add_reaction(S2, 0, c2)
model.add_reaction(S3, 0, c3)
model.add_reaction(S4, 0, c4)

model.generate_reaction_system()


"""
Generate tree and initial condition
"""
r = np.array([5, 4])
p0 = "(S0 S1)((S2 S3)(S4))"
partitioning = Partitioning(p0, r, model)

n = np.array([16, 41, 11, 11, 11])
d = n.size
binsize = np.ones(d, dtype=int)
liml = np.zeros(d)
partitioning.add_grid_params(n, binsize, liml)

partitioning.generate_tree()


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


p0 = np.zeros(partitioning.grid.dx())
vec_index = np.zeros(partitioning.grid.d())
for i in range(partitioning.grid.dx()):
    state = vecIndexToState(
        vec_index, partitioning.grid.liml, partitioning.grid.binsize
    )
    p0[i] = multinomial(state + (partitioning.grid.binsize - 1.0) * 0.5)
    incrVecIndex(vec_index, partitioning.grid.n, partitioning.grid.d())

p0_mat = p0.reshape(
    (
        partitioning.tree.root.child[0].grid.dx(),
        partitioning.tree.root.child[1].grid.dx(),
    ),
    order="F",
)

# SVD of p0
u, s, vh = np.linalg.svd(p0_mat, full_matrices=False)

# Use only the first `r` singular values
x0 = u[:, : partitioning.tree.root.rankOut()]
q = np.diag(s[: partitioning.tree.root.rankOut()])
x1 = vh[: partitioning.tree.root.rankOut(), :].T

# SVD of x0
q1, x10, x11 = factorizeLRFactor(x1, partitioning.tree.root.child[1])  # This because p0

# Number of basisfunctions
n_basisfunctions = r

# Low-rank initial conditions
partitioning.generate_initial_condition(n_basisfunctions)

partitioning.initial_conditions.Q[0][:, :, 0] = q
partitioning.initial_conditions.Q[1][:] = q1
partitioning.initial_conditions.X[0][:] = x0
partitioning.initial_conditions.X[1][:] = x10
partitioning.initial_conditions.X[2][:] = x11

x10_sum = np.sum(x10, axis=0)
x11_sum = np.sum(x11, axis=0)
x0_sum = np.sum(x0, axis=0)
x1_sum = np.array([x10_sum @ q1[:, :, i] @ x11_sum.T for i in range(r[0])])

norm = x0_sum @ q @ x1_sum.T
print("norm:", norm)


print(partitioning.tree)


"""
write input file and run
"""
run(partitioning, "output_lambda_phage", 1e-3, 10, snapshot=10, method="implicit_Euler")


"""
Do the plotting
"""

time_series = TimeSeries("output_lambda_phage")
concentrations = time_series.calculateMoments()
t = time_series.time

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4))
deviation = {
    key: np.sqrt(concentrations[1][key] - concentrations[0][key] ** 2)
    for key in concentrations[0]
}
observables = ["S0", "S1"]
observables_alt = ["$S_0$", "$S_1$", "$S_2$"]
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
for i, (o, o_alt) in enumerate(zip(observables, observables_alt, strict=False)):
    ax1.plot(t, concentrations[0][o], "-", label=o_alt, color=colors[i], alpha=0.7)
    ax1.fill_between(
        t,
        concentrations[0][o] - deviation[o],
        concentrations[0][o] + deviation[o],
        color=colors[i],
        alpha=0.2,
    )
ax1.set_ylabel("$\\langle x_i(t) \\rangle$")
ax1.set_ylim([0.0, 20.0])

observables = ["S2", "S3", "S4"]
observables_alt = ["$S_2$", "$S_3$", "$S_4$"]
for idx_o, (o, o_alt) in enumerate(zip(observables, observables_alt, strict=False)):
    i = idx_o + 2
    ax2.plot(t, concentrations[0][o], "-", label=o_alt, color=colors[i], alpha=0.7)
    ax2.fill_between(
        t,
        concentrations[0][o] - deviation[o],
        concentrations[0][o] + deviation[o],
        color=colors[i],
        alpha=0.2,
    )
ax2.set_ylabel("$\\langle x_i(t) \\rangle$")
ax2.set_ylim([0, 2.5])
ax2.yaxis.tick_right()
ax2.yaxis.set_ticks_position("both")
ax2.yaxis.set_label_position("right")
plt.setp((ax1, ax2), xlabel="$t$", xlim=[0.0, 10.0], xticks=[0.0, 2.5, 5.0, 7.5, 10.0])

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = (sum(ll, []) for ll in zip(*lines_labels, strict=False))
fig.legend(lines, labels, ncols=5, loc="upper center")

plt.savefig("plots/lambda_phage_concentrations.pdf")
