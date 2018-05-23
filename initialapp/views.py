from django.shortcuts import render
from initialapp.forms import rsvpForm

# Create your views here.
def index(request):
		if request.method == 'POST':
				form = rsvpForm(request.POST)
				if form.is_valid():
					name = request.POST.get('name', None)
					email = request.POST.get('email', None)
					note = request.POST.get('note', None)
					rsvp1 = rsvp.objects.update_or_create(
           		 								  name = name,
           		 								  email = email,
             									 note = note,
             									 )
					message = 'Thank you, see you in Boston'
					##or we could send a comfirmation e-mail by built-in django function
					return render(request, 'index.html', { 'message':message })
		else:
				form = rsvpForm()
				return render(request, 'index.html', { 'form':form })
###if you send a POST request, we give you a message; else, we give you the form	
def items(request):
		item = Item.objects.all()
		return render(request, 'items.html', {'items':items})

def item_view(request,title):
		the_item = Item.objects.filter(title=title)
		#title name comes from urls
		return render(request, 'item.html', {'items':the_item})
		#get all the item that fits the criters of filter, upload form python to the bowser)