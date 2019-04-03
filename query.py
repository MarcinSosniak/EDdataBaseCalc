from enum import Enum
from stationsAndSystems import *



class TRANSACTION_TYPE(Enum):
    BUY = 5
    SELL = 6

class QUERRY_CONDITIONS(Enum):
    LANDING_PAD =0
    PLANETARY = 1
    PERMIT =2
    DISTANCE_SYSTEMS =3
    DISTANCE_STAR =4




class Querry:
    def __init__(self,current_station_name,current_system_name):
        self._current_station_name=current_station_name
        self._current_system_name=current_system_name
        # in that order: 0 Distance Systems, 1 Permit, 2 Planetary, 3 LandingPad, 4 Distance from star
        # distance between current and target station has to lesser than list[0]
        self._distance_systems=math.inf
        self._permit=False#defaulty no permit rewuired, true means it CAN (but doesn't habe to) haeva  permit
        self._planetary=False#default not palnetary, true means it CAN (but doesn't have to) be a planetary
        self._landing_pad="S"
        self._distance_from_star=math.inf# station trying to be queried has to have lesser
        self._comodity_list=[]
        self._condition_iterator_counter=0
        self._comodity_list_iterator=iter(self._comodity_list)

    #take value as a UPPERCASE string
    def addCondition(self,cond_type,value):
        value=value.upper()
        if (cond_type==QUERRY_CONDITIONS.LANDING_PAD):
            if value== "L" or value=="M" or value=="S" or "ANY":
                self._landing_pad=value
            else:
                raise ValueError("invalid data input for LandingPad, got '"+str(value)+"'")
        elif cond_type==QUERRY_CONDITIONS.PLANETARY:
            if (value=="TRUE" or value=="T"):
                self._planetary=True
        elif cond_type==QUERRY_CONDITIONS.PERMIT:
            if (value=="TRUE" or value=="T"):
                self._permit=True
        elif cond_type==QUERRY_CONDITIONS.DISTANCE_STAR:
            fVal=float(value)
            if(fVal >= 0):
                self._distance_from_star=fVal
            else:
                raise ValueError("distance to star cannot be below zero")
        elif cond_type==QUERRY_CONDITIONS.DISTANCE_SYSTEMS:
            fVal = float(value)
            if (fVal >= 0):
                self._distance_systems = fVal
            else:
                raise ValueError("distance between systems cannot be below zero")
        else:
            raise ValueError("invalid condition type got:" + str(cond_type))
    #enddef
    def addCommodity(self,name,transaction_type,amount):
        if(transaction_type==TRANSACTION_TYPE.SELL):
            raise ValueError("Selling queries not supported yet")
        elif not transaction_type==TRANSACTION_TYPE.BUY:
            raise ValueError("Invalid transaction type got"+str(transaction_type)+" Excpecter QUERRY_CONDITIONS.SELL or QUERRY_CONDITIONS.BUY")
        #endif
        self._comodity_list.append((name,transaction_type,int(amount)))

    def next_condition(self):
        if self._condition_iterator_counter==0:
            if not self._distance_systems==math.inf:
                self._condition_iterator_counter=self._condition_iterator_counter+1
                return (QUERRY_CONDITIONS.DISTANCE_SYSTEMS,self._distance_systems)
            else:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
        if self._condition_iterator_counter==1:
            if not self._permit: # if permit can but doesn't ahev to be it takea allstations,so no reason to check condition
                self._condition_iterator_counter = self._condition_iterator_counter + 1
                return (QUERRY_CONDITIONS.PERMIT,False)
            else:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
        if self._condition_iterator_counter==2:
            if not self._planetary:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
                return (QUERRY_CONDITIONS.PLANETARY, False)
            else:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
        if self._condition_iterator_counter==3:
            if self._landing_pad=="M" or self._landing_pad=="L":
                self._condition_iterator_counter = self._condition_iterator_counter + 1
                return (QUERRY_CONDITIONS.LANDING_PAD,self._landing_pad)
            else:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
        if self._condition_iterator_counter==4:
            if not self._distance_from_star== math.inf:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
                return (QUERRY_CONDITIONS.DISTANCE_STAR,self._distance_from_star )
            else:
                self._condition_iterator_counter = self._condition_iterator_counter + 1
        raise StopIteration
    #enddef

    def next_commodity(self):
        return self._comodity_list_iterator.__next__()

    def get_commodity_new_iter(self):
        return iter(self._comodity_list)
    def get_commodities_list(self):
        return self._comodity_list

    def reset_conditions_iter(self):
        self._condition_iterator_counter=0
    def reset_commodity_iter(self):
        self._comodity_list_iterator=iter(self._comodity_list)

    def get_station_info(self):
        return self._current_station_name,self._current_system_name

    def get_commodieties_names(self):
        names=[]
        for c in self._comodity_list:
            names.append(c[0])
        return names


