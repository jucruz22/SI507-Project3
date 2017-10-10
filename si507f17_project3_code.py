from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
gallery_data = requests.get("http://newmantaylor.com/gallery.html").text # creates response object
soup = BeautifulSoup(gallery_data, 'html.parser') # creates soup HTML object
images = soup.find("body").find_all("img") # list of HTML image objects
# print (images) it worked!
for i in images:
    try:
        print (i["alt"]) #print alt text
    except:
        print ("No alt text provided for this image!") # if no alt attribute


######### PART 1 #########

# Get the main page data...try to get and cache main page data if not yet cached
def get_from_cache(url,file_name):
    try:
        html = open(file_name,'r').read()
    except:
        html = requests.get(url).text # request object FIRST and use .text to convert it to a string
        f = open(file_name,'w')
        f.write(html)
        f.close()
    return html

# creating soup object from cache step
nps_gov_html = get_from_cache('https://www.nps.gov/index.htm','nps_gov_data.html')
nps_soup = BeautifulSoup(nps_gov_html, 'html.parser')
states_list = nps_soup.find("ul",{"class":"dropdown-menu SearchBar-keywordSearch"}).find_all("li")
# print (states_list)

# retrieving individual state URL's
state_urls = ['https://www.nps.gov' + s.find('a')['href'] for s in states_list] # example str format: '/state/al/index.htm'
# print (state_urls)

# function to get individual state URL
def get_state_url(state_code='mi'):
    for u in state_urls:
        if state_code == u.split('/')[4]:
            return (u)

ar_url = get_state_url('ar')
ca_url = get_state_url('ca')
mi_url = get_state_url('mi')
# print (ar_url) # success!
# print (ca_url) # success!
# print (mi_url) # success!

#HTML cach + soup for three states
ar_html = get_from_cache(ar_url,'arkansas_data.html') # HTML string
ar_soup = BeautifulSoup(ar_html, 'html.parser') # HTML soup object

ca_html = get_from_cache(ca_url,'california_data.html') # HTML string
ca_soup = BeautifulSoup(ca_html, 'html.parser') # HTML soup object

mi_html = get_from_cache(mi_url,'michigan_data.html') # HTML string
mi_soup = BeautifulSoup(mi_html, 'html.parser') # HTML soup object


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:
def get_park_soup_list(state_soup):
    soup_list = state_soup.find("ul",{"id":"list_parks"}).find_all("li",{"class":"clearfix"})
    return (soup_list) # list HTML soup objects, each representing one "blurb" of a national park found on an individual state

def get_park_urls(state_soup):
    parks_list = get_park_soup_list(state_soup)
    park_urls = []
    for p in parks_list:
        park_repo = p.find('h3').find('a')['href'] # /arpo/
        park_urls.append('https://www.nps.gov'+park_repo+'index.htm') # https://www.nps.gov/arpo/index.htm
    return (park_urls) # list of parks/sites/memorial URLs within in each state page

# test functions using Arkansas state page
ar_park_urls = get_park_urls(ar_soup) # list of AR park URLS
# print (ar_park_urls)
ar_park_soup_list = get_park_soup_list(ar_soup)
# print (ar_park_soup_list)
sample_ar_park = ar_park_soup_list[0]
# print ('PRINTING SAMPLE AR PARK SOUP\n',sample_ar_park.prettify()) # HTML subjection object


## Define your class NationalSite here:
class NationalSite(object):
    def __init__(self,park_soup):
        try:
            self.location = park_soup.find('h4').text
            self.name = park_soup.find('h3').find('a').text
            self.type = park_soup.find('h2').text
            self.description = park_soup.find('p').text.strip()
            self.url = 'https://www.nps.gov'+park_soup.find('h3').find('a')['href']+'index.htm'
        except:
            self.location = None
            self.name = None
            self.type = None
            self.description = ""
            self.url = ""

    def __str__(self):
        return ('{} | {}'.format(self.name,self.location))

    def __contains__(self,word):
        return word in self.name

    def get_mailing_address(self):
        park_page = requests.get(self.url) # request this page from the internet
        soup = BeautifulSoup(park_page.content,'html.parser') # make a soup object of whole HTML page
        mailing = soup.find('div',{'class':'mailing-address'})
        try:
            streetAddress = mailing.find('span',{'itemprop':'streetAddress'}).text.strip()
            addressLocality = mailing.find('span',{'itemprop':'addressLocality'}).text.strip()
            addressRegion = mailing.find('span',{'itemprop':'addressRegion'}).text.strip()
            postalCode = mailing.find('span',{'itemprop':'postalCode'}).text.strip()
        except:
            streetAddress = ""
            addressLocality = ""
            addressRegion = ""
            postalCode = ""
        return ('{} / {} / {} / {}').format(streetAddress,addressLocality,addressRegion,postalCode)

'''TESTING PROBLEM 2'''
## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

f = open("sample_html_of_park.html",'r')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# print (soup_park_inst.prettify())
sample_inst = NationalSite(soup_park_inst)
sample_inst_2 = NationalSite(sample_ar_park)

# print (sample_inst) # Isle Royale | Houghton, MI
# print (sample_inst_2) # Arkansas Post | Gillett, AR
#
# print (sample_inst.url,'|',sample_inst_2.url)
#
# print ("Isle" in sample_inst.name)
#
# print (sample_inst.get_mailing_address()) # 800 East Lakeshore Drive / Houghton / MI / 49931
# print (sample_inst_2.get_mailing_address()) # 1741 Old Post Road / Gillett / AR / 72055

# print (sample_inst_2.csv_string())
# f.close()


######### PART 3 #########

# * Create a list of `NationalSite` objects from each one of these 3 states: Arkansas, California, and Michigan. They should be saved in the following variables, respectively:

arkansas_natl_sites = [NationalSite(p) for p in get_park_soup_list(ar_soup)]
california_natl_sites = [NationalSite(p) for p in get_park_soup_list(ca_soup)]
michigan_natl_sites = [NationalSite(p) for p in get_park_soup_list(mi_soup)]
# print (arkansas_natl_sites) # list of National Park instances!
# print (california_natl_sites) # list of National Park instances!
# print (michigan_natl_sites) # list of National Park instances!

##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)


######### PART 4 #########

def csv_content(file_name,list_name):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name','Location','Type','Address','Description'])
        for obj in list_name:
            writer.writerow([obj.name, obj.location, obj.type, obj.get_mailing_address(), obj.description])

csv_content("arkansas.csv",arkansas_natl_sites)
csv_content("california.csv",california_natl_sites)
csv_content("michigan.csv",michigan_natl_sites)

# csv_headers("california.csv")
# csv_headers("michigan.csv")



# * Write 3 CSV files, `arkansas.csv`, `california.csv`, `michigan.csv` -- one for each state's national parks/sites/etc, each of which has 5 columns:
#
# 	* Name
# 	* Location
# 	* Type
# 	* Address
# 	* Description
#
# Remember to handle e.g commas and multi-line strings so that data for 1 field all ends up inside 1 spreadsheet cell when you open the CSV!
#
# For any park/site/monument/etc where a value is `None`, you should put the string `"None"` in the CSV file.

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
