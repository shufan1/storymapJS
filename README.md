
# Working with StoryMapJS in Django
This tutorial tries to explain how to create StoryMap from XML files in a Django project.

We create the Storymaps for QI project through a custom python manage.py command in `/management/commands/<command_name>.py,` store the data for Storymap as JSON object under /static/json, and get the Storymap JSON objects through Javascript on an HTML template. 
The command is finally excuted by calling `python manage.py <command_name> <aruguments>`.
The StoryMapJS JSON object should be a dictionary in the final.The structures of the JSON objects are defined on [StoryMapJS](https://storymap.knightlab.com/advanced/)

First, under your managemnt/commands directory, create a new python file, e.g. `generate.py`.

1. Include these following lines in the beginning:
```
from django.core.management.base import BaseCommand, CommandError
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import json
import xlrd
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
`*args` allows us to pass unknown number of arguments. In this case, we can pass two XML files at one time.

All the following steps and codes should go under `handle(self, *args, **options)`
5. Open the `XML` file(s)
			file_name = 'static/xml/' + xml_file + '.xml'
			workbook = xlrd.open_workbook('static/xls/TEI people, places, orgs.xlsx')
      worksheet = workbook.sheet_by_name('Places')#LOCATION
			tree = etree.parse(file_name)
			root = tree.getroot() 
      
