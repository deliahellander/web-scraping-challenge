
# %%
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager


# %%
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

mars_info = {}

# %%
def scrape_info():
    url = ('https://mars.nasa.gov/news/')
    browser.visit(url)


    # %%
    # HTML Object
    html_news = browser.html
    soup = bs(html_news, "html.parser")

    # Scrape the latest News Title and Paragraph Text
    news_title = soup.find("div", class_ = "content_title").text
    news_p = soup.find("div", class_ = "article_teaser_body").text

    # Display scrapped news 
    print(news_title)
    print("-----------------------------------------")
    print(news_p)

    # %% [markdown]
    # # JPL Mars Space Images - Featured Image

    # %%
    # Visit JPL Featured Space Image
    spaceimage_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(spaceimage_url)


    # %%
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
    # assign the url string to a variable
    img_html = browser.html
    img_soup = bs(img_html, "html.parser")

    #Make sure to find the image url to the full size .jpg image.
    featured_image = img_soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]

    # Make sure to save a complete url string for this image.
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image}"
    print("JPL Featured Space Image")
    print("-----------------------------------------")
    print(featured_image_url)

    # %% [markdown]
    # # Mars Facts

    # %%
    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts


    # %%
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ["Description", "Value"]
    # Set index to Description
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_df.head()


    # %%
    # Use Pandas to convert the data to a HTML table string.
    mars_facts_html_table = mars_facts_df.to_html()
    # stripping away unwanted new lines to clean up the table
    mars_facts_html_table.replace('\n', '')
    mars_facts_html_table

    # %% [markdown]
    # # Mars Hemispheres

    # %%
    # Using splinter to visit the USGS Astrogeology Science Center url
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, "html.parser")


    # %%
    # Retrieve the parent divs for all items
    hemispheres = soup.find_all("div", class_="item")

    # Create empty list
    hemispheres_info = []

    # Sign main url for loop
    hemispheres_url = "https://astrogeology.usgs.gov"

    # Loop through the list of all hemispheres information
    for hemisphere in hemispheres:
        hemisphere_title = hemisphere.find("h3").text
        hemispheres_img = hemisphere.find("a", class_="itemLink product-item")["href"]
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        web_info = bs(image_html, "html.parser")
        
        # Create full image url
        img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
        
        hemispheres_info.append({"title" : hemisphere_title, "img_url" : img_url})

    #display titles and images
        print("")
        print(hemisphere_title)
        print(img_url)
        print("-----------------------------------------")

    # Close the browser after scraping
	browser.quit()
	
return mars_info
	
	