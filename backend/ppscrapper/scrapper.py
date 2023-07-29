from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
import pandas as pd

"""
File responsible for pulling the betting lines form PrizePicks.
"""

def getPPProps(sport_abbrev):
    """
    Returns a pandas dataframe containing all the betting lines in all categories of a specific sport. Also writes the data to a csv file.

    params:
    sport_abbrev : three-letter abbreviation of the title of a sports league ex. NBA, MLB, LoL
    """
    # Driver initialization
    driver = webdriver.Chrome()

    driver.get("https://app.prizepicks.com/")

    wait = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME, "close")))
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/button").click()
    time.sleep(3)

    driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='" + sport_abbrev + "']").click()
    # Waits until stat container element is viewable 
    stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

    ppPlayers = []
    # Finding all the stat elements within the stat-container
    categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

    # Collecting categories
    for category in categories:
        driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

        projectionsPP = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

        for projections in projectionsPP:
            names = projections.find_element(By.CLASS_NAME, "name").text
            value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
            proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

            players = {
                'Name': names,
                'Value': value,
                'Prop': proptype.replace("<wbr>", "")
            }
            ppPlayers.append(players)

    dfProps = pd.DataFrame(ppPlayers)
    dfProps.to_csv('prizepicks_predictor/backend/ppscrapper/past_lines/' + str(date.today()) + "_" + sport_abbrev)

    print("Retrieved the props offered by PP for" + sport_abbrev + ".", '\n')
    print(dfProps)
    print('\n')


getPPProps("MLB")