from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import urllib2
import time
import csv
import sys
import os
from pip._vendor.distlib.compat import raw_input
from _io import open
from locale import str

def main():
    if os.path.isfile("list.txt") == False:
        print "list.txt not found"
        sys.exit()
        
    print "These companies will be used:"
    file = open("list.txt", 'r')
    for line in file:
        print line,
        if 'str' in line:
            break
    raw_input("\nPress Enter to continue...")
    print "Please wait..."
    
    # Creates output folder
    if not os.path.exists(os.getcwd() + "/output"):
        os.mkdir(os.getcwd() + "/output")
    data = open(os.getcwd() + "/output/" + "data.xml", 'w')
    data.write(u"<data>\n")
    driver = webdriver.Firefox()
    file = open("list.txt", 'r')
    for line in file:
        if line == "":
            continue
        print "Now parsing through: " + line,
        line = line.strip()
        data.write("\t<entry>\n\t<name>" + line + "</name>\n\t")
        # Searching Facebook
        print "Checking facebook..."
        driver.get("https://www.bing.com/search?q=" + line + "+facebook")
        time.sleep(10)
        main_window = driver.current_window_handle
        ListlinkerHref = driver.find_elements_by_xpath("//*[@href]")
        hrefList = []
        for link in ListlinkerHref:
            hrefList.append(link.get_attribute("href"))
            
        # Finding the Facebook page and retrieving number of likes
        for href in hrefList:
            if "https://www.facebook.com" in href:
                print "Checking " + href
                driver.get(href)
                driver.switch_to_window(main_window)
                time.sleep(10)
                if check_exists_by_id(driver, "PagesLikesCountDOMID"):
                    element = driver.find_element_by_id("PagesLikesCountDOMID")
                    s = element.text
                    s = s.replace("likes", "")
                    data.write("<facebook>" + s + "</facebook>\n\t")
                    break;
                
        # Searching Twitter
        print "Checking twitter..."
        driver.get("https://www.bing.com/search?q=" + line + "+twitter")
        time.sleep(10)
        main_window = driver.current_window_handle
        ListlinkerHref = driver.find_elements_by_xpath("//*[@href]")
        hrefList = []
        for link in ListlinkerHref:
            hrefList.append(link.get_attribute("href"))
            
        # Finding the twitter page and retrieving number of followers
        for href in hrefList:
            if "https://twitter.com" in href:
                print "Checking " + href
                driver.get(href)
                driver.switch_to_window(main_window)
                time.sleep(10)
                if check_exists_by_css(driver, "li.ProfileNav-item.ProfileNav-item--followers"):
                    element = driver.find_element_by_css_selector("li.ProfileNav-item.ProfileNav-item--followers")
                    s = element.text
                    s = s.replace("\n", "")
                    s = s.replace("FOLLOWERS", "")
                    data.write("<twitter>" + s + "</twitter>\n\t")
                    break;
        
        # Finding the linkedin page and retrieving number of followers
        print "Checking linkedin..."
        driver.get("https://www.bing.com/search?q=" + line + "+linkedin")
        time.sleep(10)
        main_window = driver.current_window_handle
        ListlinkerHref = driver.find_elements_by_xpath("//*[@href]")
        hrefList = []
        for link in ListlinkerHref:
            hrefList.append(link.get_attribute("href"))
            
        # Finding the twitter page and retrieving number of followers
        for href in hrefList:
            if "https://www.linkedin.com" in href:
                print "Checking " + href
                driver.get(href)
                driver.switch_to_window(main_window)
                time.sleep(10)
                if check_exists_by_css(driver, "p.followers-count"):
                    element = driver.find_element_by_css_selector("p.followers-count")
                    s = element.text
                    s = s.replace("\n", "")
                    s = s.replace("followers", "")
                    data.write("<linkedin>" + s + "</linkedin>\n")
                    break;
        
        data.write(u"\t</entry>\n")
    data.write(u"</data>")
    data.close()
    driver.close()
    print "\nOutput written to text"
    
def check_exists_by_id(driver, idDom):
    try:
        driver.find_element_by_id(idDom)
    except:
        return False
    return True

def check_exists_by_css(driver, classDom):
    try:
        driver.find_element_by_css_selector(classDom)
    except:
        return False
    return True
     
if __name__ == '__main__':
    main()