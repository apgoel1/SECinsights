'''
getting data from SEC database using API
'''

import requests
# for easy working with websites (https)
# creates a response object that encapsulates the information returned by the server, such as status codes, headers, and the response body.
import pandas as pd
# useful for working with data frames and tables

headers = {'User-Agent' : "aditya.goel.tx@gmail.com"}
# dictionary with email used to id myself when making requests to api

companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers = headers)
# request the information of each co's CIK
# the companyTickers object is a dictionary at this point.
    # the key is just an int from 0 to whatever
    # the value is a list of nested dictionaries with cik_str, ticker, and title

# print(companyTickers.json()  ### this prints the entire dictionary with the names of the companies
print(companyTickers.json().keys())
# this only shows the keys

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']
# method for getting the information out of the first key

# parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']
# produces the CIK for this key

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')
# convert the dictionary to a dataframe using the index, the columns are the cik, ticker, and title


# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)
# makes every cik 10 digits long by filling in leading 0s

# review data
print(companyData[:1])
# will show entries [start:finish-1]

cik = companyData[0:1].cik_str[0]
# takes the cik of the first company (Nvidia as of now)
    # need the [0] bc that pulls the string value of the cik for row 1. (think of cik_str as a column with indicies)

# get company specific filing metadata
filingMetadata = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json',headers=headers)
# the link is an endpoint for finding what available financial information is available
    # headers = headers required by sec api for all data requests

### MUST REMEMBER THAT filingMetadata IS ONLY THE INFORMATION FOR ONE COMPANY 

# review json 
print(filingMetadata.json().keys()) # shows the available information for the company specified (the cik in the link)
filingMetadata.json()['filings'] # goes to the dictionary for the filings
filingMetadata.json()['filings'].keys() 
filingMetadata.json()['filings']['recent'] # another dict
filingMetadata.json()['filings']['recent'].keys() # finally see all the data, including accession#, date, etc.

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(filingMetadata.json()['filings']['recent'])
# this gives a dataframe with each row giving a form/filing of the given company and the columns providing details (accession#, date, etc) about that form/filing


# review columns
allForms.columns # tells us what all columns we have available
allForms[['accessionNumber', 'reportDate', 'form']].head(50) # shows the first 50 rows/files

# 10-Q metadata
allForms.iloc[99] # grabs the information for the file at index [xx]

# get company facts data
companyFacts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json', headers=headers)


#review data
companyFacts.json().keys() # bunch of dictionaries
companyFacts.json()['facts'] # more dictionaries 
companyFacts.json()['facts'].keys() 

# filing metadata
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding'].keys()
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'] # wow so many nested dicts. finally reach a list
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][0] # taking the first item in the list
# this item is still metadata for specific filings. gives date, form, AND THE VALUE IS THE VALUE OF THE COMMON STOCK SHARES OUTSTANDING

# concept data // financial statement line items
companyFacts.json()['facts']['us-gaap']
companyFacts.json()['facts']['us-gaap'].keys() # gives us line items from financial statemnts

# different amounts of data available per concept
companyFacts.json()['facts']['us-gaap']['AccountsPayableCurrent'] # gives key and label for description and the values for each form
companyFacts.json()['facts']['us-gaap']['Revenues']
companyFacts.json()['facts']['us-gaap']['Assets']
# each of these line items gives a different amount of data, so must consider this when parsing thru

# get company concept data
companyConcept = requests.get((f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'f'/us-gaap/Assets.json'), headers=headers)
# here, the line item "Assets" is hard coded. can introduce another variable there to adjust it

# review data
companyConcept.json().keys() 
companyConcept.json()['units']
companyConcept.json()['units'].keys()
companyConcept.json()['units']['USD']
companyConcept.json()['units']['USD'][0] #grab the first item in the list. we can see the form name and a value (which is assets in this hardcoded example)

# parse assets from single filing
companyConcept.json()['units']['USD'][0]['val'] # grabs the actual asset value

# get all filings data 
assetsData = pd.DataFrame.from_dict((companyConcept.json()['units']['USD']))

# review data
assetsData.columns # shows the columns
assetsData.form # only shows the type of form 

# get assets from 10Q forms and reset index
assets10Q = assetsData[assetsData.form == '10-Q']
assets10Q = assets10Q.reset_index(drop=True) # resets the index ordering to 0 1 2 3 compared to just keeping the original index, which would have gaps because we only picked out the 10-Q forms

# plot 
assets10Q.plot(x='end', y='val') 
# provides a plot of the assets value over time, with data from the forms that we have selected
# in this example, the company is NVIDIA