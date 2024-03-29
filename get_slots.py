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
            with open(self.district_file, 'r') as file:
                self.districts = json.load(file)

    def metadata_api(self):
        states_and_districts = []
        state_url = Websites.states_list_url
        r = requests.get(state_url, headers=self.headers)
        if r.ok:
            all_states = r.json()
            states = all_states["states"]
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
            with open(self.district_file, 'w') as file:
                json.dump(states_and_districts, file, indent=4)
                file.close()
            return states_and_districts
        else:
            print('Request to get states failed! Error code:', r.status_code)

    def get_slots(self, district, date, pincodes, vaccine, dose, age):
        url = f"{Websites.calender_by_district}?district_id={district}&date={date}"
        r = requests.get(url, headers=self.headers)
        if r.ok:
            with open("slots.json", "w") as file:
                json.dump(r.json(), file, indent=5)
                file.close()

            final_centers = []
            centers = r.json()['centers']
            for i in centers:
                center = i
                if center['pincode'] in pincodes:
                    sessions = center["sessions"]
                    filtered_sessions = []
                    for j in sessions:
                        session = j
                        if session["min_age_limit"] == age and session[dose] > 0 \
                                and session['vaccine'] == vaccine:
                            filtered_sessions.append(session)
                    if len(filtered_sessions) > 0:
                        center["sessions"] = filtered_sessions
                        final_centers.append(center)
            with open("filtered_slots", "w") as file:
                json.dump(final_centers, file, indent=5)
                file.close()
            return final_centers
        else:
            print("Could not get slots!!", r.json())
