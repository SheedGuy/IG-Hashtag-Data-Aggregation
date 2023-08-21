from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv


def GetPostCountFromHashtag(hashtag):

    driver = webdriver.Chrome()
    driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')

    # wait for info to load
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_ac2a")))

    # grab HTML and get rid of driver
    everything = driver.page_source
    driver.quit()

    # parse HTML looking for post number then returning it
    soup = BeautifulSoup(everything, 'html.parser')
    number_span = soup.find('span', class_='_ac2a')

    numPosts = number_span.text.replace(',', '')

    return int(numPosts)

def InputHashtags():
    raw = input("Please input hashtag(s) without the # and separate them with commas: \n")
    lessRaw = raw.replace(' ', "")
    evenLessRaw = list(lessRaw.split(","))
    return evenLessRaw

hashtagList = InputHashtags()

hashtagPostDict = {}

with open('hashtagData.csv', 'w', newline='') as csvfile:
    fieldnames = ['hashtag', '# of posts']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for hashtag in hashtagList:
        writer.writerow({'hashtag': hashtag, '# of posts': GetPostCountFromHashtag(hashtag)})

# for hashtag in hashtagList:
#     hashtagPostDict[hashtag] = GetPostCountFromHashtag(hashtag)

print(hashtagPostDict)