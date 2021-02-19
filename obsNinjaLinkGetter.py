from sys import argv
from selenium import webdriver
import time
import json
#print(argv[1])


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument("--headless")
options.add_argument("--window-size=1200,1200")
#options.binary_location = "/usr/bin/chromium"
kampOversikt = None
kampe = None
with open("jsonFiles/kamper/oversikt.json","r") as f:
    kampOversikt = json.load(f)

driver = webdriver.Chrome(chrome_options=options)
if(len(argv)>1):
    tid = str(time.time())
    print(tid)
    #driver.get(argv[1])
    #driver.get("http://localhost:5000/production/twitterMatchImage/c92e83b4-f59d-421f-9ffe-bb01f382f0e4")
    driver.get("http://localhost:5000/production/twitterMatchImage/"+argv[1])
    for kamp in kampOversikt:
        if kamp["kampID"] == argv[1]:
            kampe = kamp
            break
    if(kampe != None):
        lagring = str(tid)+ "_"+str(kampe["dato"])
    else:
        lagring = argv[1]
    driver.save_screenshot("static/img/twitter/"+lagring+".png")

    driver.close()
else:
    
    kamp = kampOversikt[0]
    print(kamp)
    if(kamp != None):
        tidColon = kamp["tid"]
        tid1 = tidColon[0:2]
        tid2 = tidColon[3:5]
        tid = tid1+tid2
        #print(tid1)
        #print(tid2)
        # +"_"+str(kamp["kampID"][0:4])
        lagring = str(tid)+ "_"+str(kamp["dato"])
        #print(lagring)
        driver.get("http://localhost:5000/production/twitterMatchImage/"+kamp["kampID"])
        driver.save_screenshot("static/img/twitter/"+lagring+".png")
        driver.close()
    else:
        print("Du må sende med kampID når du starter programmet")
        input("Trykk en knapp for gå ut!")
