# Web-Scraping-Challenge
This challenge uses Python, Pandas, Beautiful Soup, Splinter, PyMongo, Flask, and MongoDB to perform a web-scraping ETL workload. News, Images, and Data tables on Mars are scraped from multiple sources and then presented together on a single webpage.

## Scraping

Splinter was used to connect to, navigate, and save the html for each page visited. The code was then parsed using Beautiful soup, and the desired content extracted. This content was loaded into mongoDB using the PyMongo library for Python. 

![ETL Code Sample](https://github.com/bakerv/web-scraping-challenge/blob/main/Missions_to_Mars/Resources/ETL_Code_Sample.PNG)

## Presentation

A Flask app was created to correctly read the stored data from mongoDB into an HTML template. Included in the template is a button to rescrape all data sources, update the contents of the database, and then refresh the webpage with the new data. This allows users to view freshly scraped data on demand. 

![Website Sample](https://github.com/bakerv/web-scraping-challenge/blob/main/Missions_to_Mars/Resources/Webpage_Sample.PNG)


## Data Sources:

*Nasa's Mars Exploration Program*. NASA Mars Exploration Program and Jet Propulsion Laboratory, https://mars.nasa.gov/. Accessed 16 June 2021.

*Astrogeology Science Center*. U.S. Geological Survey, https://astrogeology.usgs.gov. Accessed 16 June 2021.

*Mars Facts - Interesting Facts About Mars.* Space Facts, https://space-facts.com/mars. Accessed 16 June 2021





