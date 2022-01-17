from django.shortcuts import render

# Create your views here.

def index(request):
    print("Client IP is " + request.META['REMOTE_ADDR'])
    return render(request, 'index.html', context={'client_IP': request.META['REMOTE_ADDR']})