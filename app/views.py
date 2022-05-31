from django.shortcuts import render

# Connection to database
from mysql.connector import connect
from datetime import datetime
from threading import Thread
def leave_record(ip, message):
    try:
        with connect(host='104.200.31.89',user='user',password='password',database='usage_analysis') as cnx:
            query = 'INSERT INTO request_record (client_IP,datetime,description) VALUES (%s,%s,%s);'
            data = ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message
            cnx.cursor().execute(query, data)
            cnx.commit()
    except:
        print("Error connecting to database")

# Create your views here.

# Allow the page to be embedded in frameset
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt

def index(request):
    ip = request.META['REMOTE_ADDR']
    print("Client IP is " + ip)
    Thread(target=leave_record,args=(ip,'main page')).start()
    return render(request, 'index.html', context={'client_IP': ip})

def brown(request):
    ip = request.META['REMOTE_ADDR']
    print("Client IP is " + ip)
    Thread(target=leave_record,args=(ip,'brown misses cony')).start()
    return render(request, 'brown.html')