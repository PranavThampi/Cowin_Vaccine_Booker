from utils import Websites
import requests
import hashlib


class Authentication:

    def __init__(self, mobile):
        self.mobile = mobile
        self.headers = Websites.headers

    def generate_otp(self):
        url = Websites.generate_otp
        data = {
            "mobile": self.mobile,
            "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw=="
        }
        r = requests.post(url,data=data, headers=self.headers)
        if r.ok:
            self.txn_id = r.json()['txnId']
        else:
            print("Error in generating OTP!")

    def validate_otp(self):
        otp = input("Enter your otp:")
        encode_otp = otp.encode()
        encoded_otp = hashlib.sha256(encode_otp).hexdigest()

        url = Websites.validate_otp
        data = {
            "txnID": self.txn_id,
            "otp": encoded_otp
        }
        r = requests.post(url, data=data, headers=self.headers)
        if r.ok:
            self.token = r.json()['token']
        else:
            print("OTP validation failed!")
        
    def get_beneficiaries(self):
        url = Websites.get_beneficiaries
        r = requests.get(url, headers=self.headers, auth=(self.token))
        if r.ok:
            beneficiaries_list = r.json()["beneficiaries"]
            beneficiary_list = {}
            count = 1
            if len(beneficiaries_list) > 1:
                print("You have more than one beneficiary linked to this number. \nPlease select the beneficiary by selecting the number")
                for beneficiaries in beneficiaries_list:
                    beneficiary_list[count] = [beneficiaries['name'], beneficiaries['beneficiary_reference_id']]
                    print(count,'-',beneficiaries['name'])
                    count += 1
                choice = int(input('Enter choice: '))
                beneficiary = beneficiary_list[choice]
            else:
                beneficiary = beneficiaries_list['beneficiary_reference_id']

        return beneficiary
