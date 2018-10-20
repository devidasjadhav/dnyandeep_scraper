import cookielib
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import csv
import re


cfile = open("dny1.csv",'wb')
# Store the cookies and create an opener that will hold them
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('User-agent', 'RedditTesting')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib2.install_opener(opener)

# The action/ target from the form
authentication_url = 'https://dnyandeepvadhuvar.com/index.php?r=site/login'
test_url = 'https://dnyandeepvadhuvar.com/index.php?r=DnyandeepVadhuVar/candidates/viewCandidate/id/'
# Input parameters we are going to send
payload = {
  'LoginForm[username]': '<userid>',
  'LoginForm[password]': '<password>'
  }

# Use urllib to encode the payload
data = urllib.urlencode(payload)

# Build our Request object (supplying 'data' makes it a POST)
req = urllib2.Request(authentication_url, data)

# Make the request and read the response
resp = urllib2.urlopen(req)
contents = resp.read()

durl = 'https://dnyandeepvadhuvar.com/index.php?r=DnyandeepVadhuVar/candidates/search&Candidate[candidate_id]=&Candidate[first_name]=&Candidate[last_name]=&Candidate[parent_native_district]=&Candidate[education]=Engineer&Candidate[age]=&Candidate[mangalik]=&Candidate[candidate_height]=&Candidate_page='
for i in range(1,4):
	aurl = durl + str(i)
	resp = urllib2.urlopen(aurl)
	contents = resp.read()

	soup = BeautifulSoup(contents, 'lxml')
	tbody = soup.find_all('td', width="120px" )
	for t in tbody:
		if t.text.isdigit():
			print int(t.text)
			out = t.text + ','
			curr_url = test_url + t.text
			resp = urllib2.urlopen(curr_url)
			contents = resp.read()
			soup = BeautifulSoup(contents, 'lxml')
			tables = soup.find_all('td', class_="candidateInformationText")
			out += soup.find('h3').text + ','
			for t in tables:
				temp = t.text.strip().replace('\n', '')
				test = re.sub("\s\s+" , " ", temp)
				out += test + ','
			print(out)
			out += '\n'
			cfile.write(out)
