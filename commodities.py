import json



class General_commodity:
    def __init__(self,name,id):
        self._name=name
        self._id=id
    def getId(self):
        return self._id
    def fId(self,id):
        return self._id == id
    def getName(self):
        return self._name
    def __str__(self):
        return self._name + ":" + str(self._id)

class Commodity(General_commodity):
    def __init__(self,gc_base,supply,buy_price,demand,sell_price):
        General_commodity.__init__(self,gc_base.getName(),gc_base.getId())
        self._supply=supply
        self._buy_price=buy_price
        self._demand=demand
        self._sell_price=sell_price
    def getSupply(self):
        return self._supply
    def getPrice(self):
        return self._buy_price
    def __str__(self):
        return self.getName()+" Supply: "+ str(self._supply) + " Buy Price: " + str(self._buy_price) + " Demand: " + str(self._demand) + " Sell Price: " + str(self._sell_price)
    def get_sell_price(self):
        return self._sell_price
    def get_demand(self):
        return self._demand
    def eq_same_name(self,other_commodity):
        return other_commodity.getName()==self.getName()


class Exact_commodity_creator:
    def __init__(self):
        self._all_general_commodities=[]

    def addCommodity(self,new_general_commodity):
        if not self.fConatinsId(new_general_commodity.getId):
            self._all_general_commodities.append(new_general_commodity)

    def fConatinsId(self,id):
        for c in self._all_general_commodities:
            if c.fId(id):
                return True
        return False

    def __str__(self):
        return str(self._all_general_commodities)

    def show(self):
        print("ecc show\nname:id")
        for gc in self._all_general_commodities:
            print(gc)

    def build_from_json_file(self,file_path):
        commodities_dictionaries_list=[]
        with open(file_path, "r") as json_file:
            commodities_dictionaries_list=json.load(json_file)
        for c_dict in commodities_dictionaries_list:
            self.addCommodity(General_commodity(c_dict['name'],int(c_dict['id'])))
        #print("build succesful")
        #self.show()

    def _find_general_commodity(self,commodity_id):
        for gc in self._all_general_commodities:
            if gc.fId(commodity_id):
                return gc
        return None


    # supply and buy_price as int
    def getExactCommodity(self,commodity_id, supply,buy_price,demand,sell_price):
        if not self.fConatinsId(commodity_id):
            raise ValueError("commodity asked for (id: " + str(commodity_id)+") but not in general commodity list")
        general_commodity=self._find_general_commodity(commodity_id)
        return Commodity(general_commodity,supply,buy_price,demand,sell_price)





