from pynotifier import Notification


def notify(self):
    Notification(
        title="Cowin Vaccine Booker",
        description="Kindly enter your OTP in the command prompt/terminal window!",
        urgency="critical"
    ).send()
