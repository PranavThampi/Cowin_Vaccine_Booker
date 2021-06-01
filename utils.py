

class Websites:
    base_url = "https://cdn-api.co-vin.in/api/v2"

    # Metadata API
    states_list_url = f"{base_url}/admin/location/states"
    districts_list_url = f"{base_url}/admin/location/districts"

    # Appointment availability
    calender_by_pincode = f"{base_url}/appointment/sessions/public/calendarByPin"
    calender_by_district = f"{base_url}/appointment/sessions/public/calendarByDistrict"

    session_by_pincode = f"{base_url}/appointment/sessions/public/findByPin"
    session_by_district = f"{base_url}/appointment/sessions/public/findByDistrict"

    # Authentication
    generate_otp = f"{base_url}/auth/generateMobileOTP"
    validate_otp = f"{base_url}auth/validateMobileOtp"

    # Appointment Scheduling and Cancelling
    schedule_appointment = f"{base_url}/appointment/schedule"
    cancel_appointment = f"{base_url}/appointment/cancel"
