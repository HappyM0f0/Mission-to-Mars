# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# print(slide_elem)
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# news_title
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# news_p
### Featured Images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# img_url_rel
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'

# img_url
# Visit URL
url = 'https://galaxyfacts-mars.com'
browser.visit(url)
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

# df
df.to_html()
browser.quit()

# Challenge starter code
# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

### Visit the NASA Mars News Site
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p
### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup
# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url
### Mars Facts
# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
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
###################################################
# ## building the url and going to it
# for relative_url in relative_urls:
#     hemispheres = {}
    
#     # go to each site via direct address
#     full_url = f'{url}{relative_url}'
#     browser.visit(full_url)
    
#     # using the buttons to move around
#     # full_image_elem = browser.find_by_text('Sample')
#     # full_image_elem.click()
#     # 

#     html = browser.html
#     urls_soup = soup(html, 'html.parser')
    
#     downloads_div = urls_soup.find('div', class_='downloads')
#     img_url = downloads_div.find('a')['href']
#     full_img_url = url + img_url
#     print(f'--> url: {full_img_url}')
    
#     title_elem = urls_soup.select_one('div.cover')
#     title = title_elem.find("h2", class_='title').get_text()
#     print(f'--> title: {title}')


#     hemispheres = {
#         'img_url': full_img_url,
#         'title': title,
#     }
#     hemisphere_image_urls.append(hemispheres)

# print('Done')
###################################################
# 3. Write code to retrieve the image urls and titles for each hemisphere.
a = 0
for clicks in relative_urls:
    
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
# 4. Print the list that holds the dictionary of each image url and title.
# hemisphere_image_urls 
# 5. Quit the browser
browser.quit()