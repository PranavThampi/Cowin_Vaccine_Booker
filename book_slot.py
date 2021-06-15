from utils import Websites
from get_slots import Slots
import json
from datetime import date
import notify
from auth import Authentication
import requests


class BookSlots:
    def __init__(self):
        with open("preferences.json") as file:
            pref = json.load(file)
            file.close()
        self.district = pref['district']
        self.pincode = pref['pincode']
        # self.time_pref = pref['day_part_choice']
        self.date = date.today()
        self.vaccine = pref['vaccine']
        self.dose = pref['dose']
        if self.dose == 1:
            dose = 'available_capacity_dose1'
        else:
            dose = 'available_capacity_dose1'
        self.age = pref['age']
        self.centers = Slots().get_slots(self.district, self.date, self.pincode, self.vaccine, dose, self.age)
        self.mobile = pref['mobile']
        if self.centers:
            auth = Authentication(self.mobile)
            self.beneficiary = auth.beneficiary
            self.token = auth.token
            self.headers = Websites.headers
            self.headers['Authorization'] = f"Bearer {self.token}"
            self.book_slots()
        else:
            print("Sorry, We could not get any slots!!")

    def book_slots(self):
        url = Websites.schedule_appointment
        for centers in self.centers:
            sessions = centers['sessions']
            for session in sessions:
                session_id = session['session_id']
                for slot in session['slots']:
                    data = {
                        "dose": 1,
                        "session_id": session_id,
                        "slot": slot,
                        "beneficiaries": [
                            self.beneficiary[1]
                        ]
                    }
                    r = requests.post(url, json=data, headers=self.headers)
                    if r.ok:
                        message = f"Appointment for {self.beneficiary[0]} has been confirmed in {centers['name']} " \
                                  f"located at {centers['address']} on {session['date']} at {slot}"
                        print(message)
                        notify.notify(message)
                        return True
