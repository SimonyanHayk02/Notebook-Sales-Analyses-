from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import csv
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options = options)
action = ActionChains(driver)
# with open('./data_buylaptop.csv', 'w', encoding='UTF8', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(("Company", "Model",
#                          "Display Height", "Display Width", "Display Size", "Display Quality", "Display Type",
#                          "Processor Name", "Processor Generation",
#                          "Memory", 
#                          "Ram", 
#                          "Videocard", "Videocard Storage",
#                          "Illuminated keyboard", 
#                          "Price",
#                          "Website index"))

def scraper():
    for i in range(83, 208):
        time.sleep(1)
        driver.find_element(By.XPATH, f"/html/body/form/div/div/div[2]/div[2]/div[{i}]/div/div[2]/h6/a").click()
        time.sleep(3)
        print(i, "current index")
        try:
            item_scraper()
        except Exception as e:
            print(e)
        driver.back()
        time.sleep(2)   
        
def item_scraper():
    model = driver.find_element(By.CSS_SELECTOR, 'div.page-title').text.split()
    company = model[0] if model[0].lower() != "macbook" else "Apple"
    model_name = ""
    for i in range(1, len(model)):
        if ("-" in model[i]) or ("_" in model[i]) or ("#" in model[i]):
            break
        model_name += model[i] + " "
    model_name = model_name.strip() if(company != "Apple") else f"MacBook {model_name.strip()}"
    print("Model: ", model_name)
    print("Company: ", company)
    
    if(company == "Apple"):
        time.sleep(1)
        apple_scrapper(model_name, company)
    else:
        time.sleep(1)
        standart_scrapper(model_name, company)
    print()

def apple_scrapper(model_name, company):
    i = 1
    if("macbook pro" in model_name.lower()):
        processor = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[1]/td[2]').text.split("(")[0].split()
        processor_name = ' '.join(processor[0:2]).strip()
        processor_generation = processor[2].strip()
        print('procesor_name: ', processor_name)
        print('procesor_generation: ', processor_generation)
        i += 1
    else:
        processor_name = None
        processor_generation = None
        print('procesor_name: ', processor_name)
        print('procesor_generation: ', processor_generation)
    display_size = float(driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[{i}]/td[2]").text.split()[0])
    display = driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[{i+1}]/td[2]").text.split('x')
    display_width = int(display[0])
    display_height = int(display[-1])
    display_quality = None
    display_type = None
    print("display_size: ", display_size)
    print("display_width: ", display_width)
    print("display_height: ", display_height)
    print("display_quality: ", display_quality)
    print("display_type: ", display_type)
    
    ram = driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[{i+2}]/td[2]").text.split()[0].strip()
    memory = int(driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[{i+3}]/td[2]').text.split()[0].strip())
    memory_gb = memory if memory > 10 else memory * 1024
    print("Ram: ", ram)
    print("Memory: ", memory_gb)

    try:
        illuminated_keyboard = 1 if(driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[{i+8}]/td[2]').text == 'Այո') else 0
        print("Illuminated_Keyboard: ", illuminated_keyboard)
    except:
        illuminated_keyboard = 0
    videocard_name = None
    videocard_memory = None
    print("Videocard_Name: ", videocard_name)
    print("Videocard_Memory: ", videocard_memory)
    
    price = int(driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/span").text.split()[0].replace(',', '').strip())
    print("Price: ", price)
    
    with open('./data_buylaptop.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((company, model_name,
                         display_height, display_width, display_size, display_quality, display_type, 
                         processor_name, processor_generation, 
                         memory, ram, 
                         videocard_name, videocard_memory,
                         illuminated_keyboard, 
                         price,
                         3))  

def standart_scrapper(model_name, company):
    processor = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[1]/td[2]').text.split("(")[0].split()
    if(processor[0].lower() == "intel"):
        if(processor[1].lower() != "core"):
            processor_name = processor[0]
            processor_generation = processor[1]
        else:
            processor_name = ' '.join(processor[0:3])
            processor_generation = processor[3].strip()
    elif(len(processor) == 1):
        processor_name = 'Intel'
        processor_generation = processor[0]
    else:
        processor_name = f"{processor[0]} {processor[1]}".strip()
        processor_generation = processor[2].strip()
    print('procesor_name: ', processor_name)
    print('procesor_generation: ', processor_generation)
        
    display_size = float(driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[2]/td[2]").text.split()[0].strip())
    try:
        display = driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[3]/td[2]").text.split()
        display_quality = display[1].strip()
        display_width = int(display[0].split('x')[0].strip())
        display_height = int(display[0].split('x')[1].strip())
    except:
        display = driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[3]/td[2]").text.split('x')
        display_quality = None    
        display_width = int(display[0].strip())
        display_height = int(display[1].strip())
    display_type = None
    
    print("display_size: ", display_size)
    print("display_width: ", display_width)
    print("display_height: ", display_height)
    print("display_quality: ", display_quality)
    print("display_type: ", display_type)
    
    ram = int(driver.find_element(By.XPATH, f"/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[4]/td[2]").text.split()[0].strip())
    memory = int(driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[5]/td[2]').text.split()[0].strip())
    memory_gb = memory if memory > 10 else memory * 1024
    print("Ram: ", ram)
    print("Memory: ", memory_gb)
    
    videocard = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[6]/td[2]").text
    if(not "graphics" in videocard.lower()):
        videocard = videocard.split()
        videocard_name = ' '.join(videocard[0:-1]).strip()
        videocard_memory = videocard[-1][:-2].strip()
    else:
        videocard_name = videocard
        videocard_memory = None
    
    print("videocard_name: ", videocard_name)
    print("videocard_memory: ", videocard_memory)
    
    try:
        illuminated_keyboard = 1 if(driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[2]/div/div/div/ul/div/table/tbody/tr[11]/td[2]').text == 'Այո') else 0
        print("Illuminated_Keyboard: ", illuminated_keyboard)
    except:
        illuminated_keyboard = 0
        
    price = int(driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/span").text.split()[0].replace(',', '').strip())
    print("Price: ", price)
       
    with open('./data_buylaptop.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((company, model_name,
                         display_height, display_width, display_size, display_quality, display_type, 
                         processor_name, processor_generation, 
                         memory, ram, 
                         videocard_name, videocard_memory,
                         illuminated_keyboard, 
                         price,
                         3))
try:
    driver.get('https://www.buylaptop.am/product-categories/notebooks')
    driver.maximize_window()
    time.sleep(2)
    scraper()
except Exception as e:
    print(e)
finally:
    driver.quit()