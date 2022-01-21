from django.shortcuts import render

# Create your views here.

# Allow the page to be embedded in frameset
from django.views.decorators.clickjacking import xframe_options_sameorigin
@xframe_options_sameorigin

def index(request):
    print("Client IP is " + request.META['REMOTE_ADDR'])
    return render(request, 'index.html', context={'client_IP': request.META['REMOTE_ADDR']})