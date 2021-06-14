import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pymongo
from pprint import pprint
from flask import Flask
from flask_pymongo import Pymongo

#urls to scrape
nasamarsurl = "https://mars.nasa.gov/news/"
nasajplurl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
sfurl = "https://space-facts.com/mars/"
usgsurl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

# connection path for splinter browser
driverpath = {'executable_path':'Resources/chromedriver.exe'}

#connection to mongodb
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#mongodb database paths
nasamars_collection = client.mission_to_mars.nasamars
jplimages_collection = client.mission_to_mars.jplimages
spacefacts_collection = client.mission_to_mars.spacefacts
usgsimages_collection = client.mission_to_mars.usgsimages
scrape_collection = client.mission_to_mars.scrape

def pull_data(scrapeurl):
    """
    Access the specified url, and return the html contents of the entire page
        Args:
            scrapeurl (str): the URL of the page you wish to scrape 
    """
    browser = Browser('chrome',**driverpath, headless=False)
    browser.visit(scrapeurl)
    rawdata = browser.html
    browser.quit()

    return rawdata

def nasamars_scraper(scrapeurl,collection):
    '''
    Access the Nasa Mars News Site and return the article titles, summarys, and dates in dictionary format
        Args:
            scrapeurl (str): url of the site to be scraped
            collection (obj): mongodb collection to save the data to, connected using MongoClient
    '''
    def clean_data(rawdata,collection):
        # clear database to prevent duplicate entries
        collection.drop()

        #parse the sites html code into a searchable list
        soup = bs(rawdata, 'html.parser')

        # put the html structure for each article into a list
        content = (soup
                    .find('section', class_='grid_gallery module list_view')
                    .find_all('div', class_= 'list_text'))

        for entry in content:
        # iterate through the list and return desired attributes for each article
            try:
                #extract desired attributes
                title = (entry.find('a').text)
                summary = (entry.find('div', class_= 'article_teaser_body').text)
                date = (entry.find('div', class_ = 'list_date').text)
                url = entry.a['href']

                #save to mongoDB
                document = {
                    'title': title,
                    'summary': summary,
                    'date': date,
                    'url': url
                }
                collection.insert_one(document)

            except Exception as error:
                print(error)
                
    rawdata = pull_data(scrapeurl)
    clean_data(rawdata,collection)
    
def usgs_scraper(scrapeurl,collection):
    '''
    Access composite mars hemisphere images obtained from the usgs
        Args:
            scrapeurl (str): url of the site to be scraped
            collection (obj): mongodb collection to save the data to, connected using MongoClient
    '''
    # parse the html code to locate URLs for each desired page
    def find_subpages(rawdata):

        soup = bs(rawdata, 'html.parser')
        subpages = soup.find_all('div', class_='item')
        links = [page.a['href'] for page in subpages]
        
        return links
    
    # parse through the html code to locate the desired information
    def clean_subpages(rawdata):
        
        soup = bs(rawdata, 'html.parser')
        download_url = soup.find('div', class_='content').a['href']
        img_url = soup.find('div', class_='downloads').a['href']
        title = soup.h2.text
        
        return [title,img_url,download_url]
    
    # Add information from each subpage to the document
    def load_data(links,collection):
        #clear database to prevent duplicate entries
        collection.drop()
        
        #create a list containing all subpage information
        document = []
        for link in links:
            try:
                rawdata = pull_data('http://astrogeology.usgs.gov' + link)
                cleandata = clean_subpages(rawdata)
                img_dict = {
                    'title': cleandata[0],
                    'img_url': cleandata[1],
                    'dowloand_url': cleandata[2]
                }
                document.append(img_dict)
                
            except Exception as error:
                print(error)
                
        #save to mongoDB       
        collection.insert_one({'USGS_Mars_Hemispheres':document})
        
        return document
                
    rawdata = pull_data(scrapeurl)
    links = find_subpages(rawdata)
    load_data(links,collection) 
    
def sf_scraper(scrapeurl,collection):
    '''
    Access mars data tables from spacefacts.com
        Args:
            scrapeurl (str): url of the site to be scraped
            collection (obj): mongodb collection to save the data to, connected using MongoClient
    '''
    # retrieve data from source and transform into a dictionary
    def extract_data(scrapeurl):
        # extract datatables from url
        rawdata = pd.read_html(scrapeurl)
        
        #transform first table into a dictionary
        sf_dict = {}
        for row,column in rawdata[0].iterrows():
            sf_dict[column[0]] = column[1]
            
        return sf_dict
    
    # save dictionary to mongoDB
    def load_data(document,collection):
        collection.drop()
        collection.insert_one(document)
        
    sf_dict = extract_data(scrapeurl)
    load_data(sf_dict,collection)
    
def scrape(collection):
    '''
    Run all scraping funcitons, and save the data to a single dictionary
        Args:
            collection (obj): mongodb collection to save the data to, connected using MongoClient
    '''
    #Scrape data and store it into mongoDB
    nasamars_scraper(nasamarsurl,nasamars_collection)
    usgs_scraper(usgsurl,usgsimages_collection)
    sf_scraper(sfurl,spacefacts_collection)
    
    #Read data from each collection into memory
    nasamars_content = [x for x in nasamars_collection.find()]
    usgs_content = [x for x in usgsimages_collection.find()]
    sf_content = [x for x in spacefacts_collection.find()]
    
    #store all data in a single dictionary
    document = {'Nasa_Mars_Exploration_Articles': nasamars_content,
                   'USGS_Mars_Hemisphere_Images': usgs_content,
                   'Space_Facts_Table': sf_content}

    #Save data to a mongoDB database
    collection.drop()
    collection.insert_one(document)