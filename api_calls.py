from utils import Websites
import json
import requests
from fake_useragent import UserAgent
import os


class ApiCalls:

    def __init__(self):
        user_agent = UserAgent().random
        self.headers = {"User-Agent": user_agent}
        self.district_file = "districts.json"
        if not os.path.exists(self.district_file) or not os.stat(self.district_file).st_size:
            self.metadata_api()

    def metadata_api(self):
        states_and_districts = []
        all_states = {}
        state_url = Websites.states_list_url
        r = requests.get(state_url, headers=self.headers)
        if r.status_code == 200:
            all_states = r.json()
            states = all_states["states"]
        else:
            print('Request to get states failed! Error code:', r.status_code)

        district_url = Websites.districts_list_url
        for state in states:
            state_info = state
            url = district_url + '/' + str(state_info["state_id"])

            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                state_info["districts"] = r.json()
                states_and_districts.append(state_info)
            else:
                print('Request to get districts failed! Error code:', r.status_code)

        with open(self.district_file,'w') as file:
            json.dump(states_and_districts, file, indent=4)
            file.close()

if __name__ == "__main__":
    ApiCalls()