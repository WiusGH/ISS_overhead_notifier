import requests
from datetime import datetime
import smtplib

MY_EMAIL = "wius.python@gmail.com"
PASSWORD = "djaddoclbkjczklc"
MY_LAT = -33.500790
MY_LNG = -70.663630
is_close = False

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

if iss_latitude > 0:
    rem_lat = MY_LAT + iss_latitude
elif iss_latitude < 0:
    rem_lat = MY_LAT - iss_latitude

if iss_longitude > 0:
    rem_lng = MY_LNG + iss_longitude
elif iss_longitude < 0:
    rem_lng = MY_LNG - iss_longitude

if rem_lng > -5 and rem_lng < 5:
    if rem_lat > -5 and rem_lat < 5:
        is_close = True

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) - 4
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) - 4
time_now = int(datetime.now().hour)
if time_now >= sunset or time_now <= sunrise:
    if is_close:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="wilidj4@hotmail.com", msg="Subject:The ISS is close!!\n\n"
                                                                                        "Look up! The ISS is close!")
