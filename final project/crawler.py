from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import traceback

url = 'https://www.linkedin.com/jobs/search/?currentJobId=3193692261&geoId=103644278&keywords=software%20engineer%20new%20grad&location=United%20States&refresh=true'

wd = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver.exe')
wd.get(url)
wd.fullscreen_window(); 

no_of_jobs = int(wd.find_element(By.CSS_SELECTOR, 'h1>span').get_attribute('innerText'))

i = 2
lastHeight = wd.execute_script("return document.body.scrollHeight")

# 25 ->test: 100
while i <= int(no_of_jobs/100)+1:
    # Scroll down to bottom
    wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(2)
    newHeight = wd.execute_script("return document.body.scrollHeight")   
    try:
        see_more_jobs_button = wd.find_element(By.XPATH, "/html/body/div[1]/div/main/section[2]/button")
        wd.execute_script("arguments[0].click();", see_more_jobs_button)
        time.sleep(2)
    except:
        traceback.print_exc()
        wd.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        newHeight = wd.execute_script("return document.body.scrollHeight")
        print(newHeight)
        time.sleep(2)
    i = i + 1

job_lists = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
jobs = job_lists.find_elements(By.TAG_NAME,'li') # return a list

print(len(jobs))
job_title_list = []
location_list = []
company_name_list = []
date_list = []
job_link_list = []

for job in jobs:
    job_title = job.find_element(By.CSS_SELECTOR, "h3").get_attribute("innerText");
    job_title_list.append(job_title)

     #company_name
    company_name = job.find_element(By.CSS_SELECTOR,"h4").get_attribute("innerText")
    company_name_list.append(company_name)
    
    #location
    location = job.find_element(By.CSS_SELECTOR,"div>div>span").get_attribute("innerText")
    location_list.append(location)
    
    #date
    date = job.find_element(By.CSS_SELECTOR,"div>div>time").get_attribute("datetime")
    date_list.append(date)
    
    #job_link
    job_link = job.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
    job_link_list.append(job_link)

    jd = [] #job_description

seniority = []
emp_type = []
job_func = []
job_ind = []

for item in range(len(jobs)):
    print(item)
    job_func0=[]
    industries0=[]
    # clicking job to view job details
    
    #__________________________________________________________________________ JOB Link
    
    try: 
        job_click_path = f'/html/body/div/div/main/section/ul/li[{item+1}]'
        job_click = job.find_element(By.XPATH,job_click_path).click()
    except:
        pass
    #job_click = job.find_element(By.XPATH,'.//a[@class="base-card_full-link"]')
    
    #__________________________________________________________________________ JOB Description
    jd_path = '/html/body/div/div/section/div/div/section/div/div/section/div'
    try:
        jd0 = job.find_element(By.XPATH,jd_path).get_attribute('innerText')
        jd.append(jd0)
    except:
        jd.append(None)
        pass
    
    #__________________________________________________________________________ JOB Seniority
    seniority_path='/html/body/div/div/section/div/div/section/div/ul/li[1]/span'
    
    try:
        seniority0 = job.find_element(By.XPATH,seniority_path).get_attribute('innerText')
        seniority.append(seniority0)
    except:
        seniority.append(None)
        pass

    #__________________________________________________________________________ JOB Time
    emp_type_path='/html/body/div/div/section/div/div/section/div/ul/li[2]/span'
    
    try:
        emp_type0 = job.find_element(By.XPATH,emp_type_path).get_attribute('innerText')
        emp_type.append(emp_type0)
    except:
        emp_type.append(None)
        pass
    
    #__________________________________________________________________________ JOB Function
    function_path='/html/body/div/div/section/div/div/section/div/ul/li[3]/span'
    
    try:
        func0 = job.find_element(By.XPATH,function_path).get_attribute('innerText')
        job_func.append(func0)
    except:
        job_func.append(None)
        pass

    #__________________________________________________________________________ JOB Industry
    industry_path='/html/body/div/div/section/div/div/section/div/ul/li[4]/span'
    
    try:
        ind0 = job.find_element(By.XPATH,industry_path).get_attribute('innerText')
        job_ind.append(ind0)
    except:
        job_ind.append(None)
        pass
    
    print("Current at: ", item, "Percentage at: ", (item+1)/len(jobs)*100, "%")

job_data = pd.DataFrame({
    'Date': date,
    'Company': company_name,
    'Title': job_title,
    'Location': location,
    'Description': jd,
    'Level': seniority,
    'Type': emp_type,
    'Function': job_func,
    'Industry': job_ind,
    'Link': job_link
})

print(job_data)