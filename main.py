import json
import os


class Booking:

    def __init__(self):
        print('\033[92m','*'*8,'Welcome to Cowin Vaccine Booker','*'*8,'\033[0m')
        if not os.path.exists('preferences.json'):
            self.preferences()
        else:
            choice = input("\nYour preferences already exist. Do you want to change them? Press \033[92mY\033[0m for yes and \033[1;31mN\033[0m for no:")
            if choice.lower() == 'y':
                self.preferences()

    def preferences(self):
        print('\n\033[1mKindly enter the following requested info to assist in booking the slots.\033[0m')
        district = input('\nEnter your district number. If you do not know your district number, it can be found in the file \033[3m\033[1mdistricts.json\033[0m:')
        cond = True
        while cond: 
            pincodes = list(map(str,input("\nEnter the pincode(s) convenient for you seperated by space:").split()))
            for x in pincodes:
                if len(x) is not 6:
                    print("Incorrect pincode. Please enter again")
                    cond = True
                    break
                else:
                    cond = False
                    
        print("\nPlease select the time frame suitable for you. Press the corresponding number followed by enter key.")
        day_part_choice = int(input("\n1. Morning(9am-12pm)\n2. Afternoon(12pm-5pm)\n3. Evening(5pm-11pm)\nChoice:"))
        age = input("\nEnter your age in years:")
        if age > '18' and age < '45':
            age = 18
        elif age > '45':
            age = 45
        else:
            print("Invalid age entered:")
        preferences = {}
        preferences['district'] = district
        preferences['pincodes'] = pincodes
        preferences['day_part_choice'] = day_part_choice
        preferences['age'] = age
        with open("preferences.json",'w') as file:
            json.dump(preferences, file, indent=3)
            file.close()

if __name__=='__main__':
    Booking()