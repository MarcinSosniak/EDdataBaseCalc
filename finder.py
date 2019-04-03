
import pprint
import os
import time
from query import *
import wget
from specific_query import find_best_single_hop_within_ly_system
from specific_query import find_best_single_hop_within_ly
from specific_query import find_best_single_hop_within_ly_with_l_pad
from progress_logger import ProgressLogger
from copy import copy

from enum import Enum

sources_dir="src"
last_download_file_name_raw="last_download.txt"
last_download_file_name=sources_dir + "/" +last_download_file_name_raw
commodities_filename=sources_dir + "/" +'commodities.json'
commodities_url="https://eddb.io/archive/v6/commodities.json"
stations_filename=sources_dir + "/" +'stations.jsonl'
stations_url="https://eddb.io/archive/v6/stations.jsonl"
populated_systems_filename=sources_dir + "/" +'systems_populated.jsonl'
populated_systems_url="https://eddb.io/archive/v6/systems_populated.jsonl"
listings_filename=sources_dir + "/" +'listings.csv'
listings_url="https://eddb.io/archive/v6/listings.csv"















def testJsonDecoder():
    with open("C:/Users/MarcinS/Downloads/commodities.json","r") as file:
        outcome=json.load(file)
        pprint.pprint(outcome)
        print("\n\n\n\n\n\n\n\n\n")
        print(outcome[0])

def test_self_build_ecc():
    ecc = Exact_commodity_creator()
    ecc.build_from_json_file("C:/Users/MarcinS/Downloads/commodities.json")

def test_stations_self_build():
    allS=AllStations()
    allS.load_stations_from_json_withEndings("C:/Users/MarcinS/Downloads/stations.json")
def test_systems_self_build():
    allS = AllStations()
    allS.load_systems_from_system_csv("C:/Users/MarcinS/Downloads/populated_systems.csv")

def test_stations_combining():
    allS = AllStations()
    allS.load_stations_from_json_withEndings("C:/Users/MarcinS/Downloads/stations.json")
    allS.load_systems_from_system_csv("C:/Users/MarcinS/Downloads/populated_systems.csv")
    allS.combineStationsAndSystems()


def test_build():
    allS=AllStations()
    allS.buildStations("C:/Users/MarcinS/Downloads/stations.json","C:/Users/MarcinS/Downloads/populated_systems.csv","C:/Users/MarcinS/Downloads/commodities.json","C:/Users/MarcinS/Downloads/listingsTest.csv")

def test_full_build():
    allS=AllStations()
    allS.buildStations("C:/Users/MarcinS/Downloads/stations.json","C:/Users/MarcinS/Downloads/populated_systems.csv","C:/Users/MarcinS/Downloads/commodities.json","C:/Users/MarcinS/Downloads/listings.csv")


def test_query_basic():
    allS = AllStations()
    allS.buildStations("C:/Users/MarcinS/Downloads/stations.json", "C:/Users/MarcinS/Downloads/populated_systems.csv",
                       "C:/Users/MarcinS/Downloads/commodities.json", "C:/Users/MarcinS/Downloads/listingsTest.csv")
    print("\n\n\n\n\n\n")

    executioner=QueryExcutioner(allS.get_stations())
    query=Querry("Bain Colony", "V492 Lyrae")
    # query.addCommodity("Hydrogen Fuel",TRANSACTION_TYPE.BUY,100)
    query.addCondition(QUERRY_CONDITIONS.LANDING_PAD,"L")
    query.addCondition(QUERRY_CONDITIONS.DISTANCE_SYSTEMS,"15")
    qr=executioner.execute(query)
    qr.print_with_range()


def test_query_full():
    allS=AllStations()
    allS.buildStations("C:/Users/MarcinS/Downloads/stations.json","C:/Users/MarcinS/Downloads/populated_systems.csv","C:/Users/MarcinS/Downloads/commodities.json","C:/Users/MarcinS/Downloads/listings.csv")

    print("\n\n\n\n\n\n")

    executioner=QueryExcutioner(allS.get_stations())
    query = Querry("Bain Colony", "V492 Lyrae")
    query.addCommodity("Hydrogen Fuel",TRANSACTION_TYPE.BUY,100)
    query.addCondition(QUERRY_CONDITIONS.LANDING_PAD, "L")
    query.addCondition(QUERRY_CONDITIONS.DISTANCE_SYSTEMS, "15")
    startTime=time.time()
    qr = executioner.execute(query)
    endTime=time.time()
    qr.print_with_range()
    print("\n\n\n\nquery took "+str(endTime-startTime)+ "s")
    return allS

class Hue_class():
    def __init__(self):
        self._hue=15
        self._hue2=64
    def inc(self):
        self._hue = self._hue2 +1
        self._hue2 = self._hue+1

    def get(self):
        return self._hue,self._hue2



