#form.py
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
import datetime
from django.db import models
from django.core.files.storage import FileSystemStorage
from initialapp.models import *

class rsvpForm(forms.ModelForm):
			note =  forms.CharField(widget=CKEditorWidget(), required=False)
			class Meta:
							fields = ['name', 'email', 'note']
							model = rsvp

##what are the differences between rsvpForm and rvsp

### build forms to accept input from site visitors,
### and then process and respond to the input.