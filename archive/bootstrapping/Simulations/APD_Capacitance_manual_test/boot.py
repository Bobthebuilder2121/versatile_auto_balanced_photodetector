import numpy as np
import matplotlib.pyplot as plt

# load file
data = np.loadtxt("bootstrapping.txt", skiprows=1)

time = data[:, 0]
vout = data[:, 1]
vpbs = data[:, 2]
vnbs = data[:, 3]

# zoom window: 1.9 ms → 3.2 ms
mask = (time >= 1.9e-3) & (time <= 3.2e-3)

t = time[mask] * 1e3  # convert to ms
vout = vout[mask]
vpbs = vpbs[mask]
vnbs = vnbs[mask]

# plot
plt.figure()
plt.plot(t, vout, label="V(out)")
plt.plot(t, vpbs, label="V(pbs)")
plt.plot(t, vnbs, label="V(nbs)")

# maximize vertical axis
ymin = min(vout.min(), vpbs.min(), vnbs.min())
ymax = max(vout.max(), vpbs.max(), vnbs.max())
plt.ylim(ymin, ymax)

plt.xlabel("Time [ms]")
plt.ylabel("Voltage [V]")
plt.title("Rail-to-rail voltages during bootstrapping")
plt.legend()
plt.grid()

plt.show()