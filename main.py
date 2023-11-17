from Plotter import Plotter
from TrapezoidalProfile import TrapezoidalProfile
from SmoothedTrapezoidalProfile import SmoothedTrapezoidalProfile
import matplotlib.pyplot as plt

time_step = 0.01

# Create a grapher object
grapher = Plotter(TrapezoidalProfile(1))

# Plot the graph
grapher_data = grapher.plot(0, 3, -1, time_step, padding=[2, 2])
# this is done to add x - time steps.
plt.plot([i * time_step for i in range(len(grapher_data))], grapher_data)

#plot other data
smoothed_grapher = Plotter(SmoothedTrapezoidalProfile(1, 1))
# done for same reason as above
smoothed_data = smoothed_grapher.plot(0, 3, -1, time_step, padding=[2, 2])
plt.plot([i * time_step for i in range(len(smoothed_data))], smoothed_data)

# Plot the graph
plt.show()