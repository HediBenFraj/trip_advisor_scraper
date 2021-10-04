from typing import get_args
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def formatting_function(chaine):
    if(isinstance(chaine,str)):
        stage1 = chaine.replace("\u00e9","e")
        stage2 = stage1.replace("\u00e7","c")
        stage3 = stage2.replace("\u00ee","e")
        stage4 = stage3.replace("\u00ef","i")
    else:
        stage4= "NONE"
    return stage4



driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://www.tripadvisor.fr/Restaurant_Review-g295401-d9740033-Reviews-Hard_Rock_Cafe-Sousse_Sousse_Governorate.html#photos;aggregationId=&albumid=101&filter=7')
print(driver.title)


try:
    main = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"_1kXteagE"))
    )
    with open('restaurants.json', 'a') as json_file:
      
        articles = main.find_elements_by_class_name("_1llCuDZj")
        data = []
        counter = 0
        for article in articles:

            title = WebDriverWait(article,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"_15_ydu6b"))
            )
            link = article.find_element_by_link_text(title.text)

            link.click()

            driver.switch_to.window(driver.window_handles[1])
          
            page = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"page"))
            )

            images = page.find_elements(By.TAG_NAME, 'img')
            avis_phone = page.find_elements(By.XPATH ,'//*[contains(concat( " ", @class, " " ), concat( " ", "_37QDe3gr", " " ))]' )
            price_cuisines = page.find_elements(By.XPATH ,'//*[contains(concat( " ", @class, " " ), concat( " ", "_1XLfiSsv", " " ))]' )
            addresses = page.find_elements(By.XPATH ,'//*[contains(concat( " ", @class, " " ), concat( " ", "_15QfMZ2L", " " ))]' )

            site_menu = page.find_elements(By.CLASS_NAME, '_15QfMZ2L')
            mails = page.find_elements(By.CLASS_NAME,'_36TL14Jn')

            restaurantTitle = page.find_element(By.XPATH , '//*[contains(concat( " ", @class, " " ), concat( " ", "_3a1XQ88S", " " ))]')
            restaurantAvisNumber = avis_phone[0]
            restaurantAddress = addresses[1]
            
            print("longeur d'image", images[0].text)

            try:
                restaurantPhoneNumber =  avis_phone[1]
            except:
                restaurantPhoneNumber = "NONE"
            try:
                restaurantWebsiteUrl = site_menu[3]
                website=restaurantWebsiteUrl.get_attribute('href')
            except:
                website='NONE'
            
            try:
                restaurantMenuUrl = site_menu[len(site_menu)-1]
                menu=restaurantMenuUrl.get_attribute('href')
            except:
                menu='NONE'
            restaurantAvisNote = page.find_element(By.XPATH , '//*[contains(concat( " ", @class, " " ), concat( " ", "r2Cf69qf", " " ))]')
            restaurantCuisines = price_cuisines[1]
            if(len(mails)==4):
                restaurantMailContainer = mails[len(mails)-2]

                try:
                    restaurantMail = restaurantMailContainer.find_element(By.TAG_NAME,'a')
                    email = restaurantMail.get_attribute('href')
                except:
                    email = "NONE"
           
            restaurantPriceRange = price_cuisines[0]
            counter = counter +1

            print("################# ",counter,"\n\n")

           

            if(restaurantTitle!="NONE"):titre=restaurantTitle.text
            if(restaurantAvisNote!="NONE"):note=restaurantAvisNote.text
            if(restaurantAvisNumber!="NONE"): avis=restaurantAvisNumber.text
            if(restaurantAddress != "NONE"):adresse=restaurantAddress.text
            if(restaurantCuisines!= "NONE"):cuisines = restaurantCuisines.text
            if(restaurantPhoneNumber != "NONE"):phone=restaurantPhoneNumber.text
            
            if(restaurantPriceRange!="NONE"):price=restaurantPriceRange.text
            

            

            data.append({
                "title" : formatting_function(titre),
                "avisNumber" : formatting_function(avis),
                "rating" : formatting_function(note),
                "address" : formatting_function(adresse),
                "phoneNumber" : formatting_function(phone),
                "websiteUrl" : formatting_function(website),
                "menuUrl" : formatting_function(menu),
                "priceRange" :formatting_function(price),
                "cuisines" : formatting_function(cuisines),
                "email" :formatting_function(email)
            })


            print({
                "title" : formatting_function(titre),
                "avisNumber" : formatting_function(avis),
                "rating" : formatting_function(note),
                "address" : formatting_function(adresse),
                "phoneNumber" : formatting_function(phone),
                "websiteUrl" : formatting_function(website),
                "menuUrl" : formatting_function(menu),
                "priceRange" :formatting_function(price),
                "cuisines" : formatting_function(cuisines),
                "email" :formatting_function(email)
            })

            print("########################## \n\n")

            
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        json.dump(data, json_file)
            
        #     formatted_title = title.text.replace("\u00e9","e")
        #     formatted_title = formatted_title.replace("\u00e7","c")

        #     descriptions = article.find_elements_by_class_name('_1p0FLy4t')

        #     formatted_description1 = descriptions[0].text.replace("\u00e9","e")
        #     formatted_description1 = formatted_description1.replace("\u00e7","c")

        #     formatted_description2 = descriptions[2].text.replace("\u00e9","e")
        #     formatted_description2 = formatted_description2.replace("\u00e7","c")


        #     data.append({
        #         "title" : formatted_title,
        #         "description1" : formatted_description1,
        #         "description2" : formatted_description2
        #     })
        # json.dump(data, json_file)
            
        
        
finally:
    json_file.close()
    driver.quit()



