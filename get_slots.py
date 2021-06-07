from utils import Websites
import json
import requests
import os


class Slots:

    def __init__(self):
        self.headers = Websites.headers
        self.district_file = "districts.json"
        if not os.path.exists(self.district_file) or not os.stat(self.district_file).st_size:
            self.districts = self.metadata_api()
        else:
            with open(self.district_file,'r') as file:
                self.districts = json.load(file)

    def metadata_api(self):
        states_and_districts = []
        all_states = {}
        state_url = Websites.states_list_url
        r = requests.get(state_url, headers=self.headers)
        if r.ok:
            all_states = r.json()
            states = all_states["states"]
        else:
            print('Request to get states failed! Error code:', r.status_code)

        district_url = Websites.districts_list_url
        for state in states:
            state_info = state
            url = district_url + '/' + str(state_info["state_id"])

            r = requests.get(url, headers=self.headers)
            if r.ok:
                state_info["districts"] = r.json()
                states_and_districts.append(state_info)
            else:
                print('Request to get districts failed! Error code:', r.status_code)

        with open(self.district_file,'w') as file:
            json.dump(states_and_districts, file, indent=4)
            file.close()
        return states_and_districts

    def get_slots(self, district, date):
        url = f"{Websites.calender_by_district}?district={district}&date={date}"
        r = requests.get(url, headers=self.headers)
        if r.ok:
            with open("slots.json", "w") as file:
                json.dump(r.json(), file, indent=5)
                file.close()
        pincodes = list(map(str,input("Enter the pincode(s) convenient for you seperated by space:".split())))
        final_centers = []
        centers = r.json()['centers']
        for i in centers:
            center = i
            if center['pincode'] in pincodes:
                sessions = center["sessions"]
                filtered_sessions = []
                for i in sessions:
                    session = i
                    if session["min_age_limit"] == 18 and session["available_capacity_dose1"] > 0:
                        filtered_sessions.append(session)
                if len(filtered_sessions) > 0:
                    center["sessions"] = filtered_sessions
                    final_centers.append(center)
        with open("filtered_slots","w") as file:
            json.dump(final_centers, file, indent=5)
            file.close
            
if __name__ == "__main__":
    Slots()