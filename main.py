#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pathlib
import sys
from pynput import keyboard
from pynput.keyboard import Key
from utils import parse_config, parse_df

config = parse_config()


# In[ ]:


search_university = config["search"][0]["url"]
search_scholar = config["search"][1]["url"]
data_path = config["directory"]["path"]

df = parse_df(data_path)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# In[ ]:


def on_event(driver, df):
    def search_on_scholar(driver):
        query = driver.execute_script("return window.getSelection().toString()")
        driver.get(search_scholar.format(query))

    def update_department(driver, df):
        department = driver.execute_script("return window.getSelection().toString()")
        df.loc[i, ["department"]] = department.strip()
        print(f"department: {department}")

    def update_name(driver, df):
        name = driver.execute_script("return window.getSelection().toString()")
        df.loc[i, ["name"]] = name.strip()
        print(f"name: {name}")

    def update_email(driver, df):
        email = driver.execute_script("return window.getSelection().toString()")
        df.loc[i, ["email"]] = email.strip()
        print(f"email: {email}")

    def update_topic(driver, df):
        topic = driver.execute_script("return window.getSelection().toString()")
        df.loc[i, ["topic"]] = topic.strip()
        print(f"topic: {topic}")
        
    def on_press(key):
        try:
            if key == Key.esc:
                return False
            elif key.char == "a":
                update_department(driver, df)
            elif key.char == "s":
                update_name(driver, df)
            elif key.char == "d":
                update_email(driver, df)
            elif key.char == "f":
                update_topic(driver, df)
            elif key.char == "z":
                search_on_scholar(driver)
        except:
            pass

    return on_press

def on_release(key):
    if key == keyboard.Key.esc:
        return False

init_handle = driver.current_window_handle

for i in range(len(df)):
    # Search University
    topic = df.loc[i, ["topic"]].item()
    print(topic)
    if topic != "":
        continue
    query = df.loc[i, ["university"]].item()
    driver.get(search_university.format(query))

    with keyboard.Listener(on_press=on_event(driver, df)) as listener:
        listener.join()

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != init_handle:
            driver.close()

    driver.switch_to.window(init_handle)


    df.to_csv(data_path, index=False)
