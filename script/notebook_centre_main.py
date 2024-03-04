from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import csv
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent


# ua = UserAgent()
# user_agent = ua.random
# print(user_agent)
options = Options()
options.add_argument('--disable-notifications')
# options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options = options)
action = ActionChains(driver)
with open('./data_notebookcentre.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(("Company", "Model",
                         "Display Height", "Display Width", "Display Size", "Display Quality", "Display Type",
                         "Processor Name", "Processor Generation",
                         "Memory", 
                         "Ram", 
                         "Videocard", "Videocard Storage",
                         "Illuminated keyboard", 
                         "Price",
                         "Website index"))

def model_changer():
    for i in range(1, 11):
        driver.find_element(By.XPATH, f'/html/body/main/div/div[1]/div[1]/div[2]/ul[2]/li[{i}]/label').click()
        time.sleep(2)
        scraper()
        time.sleep(2)
        driver.find_element(By.XPATH, f'/html/body/main/div/div[1]/div[1]/div[2]/ul[2]/li[{i}]/label').click()
        print("scrapper")

def scraper():
    elements = list(driver.find_elements(By.CSS_SELECTOR, 'li[itemtype="http://schema.org/Product"]'))
    i = 1
    while True:
        print(len(elements), "elems Len")
        time.sleep(1)
        driver.find_element(By.XPATH, f"/html/body/main/div/div[1]/div[1]/div[2]/div[2]/ul[2]/li[{i}]/div/a/div/div/img").click()
        time.sleep(3)
        print(i, "current index")
        item_scraper()
        driver.back()
        time.sleep(2)
        if( i == 29):
            time.sleep(2)
            elements = [*elements, *list(driver.find_elements(By.CSS_SELECTOR, 'li[itemtype="http://schema.org/Product"]'))[i+1:]]
            # elements.append(*list(driver.find_elements(By.CSS_SELECTOR, 'li[itemtype="http://schema.org/Product"]'))[i+1:])
        if(i == len(elements)):
            break
        i += 1;
        # driver.execute_script("window.history.go(-1)")
        # time.sleep(2)
        
def item_scraper():
    article = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[1]/div/article/div[1]/h1/span').text.split()
    company, title = article[0], " ".join(article[1:-1])
    
    display = driver.find_element(By.CSS_SELECTOR, 'tr.screen_size td.value').text.split()
    display_size, display_width, display_height= float(display[0]), int(display[2].split('x')[0]), int(display[2].split('x')[1]) 
    display_quality =  display[3] if(len(display) == 4) else None
    display_type = None
    
    processor = driver.find_element(By.CSS_SELECTOR, 'tr.screen_size ~ tr td.value').text.split()
    if(processor[0].lower() == 'intel'):
        processor_name = processor[0]
        processor_generation = processor[1]
    else:
        processor_name = f"{processor[0]} {processor[1]}"
        processor_generation = processor[2]

    print("Processor", processor_name, "generation", processor_generation)

    memory = int(driver.find_element(By.CSS_SELECTOR, 'tr.screen_size ~ tr ~ tr td.value').text.split()[0])
    if(memory <= 10):
        memory *= 1024
    print(memory)
    
    ram = int(driver.find_element(By.CSS_SELECTOR, 'tr.ram_capacity td.value').text.split()[0])
    print(ram,"Ram")
    try:
        videocard = driver.find_element(By.CSS_SELECTOR, 'tr.videocard td.value').text
        if ("graphics" in videocard.lower()):
            videocard_name = videocard
            videocard_memory = None
        else:
            videocard = videocard.split()
            videocard_name = "".join(videocard[:-1])
            videocard_memory = int(videocard[-1][:-2])
    except:
        videocard_name = None
        videocard_memory = None
    print(videocard_memory, videocard_name, "videocard_memory")
    
    try:
        driver.find_element(By.CSS_SELECTOR, 'tr.illuminated_keyboard td.value').text
        illuminated_keyboard = 1
    except:
        illuminated_keyboard = 0
        
    print(illuminated_keyboard)
    
    price = int(driver.find_element(By.CSS_SELECTOR, 'span.curent-price').text.replace(' ', '').replace('֏', ''))
    
    print(price, "price")
    
    print(company, title)
    print()
    with open('./data_notebookcentre.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((company, title,
                         display_height, display_width, display_size, display_quality, display_type, 
                         processor_name, processor_generation, 
                         memory, ram, 
                         videocard_name, videocard_memory,
                         illuminated_keyboard, 
                         price,
                         1))   


try:
    driver.get('https://notebookcentre.am/category/notebooks/')
    driver.maximize_window()
    time.sleep(2)
    model_changer()
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()