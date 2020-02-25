# import dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd



def scrape():
    # get article
    # requests call to page
    marspage = requests.get("https://mars.nasa.gov/news")
    # get page text
    marspagetext = bs(marspage.text,'html.parser')
    # get article title and body
    newstitle = marspagetext.find_all(class_='content_title')[0].a.text.strip()
    newspara = marspagetext.find_all(class_='rollover_description_inner')[0].text.strip()
    
    # get featured image
    # start up splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # navigate site
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    browser.click_link_by_id('full_image')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    imagepagetext = bs(html, 'lxml')
    browser.quit()
    imageurl = 'https://www.jpl.nasa.gov' + imagepagetext.find(class_='main_image')['src'].strip()

    # get twitter
    marstwitter = requests.get("https://twitter.com/marswxreport?lang=en")
    # get page text
    marstwittertext = bs(marstwitter.text,'html.parser')
    twitterweather = marstwittertext.find(class_="tweet-text").text.strip()

    # get mars facts
    # read facts page into dataframe
    tables = pd.read_html("https://space-facts.com/mars/")
    facts = pd.DataFrame(tables[0])
    facts = facts.rename(columns={0:'description',1:'value'})

    # get hemisphere pictures
    # start up splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # navigate site
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    mainhtml = browser.html
    mainhempagetext = bs(mainhtml, 'html.parser')
    links = mainhempagetext.find_all(class_='itemLink')
    browser.quit()
    # get titles and page links
    pageURLs = []
    titles = []
    for i in range(len(links)):
        try:
            title = links[i].text.strip('Enhanced').strip()
            link = "https://astrogeology.usgs.gov" + links[i]['href']
            if len(title) > 0:
                pageURLs.append(link)
                titles.append(title)
        except:
            pass
    # get image urls
    imagesources = []
    browser = Browser('chrome', **executable_path, headless=False)
    for link in pageURLs:
        browser.visit(link)
        pagehtml = browser.html
        pagehtmltext = bs(pagehtml, 'html.parser')
        imgsrc = "https://astrogeology.usgs.gov/" + pagehtmltext.find(class_="wide-image")['src'].strip()
        imagesources.append(imgsrc)
        
    hemisphereURLs = []
    for i in range(len(titles)):
        hemisphereURLs.append({'title':titles[i], 'img_url':imagesources[i]})
        
    # close browser
    browser.quit()

    fulldict = {
        "newsarticletitle":newstitle,
        "newsarticlepara":newspara,
        "featuredimage":imageurl,
        "twitterweather":twitterweather,
        "facts":facts.to_dict('records') ,
        "hemimageurls":hemisphereURLs
    }
    print(fulldict)
    return fulldict
