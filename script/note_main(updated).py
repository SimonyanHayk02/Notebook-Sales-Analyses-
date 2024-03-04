from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep

options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options)
action = ActionChains(driver)

# with open("data_nout_am.csv", "w", encoding="UTF8", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow((
#         "Company", "Model", "Display Height", "Display Width", "Display Size", 
#         "Display Quality", "Display Type", "Processor Name", "Processor Generation",
#         "Memory", "Ram", "Videocard", "Videocard Storage", "Illuminated keyboard",
#         "Price", "Website index",
#     ))

def next_page():
    try:
        sleep(1)
        list(driver.find_elements(By.CSS_SELECTOR, "a.action.next"))[1].click()
        # next_button = list(WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.action.next"))
        # ))
        # next_button[1].click()
        print("Next page")
        scraper()
    except Exception as e:
        print(e)
        print("End of pages")

def scraper():
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/div[2]/main/div[3]/div[1]/div[6]/div[2]/ol/li")
        )
    )
    print(len(elements), "elems Len")
    sleep(3)
    for i in range(1, len(elements) + 1):
        try:
            elem = driver.find_element(
            By.XPATH,
            f"/html/body/div[2]/main/div[3]/div[1]/div[6]/div[2]/ol/li[{i}]/div/div[1]/a/span/span/img",    
            )
        except:
            elem = driver.find_element(
                By.XPATH,
                f'/html/body/div[2]/main/div[3]/div[1]/div[6]/div[2]/ol/li[{i}]/div/a/div/span/span/img',
            )        
        # try:
        #     elem = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable(
        #             (By.XPATH, f"/html/body/div[2]/main/div[3]/div[1]/div[6]/div[2]/ol/li[{i}]/div/div[1]/a/span/span/img")
        #         )
        #     )
        # except:
        #     elem = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable(
        #             (By.XPATH, f'/html/body/div[2]/main/div[3]/div[1]/div[6]/div[2]/ol/li[{i}]/div/a/div/span/span/img')
        #         )
        #     )
        elem.click()
        item_scraper()
        driver.back()
        # WebDriverWait(driver, 10).until(EC.url_contains("notebooks-ultrabooks.html"))
    next_page()

def item_scraper():
    try:
        company = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td[data-th='Բրենդ']"))
        ).text
    except Exception as e:
        print(e)
        return
    print("Company", company)

    # Rest of the item_scraper() code...
    model = driver.find_element(
        By.XPATH, "/html/body/div[2]/main/div[2]/div/div[2]/div[8]/div"
    ).text.split("/")[0]
    model = model.split()
    model_name = ""
    for i in range(2, len(model)):
        if ("-" in model[i]) or ("_" in model[i]) or ("#" in model[i]):
            break
        model_name += model[i] + " "
    model_name = model_name.strip()
    print("Model", model_name)
    try:
        display_size = float(
            driver.find_element(
                By.CSS_SELECTOR, "td[data-th='Անկյունագիծ \"']"
            ).text.split()[0]
        )
    except:
        display_size = None
    try:
        display_options = driver.find_element(
            By.CSS_SELECTOR, "td[data-th='Կետայնություն']"
        ).text.split()
    except:
        display_options = None
    try:
        display_height = int(display_options[-1])
    except:
        display_height = None
    try:
        display_width = int(display_options[0])
    except:
        display_width = None
    display_quality = None
    try:
        display_type = driver.find_element(
            By.CSS_SELECTOR, "td[data-th='Մատրիցայի տեսակ']"
        ).text.strip()
    except:
        display_type = None
    print(display_height, display_width, display_size, display_quality, display_type)

    processor_name = driver.find_element(By.CSS_SELECTOR, "td[data-th='Պրոցեսոր']").text
    processor_generation = (
        driver.find_element(By.CSS_SELECTOR, "td[data-th='Պրոցեսորի մոդել']")
        .text.split("-")[-1]
        .split()[-1]
    )
    print("Processor name", processor_name, "Generation", processor_generation)

    try:
        ram = int(
            driver.find_element(
                By.CSS_SELECTOR, "td[data-th='Օպերատիվ հիշողութ.']"
            ).text.split()[0]
        )
    except:
        ram = None
    print("RAM", ram)

    try:
        memory = int(
            driver.find_element(
                By.CSS_SELECTOR, "td[data-th='SSD կուտակիչ']"
            ).text.split()[0]
        )
    except:
        try:
            memory = int(
                driver.find_element(
                    By.CSS_SELECTOR, "td[data-th='Կոշտ սկավառակ (HDD)']"
                ).text.split()[0]
            )
        except:
            memory = None
    try:
        if memory < 10:
            memory *= 1024
    except:
        pass
    print("Memory", memory)
    try:
        videocard_name = driver.find_element(
            By.CSS_SELECTOR, "td[data-th='Տեսաքարտ']"
        ).text
    except:
        videocard_name = None
    try:
        videocard_memory = int(
            driver.find_element(
                By.CSS_SELECTOR, "td[data-th='Տեսաքարտի օպերատիվ հիշողություն']"
            ).text.split()[0]
        )
    except:
        videocard_memory = None
    print("Videcard Name", videocard_name, "Videocard Memory", videocard_memory)

    illuminated_keyboard = None

    try:
        price = int(
            driver.find_element(
                By.XPATH,
                "/html/body/div[2]/main/div[2]/div/div[2]/div[4]/div[1]/div[1]/span[2]/span/span[2]/span",
            )
            .text.replace(" ", "")
            .replace("դր.", "")
        )
    except:
        try:
            price = int(
            driver.find_element(
                By.XPATH,
                "/html/body/div[2]/main/div[2]/div/div[2]/div[4]/div[1]/div[1]/span/span/span",
            )
                .text.replace(" ", "")
                .replace("դր.", "")
            )
        except:
            price = None
    print("Price", price)

    print()

    with open("data_nout_am.csv", "a", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow((
            company,
            model_name,
            display_height,
            display_width,
            display_size,
            display_quality,
            display_type,
            processor_name,
            processor_generation,
            memory,
            ram,
            videocard_name,
            videocard_memory,
            illuminated_keyboard,
            price,
            2,
        ))

try:
    driver.get("https://nout.am/am/notebooks-ultrabooks.html?p=41&product_list_dir=desc&product_list_order=brand")
    driver.maximize_window()
    scraper()
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
