from django.db import models
from ckeditor.fields import RichTextField
##add wordpress function, enable user to edit
from django.template.defaultfilters import slugify
###create a new, clean url under new,usinf data already obtain
###like:https://xxxx.com/ dfyua/creator/work
# Create your models here.
import datetime

class rsvp(models.Model):
		name=models.CharField(max_length=200, null=True)
		email=models.CharField(max_length=200, null=True)
		note=RichTextField(blank=True)
		
		def __str__(self):
				return self.name
				
class Item(models.Model):
		title = models.CharField(max_length=30)
		description=RichTextField()
		attributes = models.TextField()
		###attributes include creator,collectins, tags in plain text
		slug= models.SlugField(max_length=30)
		files=models.FileField(upload_to='media/')
		url=models.URLField(max_length=200)
		date = models.DateField(default=datetime.date.today)
		def save(self,*args, **kwargs):
						if not self.id:
									self.slug=slugify(self.title)
						super(Item, self).save(*args, **kwargs)
		def __str__(self):
					return self.title

class language(models.Model):
		language = models.CharField(max_length =20, help_text="Enter the language of this book")
		
		def __str__(self):
				return self.language
							
