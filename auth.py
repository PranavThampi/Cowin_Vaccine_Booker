from utils import Websites
import requests
import hashlib
import json
import notify


class Authentication:

    def __init__(self, mobile):
        self.mobile = mobile
        self.headers = Websites.headers
        if self.generate_otp():
            self.validate_otp()
            self.get_beneficiaries()

    def generate_otp(self):
        url = Websites.generate_otp
        data = {
            "mobile": self.mobile,
            "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw=="
        }
        r = requests.post(url, json=data, headers=self.headers)
        if r.ok:
            self.txn_id = r.json()['txnId']
            notify.notify("Please enter your OTP in the terminal window!!!")
            return True
        else:
            print("Error in generating OTP!", r.json())

    def validate_otp(self):
        otp = input("Enter your otp:")
        encode_otp = otp.encode()
        encoded_otp = hashlib.sha256(encode_otp).hexdigest()

        url = Websites.validate_otp
        data = {
            "otp": encoded_otp,
            "txnId": self.txn_id
        }
        r = requests.post(url, json=data, headers=self.headers)
        if r.ok:
            self.token = r.json()['token']
        else:
            print("OTP validation failed!", r.json())

    def get_beneficiaries(self):
        url = Websites.get_beneficiaries
        self.headers['Authorization'] = f"Bearer {self.token}"
        r = requests.get(url, headers=self.headers)
        if r.ok:
            with open("beneficiary.json", "w") as file:
                json.dump(r.json()['beneficiaries'], file, indent=4)
                file.close()

            beneficiaries_list = r.json()['beneficiaries']
            count = 1
            if len(beneficiaries_list) > 1:
                beneficiary_list = {}
                print(
                    "You have more than one beneficiary linked to this number. \nPlease select the beneficiary by "
                    "selecting the number")
                for beneficiaries in beneficiaries_list:
                    beneficiary_list[count] = [beneficiaries['name'], beneficiaries['beneficiary_reference_id']]
                    print(count, '-', beneficiaries['name'])
                    count += 1
                choice = int(input('Enter choice: '))
                self.beneficiary = beneficiary_list[choice]
            else:
                self.beneficiary = [beneficiaries_list[0]['name'], beneficiaries_list[0]['beneficiary_reference_id']]
        else:
            print("Could not fetch beneficiaries!!", r.text)
