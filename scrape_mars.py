# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser

def scrape():

        mars_data = {}

        # Database Setup

        conn = 'mongodb://localhost:27017'
        client = pymongo.MongoClient(conn)

        db = client.mars_db
        collection = db.articles


        # ## Step 1 - Scraping

        # ## NASA Mars News

        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)

        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_title = soup.find('div', class_='content_title').a.text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_data['latest_news_title'] = news_title
        mars_data['latest_news_article_p'] = news_p


        # ## JPL Mars Space Images - Featured Image

        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        image_style = soup.find('article')['style']
        image_url = image_style.split("'")[1].split("'")[0]

        featured_image_url = 'https://www.jpl.nasa.gov' + image_url

        mars_data['featured_img'] = featured_image_url
        

        # ## Mars Weather

        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

        mars_data['weather_tweet'] = mars_weather


        # ## Mars Facts

        url = 'https://space-facts.com/mars/'
        tables = pd.read_html(url)

        mars_facts_df = tables[1]
        mars_facts_df.columns = ['Description', 'Value']
        mars_facts_df.set_index('Description', inplace=True)

        html_table = mars_facts_df.to_html()
        html_table = html_table.replace('\n', '')

        mars_data['html_table'] = html_table


        # ## Mars Hemispheres

        hemisphere_image_urls = []

        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        results = soup.find_all('div', class_='item')

        # Create for loop to get image url and title of all hemispheres 

        for result in results:
                link = result.find('h3').text
                title = link.replace(' Enhanced', '')
                browser.click_link_by_partial_text(link)
                html = browser.html
                soup = BeautifulSoup(html, 'html.parser')
                result2 = soup.find('img', class_='wide-image')
                url = 'https://astrogeology.usgs.gov/' + result2["src"]
                hemisphere_image_urls.append({"title":title, "img_url":url})
                browser.back()

        mars_data['hemisphere_imgs'] = hemisphere_image_urls

        return mars_data         