import json
import math
from progress_logger import ProgressLogger
from commodities import *
import time

def do_nothing():
    pass

class System():
    def __init__(self,id,name,x,y,z,permit):
        self._name=name
        self._id=id
        self._x=x
        self._y=y
        self._z=z
        self._permit=permit
    def __str__(self):
        return self._name + " permit:"+str(self._permit)
    def fId(self,id):
        return id==self._id
    def getId(self):
        return self._id
    def getPermit(self):
        return self._permit
    def getName(self):
        return self._name
    def getXYZ(self):
        if self._name=="Sol":
            do_nothing()
        return (self._x , self._y , self._z)
    def calcualte_distance(self,system):
        otherXYZ=system.getXYZ()
        otherX,otherY,otherZ=otherXYZ
        xDiff=self._x-otherX
        yDiff=self._y-otherY
        zDiff=self._z-otherZ
        return math.sqrt(xDiff*xDiff+yDiff*yDiff+zDiff*zDiff)



class Station():
    def __init__(self,name,id,system_id,max_landing_pad,distance_to_star,planetary):
        self._name=name
        self._id=id
        self._system_id=system_id
        self._max_landing_pad=max_landing_pad
        self._distance_to_star=distance_to_star
        self._planetary=planetary
        self._commodities=[]
        self._system=None
    def __str__(self):
        if not self._system is None:
            return self._name + " in " + self._system.getName() + " MaxLadingPad=\""+self._max_landing_pad+"\" distance to star: " + str(self._distance_to_star)+ "Ls permit: " + \
                    str(self._system.getPermit()) + " planetary: " + str(self._planetary)
        else:
            return self._name + " in SYSTEM NOT ADDED WITH ID:" + str(self._system_id) + " MaxLadingPad=\"" + self._max_landing_pad + "\" distance to star: " + str(
                self._distance_to_star) + "Ls permit: " + \
                   str(True) + " planetary: " + str(self._planetary)
    #enddef
    def getId(self):
        return self._id
    def setSsytem(self,system):
        self._system=system
    def getName(self):
        return self._name
    def getSystem(self):
        return self._system
    def get_system_id(self):
        return self._system_id
    def get_max_landing_pad(self):
        return self._max_landing_pad
    def get_distance_to_star(self):
        return self._distance_to_star
    def get_permit(self):
        if self._system is None:
            return True
        else:
            return self._system.getPermit()
    def get_planetary(self):
        return self._planetary
    def get_commodities(self):
        return self._commodities
    def add_commodity(self,commodity):
        self._commodities.append(commodity)
    def find_commodity(self,commodity_name):
        for c in self._commodities:
            if c.getName()==commodity_name:
                return c
        return None
    def f_commodity_with_supply(self,commodity_name,supply):
        for c in self._commodities:
            if c.getName()==commodity_name and c.getSupply()>=supply:
                return c
        return None
    def print_with_all_commodities(self):
        print(str(self))
        for c in self._commodities:
            print("      "+str(c))

    def print_with_specified_commodities(self,commodities_names_list):
        print(str(self))
        for c in self._commodities:
            if c.getName() in commodities_names_list:
                print("      " + str(c))

    def str_with_specified_commodities(self, commodities_names_list):
        outcome =[]
        outcome.append(str(self._id) + ": " + str(self)+"\n")
        for c in self._commodities:
            if c.getName() in commodities_names_list:
                outcome.append("      " + str(c)+"\n")
        return "".join(outcome)

    def calcualte_distance_station(self,other_station):
        if self.getSystem() is None or other_station.getSystem() is None:
            return math.inf
        else:
            return self.getSystem().calcualte_distance(other_station.getSystem())

    def calcualte_distance_system(self,other_system):
        if self.getSystem() is None:
            return math.inf
        else:
            return self.getSystem().calcualte_distance(other_system)


