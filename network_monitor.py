import os
import subprocess
import smtplib
from email.mime.text import MIMEText

#function to ping a device and check if its online 
def ping_device(device_ip):
    try:
    # check os to determine ping command flag (-c for unix, -n for windows)
        param = "-c" if os.name != "nt" else "-n"
        response = os.system(f"ping {param} 1 {device_ip}")
        return response == 0 # returns true if online , false if offline
    except Exception as e:
        print(f"Error pinging {device_ip}: {e}")
        return False  

# function to check internet speed 
def check_speed():
    try:
        # check if speedtest-cli is installed, run speed test, return doenload speed
        result = subprocess.run(['speedtest-cli', '--simple'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        download_speed = float(result.split('\n')[1].split()[1])
        return download_speed
    except Exception as e:
        print(f"Error checking speed: {e}")
        return 0.0 # return 0.0 in case of failure

# function to send  an email alert
def send_alert(subject, message):
    try:
        msg = MIMEText(message)
        msg['subject'] = subject
        msg['From'] = "abuzaidmohamed2324@gmail.com"
        msg['To'] = "abuzaidmohamed2324@gmail.com"
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
         server.starttls()
         server.login("abuzaidmohamed2324@gmail.com", "rnlwfvlualcymepp")
         server.sendmail("abuzaidmohamed2324@gmail.com", "abuzaidmohamed2324@gmail.com", msg.as_string())
        print(f"Alert sent: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")   

# adresses of devices to monitor 
router_ip = "192.168.1.1"
laptop_ip = "192.168.1.70"
pc_ip = "172.26.240.1"

# monitoring devices
if not ping_device(router_ip):
    send_alert("Router offline", f"The router with IP {router_ip} is offline.")
if not ping_device(laptop_ip):
    send_alert("Laptop offline", f"The laptop with IP {laptop_ip} is offline.")
if not ping_device(pc_ip):
    send_alert("PC offline", f"The pc with IP {pc_ip} is offline.")

# monitoring internet speed
speed_threshold = 176.51 
current_speed = check_speed()
if current_speed < speed_threshold:
    send_alert("Internet speed Alert", f"internet speed is too low: {current_speed} Mbps")    
else:
    print(f"Internet speed is {current_speed} Mbps, which is above the treshold.")
