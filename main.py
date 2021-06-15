import json
import os
import time

from book_slot import BookSlots
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

class Booking:

    def __init__(self):
        print('\033[92m', '*' * 8, 'Welcome to Cowin Vaccine Booker', '*' * 8, '\033[0m')
        if not os.path.exists('preferences.json'):
            self.preferences()
        else:
            choice = input(
                "\nYour preferences already exist. Do you want to change them? Press \033[92mY\033[0m for yes and "
                "\033[1;31mN\033[0m for no:")
            if choice.lower() == 'y':
                self.preferences()
        self.initiate_booking()

    @staticmethod
    def preferences():
        print('\n\033[1mKindly enter the following requested info to assist in booking the slots.\033[0m')
        district = input(
            '\nEnter your district number. If you do not know your district number, it can be found in the file \033['
            '3m\033[1mdistricts.json\033[0m:')
        cond = True
        while cond:
            pincodes = list(map(str, input("\nEnter the pincode(s) convenient for you seperated by space:").split()))
            for x in pincodes:
                if len(x) is not 6:
                    print("Incorrect pincode. Please enter again")
                    cond = True
                    break
                else:
                    cond = False

        print("\nPlease select the time frame suitable for you. Press the corresponding number followed by enter key.")
        # day_part_choice = int(input("\n1. Morning(9am-12pm)\n2. Afternoon(12pm-5pm)\n3. Evening(5pm-11pm)\nChoice:"))
        age = input("\nEnter your age in years:")
        if '18' < age < '45':
            age = 18
        elif age > '45':
            age = 45
        else:
            print("Invalid age entered:")

        while True:
            mobile = input("Enter your 10 digit mobile number")
            if len(mobile) is not 10 and not int(mobile):
                print("\033[1;31mIncorrect number. Please enter again\033[0m")
            else:
                break
        print("Please select your vaccine preference!")
        vaccine_choice = int(input("Press 1 for Covishield and 2 for Covaxin:"))
        vaccine = 'COVISHIELD' if vaccine_choice == 1 else 'COVAXIN'
        dose = int(input('Press 1 for first dose and 2 for second dose'))
        preferences = {
            'district': district,
            'pincodes': pincodes,
            # 'day_part_choice': day_part_choice,
            'age': age,
            'mobile': mobile,
            'vaccine': vaccine,
            'dose': dose
        }
        with open("preferences.json", 'w') as file:
            json.dump(preferences, file, indent=3)
            file.close()

    @staticmethod
    def initiate_booking():
        while True:
            booking = BookSlots()
            if booking.book_slots():
                break
            time.sleep(10)


if __name__ == '__main__':
    Booking()
