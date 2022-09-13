#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pathlib
import sys
import keyboard

from utils import parse_config, parse_df

config = parse_config()


# In[ ]:


search_university = config["search"][0]["url"]
search_scholar = config["search"][1]["url"]
driver_path = config["driver"]["path"]
data_path = config["directory"]["path"]

df = parse_df(data_path)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# In[ ]:

def search_on_scholar(driver):
    query = driver.execute_script("return window.getSelection().toString()")
    driver.get(search_scholar.format(query))

def update_department(driver):
    department = driver.execute_script("return window.getSelection().toString()")
    df.loc[i, ["department"]] = department.strip()

def update_name(driver):
    name = driver.execute_script("return window.getSelection().toString()")
    df.loc[i, ["name"]] = name.strip()

def update_email(driver):
    email = driver.execute_script("return window.getSelection().toString()")
    df.loc[i, ["email"]] = email.strip()

def update_topic(driver):
    topic = driver.execute_script("return window.getSelection().toString()")
    df.loc[i, ["topic"]] = topic.strip()

init_handle = driver.current_window_handle

for i in range(len(df)):
    # Search University
    topic = df.loc[i, ["topic"]].item()
    print(topic)
    if topic != "":
        continue
    query = df.loc[i, ["university"]].item()
    driver.get(search_university.format(query))

    keyboard.read_key()
    keyboard.add_hotkey("z", search_on_scholar, args=(driver,))
    keyboard.add_hotkey("a", update_department, args=(driver,))
    keyboard.add_hotkey("s", update_name, args=(driver,))
    keyboard.add_hotkey("d", update_email, args=(driver,))
    keyboard.add_hotkey("f", update_topic, args=(driver,))

    keyboard.wait("esc")

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != init_handle:
            driver.close()

    driver.switch_to.window(init_handle)


    df.to_csv(data_path, index=False)