def test_find_best_single_hop_within_ly_system(all_staions=None):
    allS=None
    if not all_staions is None:
        allS=all_staions
    else:
        allS=AllStations()
        allS.buildStations("C:/Users/MarcinS/Downloads/stations.json","C:/Users/MarcinS/Downloads/populated_systems.csv","C:/Users/MarcinS/Downloads/commodities.json","C:/Users/MarcinS/Downloads/listings.csv")
    # allS.load_systems_from_system_csv("C:/Users/MarcinS/Downloads/populated_systems.csv")
    sol_list=[x for x in allS.get_systems() if x.getName()=="Sol"]
    sol=sol_list[0]
    print(sol_list)
    print(sol)
    print(sol.getXYZ())
    xyz=sol.getXYZ()
    out=find_best_single_hop_within_ly_system(allS,25,sol)
    print("buy in:")
    print(out[0])
    print("sell in:")
    print(out[1])
    print("commodity:")
    print(out[2])
    print("for profit/tonne")
    print(out[3])


def test_find_best_single_hop_within_ly():
    allS = AllStations()
    allS.buildStations("C:/Users/MarcinS/Downloads/stations.json", "C:/Users/MarcinS/Downloads/populated_systems.csv",
                       "C:/Users/MarcinS/Downloads/commodities.json", "C:/Users/MarcinS/Downloads/listings.csv")
    sol_list = [x for x in allS.get_systems() if x.getName() == "Sol"]
    sol = sol_list[0]
    outcome=find_best_single_hop_within_ly(allS,25)
    print("buy")
    outcome[0].print_with_specified_commodities([outcome[2]])
    print("sell")
    outcome[1].print_with_specified_commodities([outcome[2]])
    print("profit= " + str(outcome[3]) + " distance= " + str(outcome[0].calcualte_distance_station(outcome[1])))

def test_find_best_single_hop_within_ly_with_l_pad():
    allS = AllStations()
    allS.buildStations("C:/Users/MarcinS/Downloads/stations.json", "C:/Users/MarcinS/Downloads/populated_systems.csv",
                       "C:/Users/MarcinS/Downloads/commodities.json", "C:/Users/MarcinS/Downloads/listings.csv")
    sol_list = [x for x in allS.get_systems() if x.getName() == "Sol"]
    sol = sol_list[0]
    print("startin special query")
    start_time=time.time()
    outcome = find_best_single_hop_within_ly_with_l_pad(allS, 25)
    end_time=time.time()
    print("ended querery in="+str(end_time-start_time))
    print("buy")
    outcome[0].print_with_specified_commodities([outcome[2]])
    print("sell")
    outcome[1].print_with_specified_commodities([outcome[2]])
    print("profit= " + str(outcome[3]) + " distance= " + str(outcome[0].calcualte_distance_station(outcome[1])))


def test_progress_logger():
    pl=ProgressLogger(100,print_amount=100)
    start_time=time.time()
    i=0
    while i<100:
        if time.time()>start_time+0.1:
            i=i+1
            start_time=time.time()
            pl.log_step()




def test_wget():
    url="https://eddb.io/archive/v6/commodities.json"
    filename=wget.download(url,out="src")
    print(filename)



def update_files(force_reload=False):
    with open(last_download_file_name,"r") as file:
        line=file.readline()
        line=line.replace("\n","")
        if not force_reload and line==time.strftime("%Y %m %d"):
            print("files up to date")
            return
    with open(last_download_file_name,"w") as file:
        file.write(time.strftime("%Y %m %d"))

    file_list=os.listdir(path=sources_dir)
    for file in file_list:
        if not file == last_download_file_name_raw:
            print("deleting file '"+file+"'")
            os.remove(sources_dir+"/"+file)
    global commodities_filename
    print("starting commodities download")
    commodities_filename=wget.download(commodities_url,out=sources_dir)
    global stations_filename
    print("starting stations download")
    stations_filename=wget.download(stations_url,out=sources_dir)
    global populated_systems_filename
    print("starting systems download")
    populated_systems_filename=wget.download(populated_systems_url,out=sources_dir)
    global listings_filename
    print("starting listings download")
    listings_filename=wget.download(listings_url,out=sources_dir)
    print("finihsed reloads")



def run_find_best_single_hop_within_ly_with_l_pad(ly):
    allS = AllStations()
    allS.buildStations(stations_filename, populated_systems_filename,
                       commodities_filename, listings_filename)
    sol_list = [x for x in allS.get_systems() if x.getName() == "Sol"]
    sol = sol_list[0]
    print("startin special query")
    start_time = time.time()
    outcome = find_best_single_hop_within_ly_with_l_pad(allS, ly)
    end_time = time.time()
    print("ended querery in=" + str(end_time - start_time))
    print("buy")
    outcome[0].print_with_specified_commodities([outcome[2]])
    print("sell")
    outcome[1].print_with_specified_commodities([outcome[2]])
    print("profit= " + str(outcome[3]) + " distance= " + str(outcome[0].calcualte_distance_station(outcome[1])))










if __name__ == "__main__":
    #test_self_build_ecc()

    #test_stations_self_build()
    #test_systems_self_build()
    # test_stations_combining()
    #test_build()
    #test_full_build()
    #test_query_basic()
    #ass=test_query_full()
    # test_find_best_single_hop_within_ly_system()
    #test_find_best_single_hop_within_ly()
    #test_progress_logger()
    #test_find_best_single_hop_within_ly_with_l_pad()
    #test_wget()
    update_files()
    run_find_best_single_hop_within_ly_with_l_pad(15)
    pass
