from enum import Enum
from stationsAndSystems import *
from progress_logger import ProgressLogger

# assumes commodities instations sorted by id
def find_best_value_commodity_across_stations(station_a,station_b):
    outcomes=[]
    outcome=(None,None,None,0)
    cb_iter=station_b.get_commodities().__iter__()
    ca_iter=station_a.get_commodities().__iter__()
    try:
        cb = cb_iter.__next__()
        for ca in ca_iter:
            while cb.getId()<ca.getId():
                cb=cb_iter.__next__()
            #endwhile
            if ca.getId()==cb.getId():
                if ca.getSupply()==0 and cb.getSupply()==0:
                    continue
                if ca.getPrice()>0 and cb.get_sell_price() > ca.getPrice():
                    if outcome[3]<(cb.get_sell_price() -ca.getPrice()):
                        outcome=(station_a,station_b,ca.getName(),(cb.get_sell_price() -ca.getPrice()))
                if cb.getPrice()>0 and ca.get_sell_price() > cb.getPrice():
                    if outcome[3]<(ca.get_sell_price() -cb.getPrice()):
                        outcome=(station_b,station_a,ca.getName(),(ca.get_sell_price() - cb.getPrice()))

    except StopIteration:
        pass

    return outcome






def find_best_single_hop_within_ly_system(all_stations,ly,refrence_system):
    general_station_list=all_stations.get_stations()
    station_list=[]
    for station in general_station_list:
        if station.getSystem() is not None and refrence_system.calcualte_distance(station.getSystem()) < ly:
            station_list.append(station)
            station.get_commodities().sort(key= lambda x: x.getId())

    outcome=(None,None,None,0)
    plog=ProgressLogger(len(station_list)*len(station_list)/2,print_amount=100)
    for i in range(len(station_list)):
        for k in range(i,len(station_list)):
            plog.log_step()
            tmp_outcome=find_best_value_commodity_across_stations(station_list[i],station_list[k])
            if outcome[3]<tmp_outcome[3]:
                outcome=tmp_outcome
    return outcome


def find_best_single_hop_within_ly(all_stations,ly):
    station_list=list(filter(lambda x:  x is not None ,all_stations.get_stations()))
    map(lambda s: s.get_commodities().sort(key= lambda x: x.getId()),station_list)

    outcome=(None,None,None,0)
    plog = ProgressLogger(len(station_list) * len(station_list) / 2, print_amount=100)
    for i in range(len(station_list)):
        for k in range(i,len(station_list)):
            plog.log_step()
            if station_list[i].calcualte_distance_station(station_list[k]) > ly:
                continue
            tmp_outcome=find_best_value_commodity_across_stations(station_list[i],station_list[k])
            if outcome[3]<tmp_outcome[3]:
                outcome=tmp_outcome
    return outcome

def find_best_single_hop_within_ly_with_l_pad(all_stations,ly):
    station_list=list(filter(lambda x:  x is not None and x.getSystem() is not None  ,all_stations.get_stations()))
    station_list=list(filter(lambda x:  x.get_max_landing_pad()=="L" ,station_list))
    map(lambda s: s.get_commodities().sort(key= lambda x: x.getId()),station_list)

    outcome=(None,None,None,0)
    plog = ProgressLogger(len(station_list) * len(station_list) / 2, print_amount=100)
    for i in range(len(station_list)):
        for k in range(i,len(station_list)):
            plog.log_step()
            if station_list[i].calcualte_distance_station(station_list[k]) > ly:
                continue
            tmp_outcome=find_best_value_commodity_across_stations(station_list[i],station_list[k])
            if outcome[3]<tmp_outcome[3]:
                outcome=tmp_outcome
    return outcome

def find_all_single_hop_within_ly(all_stations,ly):
    station_list=list(filter(lambda x:  x is not None and x.getSystem() is not None  ,all_stations.get_stations()))
    station_list=list(filter(lambda x:  x.get_max_landing_pad()=="L" ,station_list))
    map(lambda s: s.get_commodities().sort(key= lambda x: x.getId()),station_list)
    outcome_list=[]

    plog = ProgressLogger(len(station_list) * len(station_list) / 2, print_amount=100)
    for i in range(len(station_list)):
        for k in range(i,len(station_list)):
            plog.log_step()
            if station_list[i].calcualte_distance_station(station_list[k]) > ly:
                continue
            tmp_outcome=find_best_value_commodity_across_stations(station_list[i],station_list[k])
            outcome_list.append(tmp_outcome)
    return outcome_list