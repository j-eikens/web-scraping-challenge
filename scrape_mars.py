from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape():
    #scraping news_title and news_p
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = articles = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    
    browser.quit()

    #scrapping featured image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find_all('img', class_='fancybox-image')[0]['src']
        
    featured_image_url = f'{url}{image}'

    browser.quit()

    #scrapping Mars facts
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table = mars_table.rename({0: "Description", 1:"Mars", 2:"Earth" }, axis='columns')
    mars_table = mars_table.set_index('Description')
    html_table = mars_table.to_html()

    #scrapping Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #create title list
    div = soup.find_all('div', class_='item')

    title_list = []

    for i in div:
        desc = i.find('div', class_='description')
        title_full = desc.find('h3').text
        title = title_full.replace(" Enhanced", "")
        
        title_list.append(title)


    #storing image urls in image_url_list
    image_url_list = []

    for title in title_list:
        browser.links.find_by_partial_text(title).click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #find image URL
        image = soup.find_all('div', class_='downloads')



        for i in image:
            li = i.find('li')
            a = li.find('a')
            link = a['href']
        
            image_url = f'{url}{link}'
        
            image_url_list.append(image_url)
        
        browser.links.find_by_partial_text('Back').click()
    
    browser.quit()

    hemisphere_image_urls = []

    for i in range(len(title_list)):
        dict = {'title': title_list[i], 'img_url':image_url_list[i]}
            
        hemisphere_image_urls.append(dict)

    #### creating final dictionary
    mars_dict = {}
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p
    mars_dict['featured_img_url'] = featured_image_url
    mars_dict['hemisphere_img_url'] = hemisphere_image_urls
    mars_dict['table'] = html_table
    
    return mars_dict
