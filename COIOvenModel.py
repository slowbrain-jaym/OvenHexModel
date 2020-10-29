import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from BodyModelling import *

rockwool = RockWool()
steel = Steel()
air = Air()
chicken = Chicken()
door = Door()

bodies = {}
bodies['jetsair'] = Gas(290, 0.002, air, 35)
bodies['impingementair'] = Gas(290, 0.002, air, 35)
bodies['ovenair'] = Gas(290, 0.05, air, 15)
bodies["ductair"] = Gas(290, 0.002, air, 15)
bodies["jetsductwork"] = Solid(290, 0.00006, steel, 0.001)
bodies['backductwork'] = Solid(290, 0.00006, steel, 0.001)
bodies['ovenback'] = Solid(290, 0.00012, steel, 0.001)
bodies['ovenbackinsulation'] = Solid(290, 0.0024, rockwool, 0.02)
bodies['ovenbackouter'] = Solid(290, 0.00012, steel, 0.001)

#bodies['food'] = Solid(277, 0.0036, chicken, 0.04) # chicken
bodies['food'] = Solid(277, 0.00071, chicken, 0.005) # pizza


bodies['ovenwalls'] = Solid(290, 0.00072, steel, 0.001)
bodies['oveninsulation'] = Solid(290, 0.0144, rockwool, 0.02)
bodies['ovenouter'] = Solid(290, 0.00072, steel, 0.001)
bodies['ovendoor'] = Solid(290, 0.006, door, 0.03)
bodies['outsideair'] = Surroundings(290, 50)
bodies['outsideairback'] = Surroundings(290, 50)

mixing_ratio = 0.5# amount of jetsair in impingmentair

exchangers = []
exchangers.append(MassExchange(bodies['jetsair'], bodies['ovenair'], 0.002))
exchangers.append(MassExchange(bodies['ovenair'], bodies['ductair'], 0.002))
exchangers.append(MassExchange(bodies['ductair'], bodies['jetsair'], 0.002))

exchangers.append(MassExchange(bodies['jetsair'], bodies['impingementair'], 0.002*mixing_ratio))
exchangers.append(MassExchange(bodies['ovenair'], bodies['impingementair'], 0.002*(1-mixing_ratio)))
exchangers.append(MassExchange(bodies['impingementair'], bodies['ovenair'], 0.002))

exchangers.append(HeatExchange(bodies['ductair'], bodies['ovenback'], 0.06))
exchangers.append(HeatExchange(bodies['ductair'], bodies['backductwork'], 0.06))

exchangers.append(HeatExchange(bodies['ovenair'], bodies['backductwork'], 0.06))

exchangers.append(HeatExchange(bodies['jetsair'], bodies['jetsductwork'], 0.06))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['jetsductwork'], 0.06))

exchangers.append(HeatExchange(bodies['ovenback'], bodies['ovenbackinsulation'], 0.12))
exchangers.append(HeatExchange(bodies['ovenbackinsulation'], bodies['ovenbackouter'], 0.12))
exchangers.append(HeatExchange(bodies['ovenback'], bodies['ovenair'], 0.06))
exchangers.append(HeatExchange(bodies['impingementair'], bodies['food'], 0.13))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['ovenwalls'], 0.344))
exchangers.append(HeatExchange(bodies['ovenwalls'], bodies['oveninsulation'], 0.344))
exchangers.append(HeatExchange(bodies['oveninsulation'], bodies['ovenouter'], 0.344))
exchangers.append(HeatExchange(bodies['ovenouter'], bodies['outsideair'], 0.344))
exchangers.append(HeatExchange(bodies['ovenback'], bodies['outsideairback'], 0.12))
exchangers.append(HeatExchange(bodies['ovendoor'], bodies['outsideair'], 0.2))
exchangers.append(HeatExchange(bodies['ovenair'], bodies['ovendoor'], 0.2))

step_time = 0.1
steps = 90000
step_count = 0
setpoint = 180+273
foodtarget = 100+273
power = 2400 #Watts
savename = "COI Oven Chicken Mixing0"
results = {}
results["time"] = []
results["energy"] = []
for body in bodies:
    results[body] = []


while step_count<steps and bodies["food"].temp<foodtarget:
    #print "step: ", step_count
    if(bodies['ovenair'].temp<setpoint):
        bodies["jetsair"].add_flux(2400)
        results["energy"].append(2400*step_time)
    else:
        results["energy"].append(0)
    for exchanger in exchangers:
        exchanger.calc_flux()
    for body in bodies:
        results[body].append(bodies[body].temp-273)
        bodies[body].time_step(step_time)        
        #print body, bodies[body].temp
    results["time"].append(step_time*step_count)
    step_count+=1

print("Cook complete at:",results["time"][-1]/60, "mins")
print("Energy consumption:",sum(results["energy"])/1000/3600,"kWhr")
for body in bodies:
    print(body, results[body][-1])
    plt.plot(results["time"],results[body],label=body)

results_df = pd.DataFrame(results)
results_df.to_csv(r"Results//"+savename+".csv")

plt.legend()
plt.show()