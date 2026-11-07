import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import re
import requests
from bs4 import BeautifulSoup

TARGET_URL = os.environ.get(
    "TARGET_URL",
    "https://citizen.bmi.gv.at/at.gv.bmi.fnsetvweb-p/etv/public/sva/Terminvereinbarung?locale=de"
)
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
NOTIFICATION_TO = os.environ.get("NOTIFICATION_TO", EMAIL_USER)

USER_LASTNAME = os.environ.get("USER_LASTNAME", "coyote")
USER_FIRSTNAME = os.environ.get("USER_FIRSTNAME", "wile-e")
USER_DOB = os.environ.get("USER_DOB", "01.01.2000")
USER_EMAIL = os.environ.get("USER_EMAIL", "wile-e.coyote@acme.com")

MAX_DAYS_AHEAD = int(os.environ.get("MAX_DAYS_AHEAD", "30"))

def send_email_notification(station_name, filtered_slots):
    if not EMAIL_USER or not EMAIL_PASS:
        print("[!] Error: Email credentials missing.")
        sys.exit(1)

    subject = f"⚡ Early ID Austria Slot Found at {station_name}!"
    body = f"Open appointment slots found within the next {MAX_DAYS_AHEAD} days:\n\n"
    for slot in filtered_slots:
        body += f"• {slot}\n"
    body += f"\nBook immediately here: {TARGET_URL}"

    msg = MIMEMultipart()
    msg['From'] = f"ID Austria Tracker <{EMAIL_USER}>"
    msg['To'] = NOTIFICATION_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"[+] Email alert sent successfully for {station_name}.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

def check_appointments():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    print(f"[*] Initializing session on portal...")
    response = session.get(TARGET_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    base_payload = {}
    for hidden in soup.find_all("input", type="hidden"):
        if hidden.get("name"):
            base_payload[hidden.get("name")] = hidden.get("value", "")

    stelle_select = soup.find("select", id=lambda i: i and "stelle" in i)
    stations = []
    if stelle_select:
        for option in stelle_select.find_all("option"):
            val = option.get("value")
            text = option.get_text(strip=True)
            if val and val != "Bitte auswählen":
                stations.append({"id": val, "name": text})

    print(f"[*] Discovered {len(stations)} police stations in Vienna to scan.")
    global_slots_found = False
    now = datetime.now()
    cutoff_date = now + timedelta(days=MAX_DAYS_AHEAD)

    for station in stations:
        station_id = station["id"]
        station_name = station["name"]
        print(f"[*] Checking station: {station_name}...")

        payload = base_payload.copy()
        payload.update({
            "bundesland": "9",
            "schlagwort": "ID Austria - Registrierung",
            "stelle": station_id,
            "anzahl": "1",
            "familienname": USER_LASTNAME,
            "vorname": USER_FIRSTNAME,
            "geburtsdatum": USER_DOB,
            "email": USER_EMAIL,
        })

        try:
            post_response = session.post(TARGET_URL, data=payload)
            post_response.raise_for_status()

            result_soup = BeautifulSoup(post_response.text, "html.parser")
            table = result_soup.find("table", class_=lambda c: c and "table-striped" in c)
            
            valid_early_slots = []

            if table:
                for row in table.find_all("tr"):
                    if row.find(id=lambda i: i and "timeslotssub" in i) or row.find(id=lambda i: i and i.startswith("chooseTimeslot#")):
                        slot_text = row.get_text(strip=True, separator=" ")
                        
                        date_match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", slot_text)
                        if date_match:
                            day, month, year = map(int, date_match.groups())
                            try:
                                slot_date = datetime(year, month, day)
                                if now <= slot_date <= cutoff_date:
                                    valid_early_slots.append(slot_text)
                                    print(f"[!] Found early slot within range: {slot_text}")
                                else:
                                    print(f"[-] Skipping late slot: {slot_text}")
                            except ValueError:
                                pass

            if valid_early_slots:
                send_email_notification(station_name, valid_early_slots)
                global_slots_found = True

        except Exception as ex:
            print(f"[!] Error checking station {station_name}: {ex}")

    if not global_slots_found:
        print("[+] Scan complete. No early slots found within the target window.")

if __name__ == "__main__":
    check_appointments()
