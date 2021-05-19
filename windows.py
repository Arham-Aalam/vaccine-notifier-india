import requests
from win10toast import ToastNotifier
import datetime
from threading import Timer
from fake_headers import Headers
import time

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)

###############
# settings
###############
# change it accordingly (314 is for indore)
DEST_CODE = 314
PERIOD = 5 * 60 # 5 minutes
toaster = ToastNotifier()

def main():
    global DEST_CODE, toaster, header
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={DEST_CODE}&date={date}"
    print(url)
    try:
        res = requests.get(url, headers=header.generate()).json()
        # print(res.keys())
        # res['centers'][0]['sessions'][0]['available_capacity_dose1'] = 5
        for center in res['centers']:
            name = center['name']
            address = center['address']
            sessions = center.get('sessions', [])
            for session in sessions:
                if session.get('available_capacity_dose1', 0) > 0:
                    toaster.show_toast(f"{session.get('available_capacity_dose1', 0)} doses in {name}", f"{address}", duration=20, threaded=True)
                if session.get('available_capacity_dose2', 0) > 0:
                    toaster.show_toast(f"{session.get('available_capacity_dose2', 0)} doses in {name}", f"{address}", duration=20, threaded=True)
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print("[ERROR] ", e)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(PERIOD)