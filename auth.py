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
            token = r.json()['token']
        else:
            print("OTP validation failed!")
        return token
