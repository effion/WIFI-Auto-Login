import time
import json
import os
import sys
from tkinter import simpledialog
from tkinter import messagebox
try:
    
    import requests
    from infi.systray import SysTrayIcon
    from PIL import Image
except(ModuleNotFoundError):
    messagebox.showinfo("WifiV2", "Module(s) not found. Program will terminate in 5 seconds, please run install.bat again.")
    time.sleep(5)
    os.system('taskkill /F /T /IM pyw.exe')
    

messagebox.showinfo("WifiV2", "Running in background...")


try:
    with Image.open(r'favicon.png') as img:
        img.save('favicon.ico')
        os.remove('favicon.png')
except(FileNotFoundError):
    pass





# systray on_quit arg for quitting program.
def quitprg(systray):
    messagebox.showinfo("WifiV2", "Program terminated successfully.")
    SysTrayIcon.shutdown
    os.system('taskkill /F /T /IM pyw.exe')

systray = SysTrayIcon("favicon.ico", "WifiV2", on_quit=quitprg)
systray.start()


#defining file name
filename="data.json"

#userlogin function that creates a data.json file if it doesn't already exist with the user and password input from user.
def userlogin():
    try:
        with open (filename, 'r') as f:
                    settings=json.load(f)
                    print(f"{filename} found.")
                    user=settings[0]
                    passw=settings[1]
                    

                    
    except:
        print(f"{filename} not found. Creating...")
        user=simpledialog.askstring(title="USER NAME", prompt="Enter Bennett Login ID\t\t\t")
        passw=simpledialog.askstring(title="PASS WORD", prompt="Enter Bennett password\t\t\t")
        settings=[user,passw]
        with open (filename, 'w') as f:
            json.dump(settings,f)
        print(f"{filename} created.")
    return user,passw

    

#Calling above function and saving the variables received
user,passw=userlogin() 

#variables
s = requests.Session()
url = 'http://172.16.16.16/24online/servlet/E24onlineHTTPClient'
Data={
'mode': '191',
'isAccessDenied': 'null',
'url': 'null',
'message': '',
'regusingpinid': '',
'checkClose': '1',
'sessionTimeout': '0',
'guestmsgreq': 'false',
'logintype': '2',
'orgSessionTimeout': '0',
'chrome': '-1',
'alerttime': 'null',
'timeout': '0',
'popupalert': '0',
'dtold': '0',
'mac': '50:2f:a8:7e:4b:d1',
'servername': '172.16.16.16',
'temptype': '',
'selfregpageid': '',
'leave': 'no',
'macaddress': '50:2f:a8:7e:4b:d1',
'ipaddress': '10.12.10.170',
'profilegroupid': '1',
'profileName': 'bennette',
'username': f'{user}',
'password': f'{passw}',
'loginotp': 'false',
'logincaptcha': 'false',
'registeruserotp': 'false',
'registercaptcha': 'false'
}


# Convert 2 strings to lists to display censored username & password
def Convert(string,string2):
    try:
        list1=[]
        list2=[]
        list1[:0]=string
        list2[:0]=string2
    except(TypeError,IndexError):
        messagebox.showinfo("WifiV2", "Error parsing .json file. Maybe you forgot to enter user/pass? Please re-enter user password.")
        os.remove(filename)
        os.execv(sys.executable, ['python3'] + sys.argv)
    return list1,list2



# Main function that will try to post to designated URL with designated data and timeout of 1 second to ensure instant connectivity
def updatedopenpage():
    x=0
    y=0
    
    while x>=0:
        try:
            link=s.post(url=url, data=Data, timeout=1)
            if link.ok==True:
                y+=1
                funcsuccess=time.time()
                print(f'Successful attempt after: {funcsuccess-funcstart:.2f}s')
                print(f"Success! Attempt number {y}")
            else:
                continue
        except(requests.exceptions.Timeout, requests.ConnectionError):
            x+=1
            funcerror=time.time()
            print(f'Time elapsed: {funcerror-funcstart:.2f}')
            print(f"Failed. Attempt number {x}")


# Converting credentials to censored with function Convert
censoreduser,censoredpass=Convert(user,passw) #Converting user & pass to censored format

print(f'Initiating..')
print(f"Username is {censoreduser[0]}*****{censoreduser[-1]} and password is {censoredpass[0]}*****{censoredpass[-1]}. Hit CTRL+C and close program to terminate if incorrect.")
print(f"Change extension to .pyw for a seamless experience. Current timeout is set to 1")



funcstart=time.time()
updatedopenpage()



