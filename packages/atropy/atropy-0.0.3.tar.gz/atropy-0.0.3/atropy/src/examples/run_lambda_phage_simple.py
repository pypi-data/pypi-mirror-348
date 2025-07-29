import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from atropy_core.output_helper import TimeSeries

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


# Number of basisfunctions
n_basisfunctions = r

# Low-rank initial conditions
partitioning.generate_initial_condition(n_basisfunctions)


# polynomial dictionary for initial distribution
polynomials_dict = {
    S0: sp.exp(-S0**2),
    S1: sp.exp(-S1**2),
    S2: sp.exp(-S2**2),
    S3: sp.exp(-S3**2),
    S4: sp.exp(-S4**2),
}

partitioning.set_initial_condition(polynomials_dict)


# normalize
_, marginal_distribution = partitioning.tree.calculateObservables(
    np.zeros(partitioning.tree.root.grid.d(), dtype="int")
)
norm = np.sum(marginal_distribution[partitioning.tree.species_names[0]])
print("norm:", norm)
partitioning.tree.root.Q[0, 0, 0] /= norm


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

fig, ax = plt.subplots(figsize=(7, 4))

observables = ["S0", "S1", "S2", "S3", "S4"]
observables_alt = ["$S_0$", "$S_1$", "$S_2$", "$S_3$", "$S_4$"]
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
for i, (o, o_alt) in enumerate(zip(observables, observables_alt, strict=False)):
    ax.plot(t, concentrations[0][o], "-", label=o_alt, color=colors[i], alpha=0.7)
ax.set_ylabel("$\\langle x_i(t) \\rangle$")
ax.set_ylim([0.0, 12.0])

plt.setp(ax, xlabel="$t$", xlim=[0.0, 10.0],
         xticks=[0.0, 2.5, 5.0, 7.5, 10.0])

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = (sum(ll, []) for ll in zip(*lines_labels, strict=False))
fig.legend(lines, labels, ncols=5, loc="upper center")

plt.savefig("plots/lambda_phage_concentrations.pdf")