class QueryResult:
    def __init__(self,stations=None,commodities_names=None,refrence_station=None):
        if stations is None:
            self._stations=[]
        else:
            self._stations=stations
        if commodities_names is None:
            self._commodities_names=[]
        else:
            self._commodities_names=commodities_names
        self._refrence_station=refrence_station

    def add_station(self,station):
        self._stations.append(station)


    def print(self):
        for s in self._stations:
            s.print_with_specified_commodities(self._commodities_names)
    #ENDDEF
    def sort_by_disatnce(self):
        if self._refrence_station is not None:
            self._stations.sort(key= lambda x: x.getSystem().calcualte_distance(self._refrence_station.getSystem()))
    #ednddef

    def print_with_range(self):
        if self._refrence_station is None:
            self.print()
            return
        for s in self._stations:
            print(str(s.getSystem().calcualte_distance(self._refrence_station.getSystem()))+"Ly : ",end="")
            s.print_with_specified_commodities(self._commodities_names)

    def print_top_n_with_range(self,n):
        if self._refrence_station is None:
            self.print()
            return
        counter=n
        for s in self._stations:
            if counter<=0 :
                break
            counter=counter-1
            print(str(s.getSystem().calcualte_distance(self._refrence_station.getSystem()))+"Ly : ",end="")
            s.print_with_specified_commodities(self._commodities_names)







class QueryExcutioner:
    def __init__(self,stations):
        self._stations=stations

    # def _find_refrence_station(self,station_info):
    #     for s in self._stations:
    #         if s.getName().upper() == station_info[0].upper() and s.getSystem().getName().upper() == station_info[1].upper():
    #             return s
    #     raise ValueError("cold not find specified system, looking for station '"+station_info[0] +"' in '"+station_info[1]+"'")

    def _find_refrence_station(self,station_name,system_name):
        for s in self._stations:
            if s.getName() == station_name:
                if s.getSystem().getName().upper() == system_name.upper():
                    return s
        raise ValueError("cold not find specified system, looking for station '"+station_name +"' in '"+system_name+"'")



    def check_condtion(self,cond_and_val,station,refrence_station):
        if cond_and_val[0]==QUERRY_CONDITIONS.DISTANCE_SYSTEMS:
            if station.getSystem().calcualte_distance(refrence_station.getSystem()) < cond_and_val[1]:
                return True
            else:
                return False
        if cond_and_val[0]==QUERRY_CONDITIONS.DISTANCE_STAR:
            if station.get_distance_to_star()<cond_and_val[1]:
                return True
            else:
                return False
        if cond_and_val[0]==QUERRY_CONDITIONS.LANDING_PAD:
            if cond_and_val[1]=="L" and (station.get_max_landing_pad()=="M" or station.get_max_landing_pad()=="S"):
                return False
            elif cond_and_val[1]=="M" and station.get_max_landing_pad()=="S":
                return False
            return True
        if cond_and_val[0]==QUERRY_CONDITIONS.PLANETARY:
            if cond_and_val[1]==True:
                return True
            else:
                return not station.get_planetary()
        if cond_and_val[0]==QUERRY_CONDITIONS.PERMIT:
            if cond_and_val[1]== True:
                return True
            else:
                return not station.getSystem().getPermit()
        raise ValueError("invalid condition type, got: "+ str(cond_and_val))




    def execute(self,query):
        refrence_station_name,refrence_system_name=query.get_station_info()
        refrenceStation = self._find_refrence_station(refrence_station_name,refrence_system_name)
        qresult=QueryResult(commodities_names=query.get_commodieties_names(),refrence_station=refrenceStation)
        for station in  self._stations:
            if station.getSystem() is None:
                continue
            passed_conditions=True
            query.reset_conditions_iter()
            while True:
                try:
                    if not self.check_condtion(query.next_condition(),station,refrenceStation):
                        passed_conditions=False
                        break
                except StopIteration:
                    break
            if not passed_conditions:
                continue# drop station,check next
            #endod
            for commodityCond in query.get_commodity_new_iter():
                if commodityCond[1]==TRANSACTION_TYPE.BUY:
                    if station.f_commodity_with_supply(commodityCond[0],commodityCond[2]) is not None:
                        pass
                    else:
                        passed_conditions=False
                        break
                else:
                    ValueError("unnsported operation excepction, currently only supported TRANSACTION_TYPE is buy")
            if passed_conditions:
                qresult.add_station(station)
        #endfor
        return qresult
