######### MAIN ############## MAIN #################### MAIN ########################

from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import smtplib
from email.message import EmailMessage
from pyvirtualdisplay import Display
import time as TIME
import sys


# Function to send email
def send_mail(receiver_address, sender_address, content):
    msg = EmailMessage()

    msg['Subject'] = "New Slot On Sainsburys"
    msg['From'] = sender_address
    msg['To'] = receiver_address

    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(msg["From"], password)
        smtp.send_message(msg)

    print("Slot Found")    
    print("Sent")




print("Starting for zipcode " + str(sys.argv[1]))


Important
display = Display(visible=0, size=(800, 600))
display.start()

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', desired_capabilities=capa)

#driver = webdriver.Chrome(executable_path='chromedriver.exe', desired_capabilities=capa)

password = str(sys.argv[2]).strip()
    
zip_code = str(sys.argv[1]).strip().lower()



while True:
    
    print("starting...")


    try:
        driver.get("http://www.sainsburys.co.uk/shop/gb/groceries")
        wait = WebDriverWait(driver, 65)
        wait.until(EC.presence_of_element_located((By.ID, '#postCode')))
        driver.execute_script("window.stop();")

    except Exception as e:
        print(e)
        pass


    try:
        driver.find_element_by_id("postCode").send_keys(zip_code, Keys.ENTER)
        WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.ID, "collectBookSlotBtn")))

    except Exception as e:
        print(e)
        pass


    try:

        choose_loc_btn = driver.find_element_by_id("collectBookSlotBtn")
        driver.execute_script("arguments[0].click();", choose_loc_btn)
        WebDriverWait(driver, 40).until(ec.visibility_of_element_located((By.CLASS_NAME, "actions")))

    except Exception as e:
        print(e)
        pass



    try:

        select_loc_btn = driver.find_element_by_class_name("actions")
        select_loc_btn.click()

    except Exception as e:
        print(e)
        pass


    #Close cookie popup

    try:
        WebDriverWait(driver, 7).until(ec.visibility_of_element_located((By.ID, "cookieContinue")))

    except:
        pass


    try:
        accept_cookie_btn = driver.find_element_by_id("cookieContinue")
        accept_cookie_btn.click()

    except:
        pass


    #Find delivery slots table

    try:
        all_table_cells = driver.find_element_by_class_name("deliverySlots").find_elements_by_tag_name("td")

    except Exception as e:
        print(e)
        pass


    #Get booking on the table by getting the header value of a cell (td) which would be used to get date and time

    try:
        vert_id = ""
        hor_id = ""

        for cell in all_table_cells:
            if cell.text.strip() != "":
                vert_id = cell.get_attribute("headers").split(" ")[0].strip()
                hor_id = cell.get_attribute("headers").split(" ")[1].strip()
                break

    except Exception as e:
        print(e)
        pass



    #Get date and time

    date = ""
    time = ""


    try:
        date = driver.find_element_by_id(vert_id).text.strip()

    except:
        pass


    try:
        time = driver.find_element_by_id(hor_id).text.strip()

    except:
        pass


    if date != "":
        date = date + " " + str(datetime.datetime.now().year)
        
        try:
            send_mail(receiver_address="randeep@springsoftware.co.uk", sender_address="pycollins2019@gmail.com", 
                  content="There is a new slot on Sainsburys for date: " + str(date))

            send_mail(receiver_address="pycollins2019@gmail.com", sender_address="pycollins2019@gmail.com", 
                  content="There is a new slot on Sainsburys for date: " + str(date))
            
            
        except Exception as e:
            print(e)
            pass

        




    print("Done")
    driver.delete_all_cookies()
    #driver.quit()
    TIME.sleep(5)
