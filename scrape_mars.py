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

    articles = soup.find_all('div', class_='content_title')
    teaser = soup.find_all('div', class_='article_teaser_body')

    news_title = []
    news_p = []

    for i in articles:
        
        title = i.text
        news_title.append(title)
        
    for i in teaser:
        
        teaser_element = i.text
        news_p.append(teaser_element)
        
    browser.quit()

    #create results dictionary
    news_paragraph_dict = []

    for i in range(len(news_p)):
        dict = {'news_title': news_title[i], 'news_p':news_p[i]}
        
        news_paragraph_dict.append(dict)

    ######################
    #scrapping featured image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find_all('img', class_='fancybox-image')

    for i in image:
        featured_image = i['src']
        
    featured_image_url = f'{url}{featured_image}'

    browser.quit()

    #creating results dictionary
    featured_image_url_dict = {'featured_image_url': featured_image_url}

    #########
    #scrapping Mars facts
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_table = tables[1]
    html_table = mars_table.to_html()

    #results dictionary
    html_table_dictionary = {'html_table': html_table}

    #########
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

    #creating dictionary of results
    hemisphere_image_urls = []

    for i in range(len(title_list)):
        dict = {'title': title_list[i], 'img_url':image_url_list[i]}
        
        hemisphere_image_urls.append(dict)


    #########
    #creating composite results dictionary
    mars_dict = []

    mars_dict = hemisphere_image_urls
    mars_dict.extend(news_paragraph_dict)
    mars_dict.append(featured_image_url_dict)
    mars_dict.append(html_table_dictionary)


    return(mars_dict)