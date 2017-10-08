from bs4 import BeautifulSoup
import unittest
import requests

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
def get_state(state_code='mi',state_urls=state_urls):
    for u in state_urls:
        if state_code == u.split('/')[4]:
            return (u)
ar_url = get_state('ar')
ca_url = get_state('ca')
mi_url = get_state('mi')

# print (ar_url) # success!
# print (ca_url) # success!
# print (mi_url) # success!

#HTML cach + soup for three states
ar_html = get_from_cache(ar_url,'arkansas_data.html')
ar_soup = BeautifulSoup(ar_html, 'html.parser')

ca_html = get_from_cache(ca_url,'california_data.html')
ca_soup = BeautifulSoup(ca_html, 'html.parser')

mi_html = get_from_cache(mi_url,'michigan_data.html')
mi_soup = BeautifulSoup(mi_html, 'html.parser')


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...





## Define your class NationalSite here:





## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.




##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
