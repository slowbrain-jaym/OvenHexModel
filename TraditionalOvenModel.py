import matplotlib.pyplot as plt
import numpy as np
from BodyModelling import *

rockwool = RockWool()
steel = Steel()
air = Air()
hipor = Hipor()
door = Door()

bodies = {}
bodies['fanair'] = Gas(290, 0.002, air, 50, 0.1)
bodies['ovenair'] = Gas(290, 0.05, air, 5, 0.25)
bodies['fanshroud'] = Solid(290, 0.00006, steel, 0.001)
bodies['ovenback'] = Solid(290, 0.00012, steel, 0.001)
bodies['ovenbackinsulation'] = Solid(290, 0.0024, rockwool, 0.02)
bodies['ovenbackouter'] = Solid(290, 0.00012, steel, 0.001)
bodies['food'] = Solid(290, 0.0036, hipor, 5)
bodies['ovenwalls'] = Solid(290, 0.00072, steel, 0.001)
bodies['oveninsulation'] = Solid(290, 0.0144, rockwool, 0.02)
bodies['ovenouter'] = Solid(290, 0.00072, steel, 0.001)
bodies['ovendoor'] = Solid(290, 0.006, door, 0.03)
bodies['outsideair'] = Surroundings(290, 50)
bodies['outsideairback'] = Surroundings(290, 50)


exchangers = []
exchangers.append(MassExchange(bodies['fanair'], bodies['ovenair'], 0.002))
exchangers.append(HeatExchange(bodies['fanair'], bodies['ovenback'], 0.06))
exchangers.append(HeatExchange(bodies['fanair'], bodies['fanshroud'], 0.06))
exchangers.append(HeatExchange(bodies['ovenback'], bodies['ovenbackinsulation'], 0.2))
exchangers.append(HeatExchange(bodies['ovenbackinsulation'], bodies['ovenbackouter'], 0.2))
exchangers.append(HeatExchange(bodies['ovenback'], bodies['ovenair'], 0.06))
exchangers.append(HeatExchange(bodies['fanshroud'], bodies['ovenair'], 0.06))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['food'], 0.13))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['ovenwalls'], 0.72))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['ovendoor'], 0.2))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['ovenback'], 0.2-0.06))
exchangers.append(HeatExchange(bodies['ovenwalls'], bodies['oveninsulation'], 0.72))
exchangers.append(HeatExchange(bodies['oveninsulation'], bodies['ovenouter'], 0.72))
exchangers.append(HeatExchange(bodies['ovenouter'], bodies['outsideair'], 0.72))
exchangers.append(HeatExchange(bodies['ovenbackouter'], bodies['outsideairback'], 0.72))
exchangers.append(HeatExchange(bodies['ovendoor'], bodies['outsideair'], 0.2))


step_time = 0.1
steps = 6000
step_count = 0
results = {}
for body in bodies:
    results[body] = []


while step_count<steps:
    #print "step: ", step_count
    bodies["fanair"].add_flux(2400)
    for exchanger in exchangers:
        exchanger.calc_flux()
    for body in bodies:
        results[body].append(bodies[body].temp-273)
        bodies[body].time_step(step_time)        
        #print body, bodies[body].temp
    step_count+=1

for body in bodies:
    print(body, results[body][-1])
    plt.plot(np.linspace(0,step_time*steps/60.0,steps),results[body],label=body)

plt.legend()
plt.show()

