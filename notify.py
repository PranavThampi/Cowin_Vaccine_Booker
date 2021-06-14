from pynotifier import Notification


def notify(description):
    Notification(
        title="Cowin Vaccine Booker",
        description=description,
        urgency="critical"
    ).send()
