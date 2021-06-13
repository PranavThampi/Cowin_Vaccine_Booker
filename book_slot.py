from utils import Websites
from get_slots import Slots
import json
from datetime import date
import notify
from auth import Authentication

class BookSlots:
    def __init__(self):
        with open("preferences.json") as file:
            pref = json.load(file)
            file.close()
        self.district = pref['district']
        self.pincode = pref['pincode']
        self.date = date.today()
        self.centers = Slots().get_slots(self.district, self.date)
        self.mobile = pref['mobile']
        if self.centers:

            self.book_slots()
        else:
            print("Sorry, We could not get any slots!!")

    def book_slots(self):
