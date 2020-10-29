''' Library containing functions and information to run an oven simulation'''

import matplotlib.pyplot as plt
import numpy as np

class Body(object):
    def __init__(self, T0, volume, mat, debug):
        self.temp = T0
        self.mat = mat
        self.volume = volume
        self.step_heat = 0
        self.debug = debug

    def add_flux(self, flux):
        self.step_heat += flux

    def time_step(self, step):
        thermal_mass = self.volume*self.mat.density(self.temp)*self.mat.heat_capacity(self.temp)
        if self.debug:
            print(self.temp, thermal_mass, self.step_heat)
        self.temp += self.step_heat/thermal_mass*step
        self.step_heat = 0 

class Solid(Body):
    def __init__(self,T0, volume, mat, thickness, debug=False):
        Body.__init__(self, T0, volume, mat, debug)
        self.thickness = thickness

    def htc(self):
        #print(2.0*self.mat.thermal_cond(self.temp)/self.thickness)
        return 2.0*self.mat.thermal_cond(self.temp)/self.thickness

class Gas(Body):   
    def __init__(self, T0, volume, mat, velo, length, debug=False):
        Body.__init__(self, T0, volume, mat, debug)
        self.velo = velo
        self.length = length

    def htc(self):
        return 25
        ''' Using corrleations - switched to fixed values taken from Carson et al 2006
        re = self.mat.density(self.temp)*self.velo*self.length/(self.mat.viscosity(self.temp))
        pr = self.mat.prandtl(self.temp)
        #print re, self.length
        
        if re > 10**5:
            #print self.mat.thermal_cond(self.temp)/self.length * (0.037*re**0.8-871)*pr**0.333
            return self.mat.thermal_cond(self.temp)/self.length * \
                (0.037*re**0.8-871)*pr**0.333

        else:
            #print self.mat.thermal_cond(self.temp)/self.length * 2*0.3387*re**0.5*pr**0.333*(1-(0.0468/pr)**0.667)**-0.25 
            return self.mat.thermal_cond(self.temp)/self.length * \
                2*0.3387*re**0.5*pr**0.333/((1-(0.0468/pr)**0.667)**0.25) 
        '''

class Surroundings(Body):
    def __init__(self, T0, htc):
        Body.__init__(self, T0, 0, 0, False)
        self.htc_num = htc

    def htc(self):
        return self.htc_num

    def time_step(self, step):
        return 

class Exchanger(object):
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

class HeatExchange(Exchanger):
    def __init__(self, obj1, obj2, area):
        Exchanger.__init__(self, obj1, obj2)
        self.area = area
    
    def calc_flux(self):
        htc1 = self.obj1.htc()
        htc2 = self.obj2.htc()
        overall_HTC = (htc1**-1+htc2**-1)**-1
        #print type(self.obj1), htc1, type(self.obj2), htc2, overall_HTC
        if overall_HTC < 0:
            print("Error, negative HTC:", overall_HTC)

        flux = -overall_HTC*self.area*(self.obj1.temp-self.obj2.temp)
        self.obj1.add_flux(flux)
        self.obj2.add_flux(-flux)

class MassExchange(Exchanger):
    def __init__(self, obj1, obj2, flowrate):
        Exchanger.__init__(self, obj1, obj2)
        self.flowrate = flowrate

    def calc_flux(self):
        flux = self.flowrate*(self.obj1.mat.heat_capacity(self.obj1.temp)*self.obj1.temp-
                              self.obj2.mat.heat_capacity(self.obj2.temp)*self.obj2.temp)

        self.obj1.add_flux(-flux)
        self.obj2.add_flux(+flux)

class Air(object):
    def viscosity(self, temp):
        return 1.716*10**-5 *(temp/273.15)**1.5*(273.15+110.4)/(temp+110.4)

    def heat_capacity(self,temp):
        return 1000

    def thermal_cond(self,temp):
        return 2.428*10**-2 *(temp/273.15)**1.5*(273.15+110.4)/(temp+110.4)

    def prandtl(self, temp):
        return self.heat_capacity(temp)*self.viscosity(temp)/self.thermal_cond(temp)

    def density(self,temp):
        return 100000.0/(287.0*temp)

class Steel(object):
    def viscosity(self, temp):
        return False
    
    def heat_capacity(self, temp):
        return 490 

    def thermal_cond(self, temp):
        return 40

    def prandtl(self, temp):
        return False
    
    def density(self, temp):
        return 7700

class RockWool(object):
    def viscosity(self, temp):
        return False
    
    def heat_capacity(self, temp):
        return 2100

    def thermal_cond(self, temp):
        return 0.038

    def prandtl(self, temp):
        return False
    
    def density(self, temp):
        return 50

class Hipor(object):
    def viscosity(self, temp):
        return False
    
    def heat_capacity(self, temp):
        return 4200

    def thermal_cond(self, temp):
        return 0.6

    def prandtl(self, temp):
        return False
    
    def density(self, temp):
        return 1000

class Door(object):
    def viscosity(self, temp):
        return False
    
    def heat_capacity(self, temp):
        return 1500

    def thermal_cond(self, temp):
        return 0.36

    def prandtl(self, temp):
        return False
    
    def density(self, temp):
        return 750
