# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) #True will have no window preview
    
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }
   # Stop webdriver and return data
    browser.quit()
    return data


### First Scrape
def mars_news(browser):
    # Visit the mars nasa news site
    # url = 'https://redplanetscience.com'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html' #provided by module
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    # slide_elem = news_soup.select_one('div.list_text') # this was moved to inside the try statement
    # slide_elem.find('div', class_='content_title') # this was moved to inside the try statement

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_p
    
    return news_title, news_p

### Featured Images
def featured_image(browser):
    # Visit URL
    # url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html' #provided by module
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # include try error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    # img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}' #provided by module
    
    
    return img_url


## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None
   
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

## Hemispheres
def hemispheres(browser):
    ### Hemispheres
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    divs = hemi_soup.find("div", class_='collapsible results')
    anchors = divs.find_all('a')
    relative_urls = set([anchor['href'] for anchor in anchors])
    # print(f'Found {len(relative_urls)} URLs')

    a = 0

    for clicks in range(4):
        
        full_image_elem = browser.find_by_tag('h3')[a]
        full_image_elem.click()
        
        # parse new html for information
        html = browser.html
        urls_soup = soup(html, 'html.parser')

        # grab titles
        title = urls_soup.find('h2', class_='title').get_text()
        title = title.replace (" Enhanced","",)
        # print(f'title: {title}')

        # grab image url
        downloads_div = urls_soup.find('div', class_='downloads')
        img_url = downloads_div.find('a')['href']
        full_img_url = url + img_url
        # print(f'--> url: {full_img_url}')
        
        hemispheres = {
            'img_url': full_img_url,
            'title': title,
        }
        
        hemisphere_image_urls.append(hemispheres)

        a += 1
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


