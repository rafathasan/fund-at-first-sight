#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

driver = webdriver.Chrome(driver_path)


# In[ ]:


for i in range(len(df)):
    query = df.loc[i, ["university"]].item()
    driver.get(search_university.format(query))

    while True:
        if keyboard.is_pressed("spacebar"):
            break
    name = driver.execute_script("return window.getSelection().toString()")
    df.loc[i, ["name"]] = name

    while True:
        if keyboard.is_pressed("spacebar"):
            break
    email = driver.execute_script("return window.getSelection().toString()")
    df.loc[i, ["email"]] = email


# In[ ]:


driver.get(search_scholar.format("W Li"))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