class AllStations():
    def __init__(self):
        self._stations=[]
        self._systems=[]
        self._exact_commodity_creator=Exact_commodity_creator()
    def load_stations_from_json_withEndings(self,filename):
        stations_dictionaries_list=[]
        with open(filename,"r") as file:
            for line in file:
                stations_dictionaries_list.append(json.loads(line))
        for sd in stations_dictionaries_list:
            is_planetary=sd["is_planetary"]
            distance_to_star=math.inf
            id=int(sd["id"])
            system_id=int(sd["system_id"])
            if not sd["distance_to_star"] is None:
                distance_to_star=int(sd["distance_to_star"])

            #self._stations.append(Station(sd["name"],int(sd["id"]),int(sd["system_id"]),sd["max_landing_pad_size"],int(sd["distance_to_star"]),is_planetary))
            self._stations.append(Station(sd["name"],id,system_id,sd["max_landing_pad_size"],distance_to_star,is_planetary))
        #self.show()

    def load_systems_from_system_csv(self,filename):
        systems_dictionaries_list=[]
        with open(filename,"r") as file:
            for line in file:
                systems_dictionaries_list.append(json.loads(line))
        for sd in systems_dictionaries_list:

            fPermit=sd["needs_permit"]

            self._systems.append(
                System(int(sd["id"]), sd["name"], float(sd["x"]), float(sd["y"]), float(sd["z"]), fPermit))
            #debug
            # if sd["name"]=="Sol":
            #     system=self._systems.pop()
            #     do_nothing()
            #     self._systems.append(system)
        #self.showSystems()


    def _findSystem(self,system_id):
        for s in self._systems:
            if s.fId(system_id):
                return s
        return None

    def combineStationsAndSystems(self):
        print(time.strftime("StartTime =%H %M %S"))
        for station in self._stations:
            try:
                station.setSsytem(self._findSystem(station.get_system_id()))
            except:
                raise ValueError("Could not find system("+str(station.get_system_id())+"), to station: "+station.getName())
        self._stations.sort(key = lambda x: x.getId())
        print(time.strftime("Endtime= %H %M %S"))
        #self.show()

    def combineStationsAndSystems_v2(self):
        station_iter=iter(self._stations)
        station=station_iter.__next__()
        system_iter=iter(self._systems)
        system=system_iter.__next__()
        print(time.strftime("StartTime =%H %M %S"))
        while (True):
            try:
                if(station.get_system_id()==system.getId()):
                    station.setSsytem(system)
                    station=station_iter.__next__()
                else:
                    system=system_iter.__next__()
            except StopIteration:
                break
        print(time.strftime("Combining finisged= %H %M %S"))
        self._stations.sort(key=lambda x: x.getId())
        print(time.strftime("Sorting finished0= %H %M %S"))



    def buildStations(self,stations_json,systems_csv,commodities_json,listings_csv):
        print("loading commodities...")
        start_time=time.time()
        self._exact_commodity_creator.build_from_json_file(commodities_json)
        end_time=time.time()
        print("finished in "+str(end_time-start_time)+"s")

        print("loading stations...")
        start_time = time.time()
        self.load_stations_from_json_withEndings(stations_json)
        end_time = time.time()
        print("finished in " + str(end_time - start_time) + "s")

        print("loading systems..")
        start_time = time.time()
        self.load_systems_from_system_csv(systems_csv)
        end_time = time.time()
        print("finished in " + str(end_time - start_time) + "s")

        print("combining systems and stations...")
        start_time = time.time()
        self.combineStationsAndSystems_v2()
        end_time = time.time()
        print("finished in " + str(end_time - start_time) + "s")

        print("adding currrent markets...")
        start_time = time.time()
        self.add_commodities_to_stations(listings_csv)
        end_time = time.time()
        print("finished in " + str(end_time - start_time) + "s")

        print("markets succesfully added... \n\n\n")
        #self.print_absolute_top_n_stations(10)

    def add_commodities_to_stations(self,listings_csv):
        station_iter=iter(self._stations)
        plc=ProgressLogger(len(self._stations),print_amount=100)
        station=station_iter.__next__()
        with open(listings_csv,"r") as file:
            #print("after openfile")
            fFirstLine=True
            for line in file:

                #print("processsing line "+line)
                if fFirstLine:
                    fFirstLine = False
                    continue
                valuesStr=line.split(",")
                #print(valuesStr)
                valuesInt=[]
                for e in valuesStr:
                    if e == "":
                        valuesInt.append(0)
                    else:
                        valuesInt.append(int(e))
                #endfor
                #print(valuesInt)
                # 0: id,1: station_id,2: commodity_id,3: supply,4: supply_bracket,5: buy_price,6: sell_price,7:demand,demand_bracket,collected_at
                while( not valuesInt[1]==station.getId()):
                    station=station_iter.__next__()
                    plc.log_step()
                station.add_commodity(self._exact_commodity_creator.getExactCommodity(valuesInt[2],valuesInt[3],valuesInt[5],valuesInt[7],valuesInt[6]))
                #print("added commodity to station")
                #station.print_with_all_commodities()
        #end with open



    def show(self):
        for s in self._stations:
            print(str(s)+"     "+str(s.getId()))

    def showSystems(self):
        for s in self._systems:
            print(s)

    def printExactStations(self):
        for s in self._stations:
            s.printWithAllComodieties()

    def print_absolute_top_n_stations(self,n):
        for s in self._stations:
            if n <=0:
                break
            s.print_with_all_commodities()
            n=n-1
        #endfor

    def get_stations(self):
        return self._stations

    def get_systems(self):
        return self._systems