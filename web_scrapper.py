import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

#Getting the Page Source
def get_source(url):
     """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 

     """
     
     try:
          session = HTMLSession()
          response = session.get(url)
          return response
     except requests.exceptions.RequestException as e:
          print(e)

def scrape_google(query):
     query = urllib.parse.quote_plus(query) # Adding Plus instead space
     response = get_source("https://www.google.com/search?q=" + query)
     links = list(response.html.absolute_links)
     google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')
     for url in links[:]:
          if url.startswith(google_domains):
               links.remove(url)
    
     return links

def get_results(query):
     query = urllib.parse.quote_plus(query)
     response = get_source("https://www.google.com/search?q=" + query)

     return response

def parse_results(response , type):
     css_identifier_result = ".tF2Cxc"
     css_identifier_title = "h3"
     css_identifier_link = ".yuRUbf a"
     css_identifier_text = ".VwiC3b"
     
     results = response.html.find(css_identifier_result)
     output = []

     if type == "result":
          for result in results:
               item = {
                    'title':result.find(css_identifier_title,first = True).text,
                    'link' : result.find(css_identifier_link , first = True).attrs['href'],
                    'text' : result.find(css_identifier_text , first = True).text
               }

               output.append(item)
          # return output
     
     elif type == "title":
          for result in results:
               item = {
                    'title':result.find(css_identifier_title,first = True).text               
               }

               output.append(item)
          # return output
     
     elif type == "link":
          for result in results:
               item = {
                    'link' : result.find(css_identifier_link , first = True).attrs['href']               
               }

               output.append(item)
          # return output
     
     elif type == "text":
          for result in results:
               item = {
                    'text' : result.find(css_identifier_text , first = True).text
               }

               output.append(item)
     return output
     
     

def google_search(query , type):
     response = get_results(query)
     
     return parse_results(response , type)
