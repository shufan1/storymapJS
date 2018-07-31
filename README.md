
# Working with StoryMapJS in Django
This tutorial tries to explain how to create StoryMap from XML files using data from an Excel file stored as xlsx file in a Django project.

We create the Storymaps for QI project through a custom python manage.py command in `/management/commands/<command_name>.py,` store the data for Storymap as JSON object under /static/json, and get the Storymap JSON objects through Javascript on an HTML template. 
The command is finally excuted by calling `python manage.py <command_name> <aruguments>`.
The StoryMapJS JSON object should be a dictionary in the final.The structures of the JSON objects are defined on [StoryMapJS](https://storymap.knightlab.com/advanced/)

## Before you start:
In my project:
* The data of places, locations are stored as Excel files in the order of `id_tei, name, county, state, Latitude (N), Longitude (W)` under `static/xls`as an **xlsx** file.
* All manuscripts that are going to be used has already been transcribed into XML files, and stored under `static/xml`. 
* In your models, you need to have a ***Place*** class, and it includes two attributes: latitude and longitude

## Now let's begin the work.
* **I think I am only able to make slides** 

First, under your managemnt/commands directory, create a new python file, e.g. `generate.py`.
1. Include these following lines in the beginning:
```
from django.core.management.base import BaseCommand, CommandError
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import json
import xlrd #xlrd is a library for reading data and formatting information from Excel files, whether they are .xls or .xlsx files.
from bs4 import BeautifulSoup
from QI.models import Place   ##replace with your models.py and the model(s) you need
```
2. Start your custom manage.py command with these three lines
```
class Command(BaseCommand):
	args = 'Arguments is not needed'
	help = 'Django admin custom command'
``` 
3. add arguments that are going to be passed into the python function for generating StoryMaps later 
```
	def add_arguments(self, parser):
		parser.add_argument('xml_file', nargs='+', type=str)
```
4. define the command, and pass the arguments 
```
	def handle(self, *args, **options):
		for xml_file in options['xml_file']: 
```
`*args` allows us to pass unknown number of arguments. In this case, we can pass multipes XML files at one time.

**All the following steps from ***Step 5*** to ***Step 9*** and codes should go under `handle(self, *args, **options)`**

5. Open the `XML` file(s) and the xlsx file, parse both of them 
```
			file_name = 'static/xml/' + xml_file + '.xml'
			workbook = xlrd.open_workbook('static/xls/TEI people, places, orgs.xlsx')
                        worksheet = workbook.sheet_by_name('Places')#LOCATION, sheet_by_name is built-in function from xlrd
			tree = etree.parse(file_name)
			root = tree.getroot() 
```   
6. create a list of `<div>s or <p>s` in your XML files that you are going to iterate through, and create one slide for each onr of them.
For example, I get a list of <div>s with `type = entry` for my StoryMaps:
```
			entries = []
			for div in root.iter(ns + 'div'):
			if div.get('type') == 'entry':
			entries.append(div)
			print (entries)	
```
#You could always add `print()` in your command. Print statements will be excuted when you run `python manage.pt command_name arguments`. They will be helpful in debugging. 

7. Itterate thorugh the list your have made in ***Step 6***, and get the content you want to put into your StoryMap from XML file
e.g.:
```
			for f, e in enumerate(entries):
				div_text = ''
  			 	for child in e:
					if child.tag == 'p':
						text = etree.tostring(child, method='text')
						div_text == div_text+ "<br>" + child.text
						#because in my case, each entry has multiple <p>s
```				

For strings in headline, text, url, caption…, if you are intersted to see how we get them from xml files and our database, please check [generate.py].

8. Get the location on each slide of the map
i). you should be able to get the location from tags in your XML files under `<dateline>` tags,which should look like
`#<dateline><date when="xxx">xxx</date>.<placeName key="zz">yyy</placeName></dateline>`
** Under `for child in e:`, on the same level of `if child.tag == 'p':` in ***Step 6 ***
```
						if child.tag == "dateline":
							dateline = child
							for child in dateline:
								if child.tag == ns + "placeName":
									place = child.get("key")
```
ii). Get latitude and longitude of the place from your database
```
				dj_place_list = Place.objects.filter(id_tei=place) #this list should only have one object at most
				if dj_place_list==None or dj_place_list==list() or len(dj_place_list)==0: 		
					print (place, "not found in database \n")
					#if the place is not in database, we can't create a StoryMap slide for it.
				else: 
					for i in dj_place_list:
						if i.latitude != None:
							dj_place = i 
							break
							 #if it passes the if statement, skip the loop 
						else:
							dj_place = i
							# either case will allow us to get the only object in dj_place_list
					lat = dj_place.latitude
					lon = dj_place.longitude
```
iii). StoryMapJS requires the input of latitude and longitude to be of float type. Therefore, we make them float; otherwise, we can default latitude and longitude. StoryMapJS requires the input of latitude and longitude to be of float type. Therefore, we make them float; otherwise, we can default latitude and longitude. 
```
					if lat =="" or lon== "":
						print ("No lat or lon for",place,"I set this to lat to 42 and lon to 83. \n")
						lat = 42 #LOCATION
						lon = 83#LOCATION
					else:
						print (place, "had lat, lon:",lat,lon,"\n")
					try:
						float(lat)
					except ValueError:
						print ("People are bad at entering data, lat for this is:", lat)
						lat = 42
						print ("set lat to 42")
					try:
						float(lon)
					except ValueError:
						print ("People are bad at entering data, lon for this is:", lon)
						lon = 83
						print ("set lon to 83")	
```
9. create JSON object following the syntax on https://storymap.knightlab.com/advanced/

* **Overview** : Create a dictionary for each slide of your StoryMap, then a python array to hold each slide of your storymap, finally a dictionary which includes the python array and other attributes of the StoryMap.
1). Create a python array to hold each slide of your storymap.
Under ```for f, e in enumerate(entries):``` in ***Step 7***, on the same level of 
```
objects=[]
for slide in your_list #replace your_list with the list of 
  object = {
          location: {            // required for all slides except "overview" slide
          lat: decimal,      // latitude of point on map
          lon: decimal       // longitude of point on map
      },
      text: {                // optional if media present
          headline: string,
          text: string       // may contain HTML markup
      },
      media: {               // optional if text present
          url: string,       // url for featured media
          caption: string,   // optional; brief explanation of media content
          credit: string     // optional; creator of media content
      }
  }
  objects.append(object) #add each slide
```


