from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.http import Http404,HttpResponse
from .forms import *
from .forms import MyForm
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages,auth
from captcha.helpers import captcha_image_url
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_to_phone
import random
from twilio.rest import Client
from django.urls import reverse
from django.views.decorators.cache import cache_control
# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# Create your views here.
def home_view(request):
    queryset=Scheme.objects.all()
    cap=['Scheme1','Scheme2','Scheme3','Scheme4']
    l=[]
    for i in range(0,len(queryset)):
        l.append(i)
    context={
        'schemes':queryset,
        'cap':cap,
        'length':l
    }
    print(len(queryset))
    return render(request,'home.html',context)



def reg_view(request):
    form=Photo(request.POST,request.FILES)
    username=""
    f=0
    ms=False
    if request.method=="POST":
        name=request.POST['name']
        Date_of_birth= request.POST['Date_of_birth']
        marital_status=request.POST.get('marital_status')
        Address= request.POST['Address']
        aadhar=request.POST['aadhar']
        username=request.POST['username']
        password=make_password(request.POST['password'])
        secret_question=request.POST['secret_question']
        email=request.POST['email']
        Mobile_number=request.POST['Mobile_number']
        img=request.FILES.get('img')
        otp=random.randint(1000,9999)
        form=Photo(request.POST,request.FILES)
        queryset=Accounts_list.objects.all()
        if marital_status=="on":
            ms=True
        for instance in queryset:
            if username==instance.username:
                f=1
        
                break
        if f==1:
            return HttpResponse("username already exists")   
        
        else:
            checkpassword=check_password(request.POST['password'], password)
            data=Accounts_list(name=name,Date_of_birth=Date_of_birth,marital_status=ms,Address=Address,aadhar=aadhar,username=username,password=password,
                secret_question=secret_question,email=email, Mobile_number=Mobile_number,otp=str(otp),image=img )
            data.save()
            print(checkpassword)

    if form.is_valid() :   
        pass 
    else:
        form=Photo(request.POST,request.FILES)
    context={
        'form':form
    }    
    return render(request,'reg.html',{})
#@cache_control(no_cache=True, must_revalidate=True ,no_store=True)
def login_view(request):
        queryset=Accounts_list.objects.all()
        form=MyForm(request.POST)
        un=[]
        human=False
        global uname
        uname=""
        pass1="" 
        k=0
        for instance in queryset:
            un.append(instance.username)
          
        if request.method=="POST":
            uname=request.POST['username']
            pass1=request.POST['password']
            if form.is_valid():
                human = True
                print("success")
            else:
                form=MyForm(request.POST)
                print("fail")      
        if uname in un and form.is_valid():
            k=1
            print(uname)
            obj=Accounts_list.objects.get(username=uname)
            checkpassword=check_password(pass1, obj.password)
            if obj.is_phone_verified==False:
                return redirect('verify')
            elif obj.is_phone_verified==True:
                if checkpassword:
                    #messages.error(request, "login unsuccessful" )
                        request.session["uid"]=request.POST["username"]
                        context={
                    "user":obj
                            }
                        return redirect('profile',context)
                

        # # elif k!=1:
        # #      messages.error(request, "username does not exist" )
        
        
        return render(request,'login.html',{"form":form})
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def logout_view(request):
#         auth.logout(request)  
#         return redirect('login')
def profile_view(request,my_id):
    my_id=uname
    obj=Accounts_list.objects.get(username=my_id)
    # accs=[]
    # for instance in obj.accounts:
    #     accs.append(instance)
    context={
        'obj':obj,
        'accs':obj.accounts.all(),
        'uname':obj.username
    }
    return render(request,'profile.html',context)
def withdraw_view(request,my_acc):
    withdraw = 0
    racc=my_acc
    rttype="Credit"
    gttype="Debit"
    receipt=""
    dic=""
    dt=datetime.datetime.now()
    context={}
    if request.method=="POST":
        withdraw=request.POST['withdraw']
        racc=request.POST['racc']
        receipt=request.POST.get('receipt')
        dic=str(racc)+" "+str(withdraw)+" "+str(dt)
        context={'dic':str(racc)+" "+str(withdraw)+" "+str(datetime.datetime.now()),
                 'acc':racc,
                 'amount':withdraw,
                 'time':datetime.datetime.now(),
                'name':uname,
                 
                 }
    query=Accounts.objects.get(account_no=my_acc)
    query1=Accounts.objects.get(account_no=racc)
    b=int(query.balance)
    b1=int(query1.balance)
    print(my_acc)
    if b< float(withdraw):
        return HttpResponse("Not enough balance")
    else:
        if float(withdraw)>0:
            b=b-int(withdraw)
            query.balance=b
            b1=b1+int(withdraw)
            query1.balance=b1
            query.transactions.create(transaction_type=gttype,amount=float(withdraw),Date_time=dt,oppo_acc=racc)
            query1.transactions.create(transaction_type=rttype,amount=float(withdraw),Date_time=dt,oppo_acc=my_acc)
            query.save()
            query1.save()
            
            context['account']=query
    if receipt=="Yes":
        return redirect(reverse('receipt',kwargs={'my_dic':dic}))
    return render(request,'withdraw.html',{'acc':my_acc,'account':query,'name':uname})
def receipt_view(request,my_dic):
        det=my_dic.split(" ")
        query=Accounts.objects.get(account_no=det[0])
        tquery=query.transactions.all()
        id=tquery.last().id
        print(tquery.last().id)
    # print(my_dic)
        # Create Bytestream buffer
        buf = io.BytesIO()
        # Create a canvas
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        
        c.drawString(50,750,'Payment Receipt') 
        # Create a text object
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)
        # Create blank list
        lines = [
            "Transaction id: "+str(id),
            "amount: "+str(det[1]),
            "to account no "+str(det[0]),
            "date: "+str(det[2]),
            "at "+str(det[3][:5])
        ]
        for line in lines:
                textob.textLine(line)
                        
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, filename='receipt.pdf')
def deposit_view(request):
    return render(request,'deposit.html',{})

def delete_view(request,my_acc):
    obj=Accounts.objects.get(account_no=my_acc)
    if obj.balance>0:
        return redirect(reverse('withdraw',kwargs={'my_acc':my_acc}))
    else:
        obj.delete()
    return render(request,'delete.html',{'acc':my_acc,'name':uname})
def create_account_view(request):
    duration=0
    balance=0
    account_type=""
    if request.method=="POST":
        account_type=request.POST['account_type']
        balance=request.POST['balance']
        duration=request.POST['duration']
    interest=0
    if int(duration)>5:
        interest=5
    else:
        interest=3
    creation_date=datetime.datetime.now()
    maturity=int(balance)+40
    username=uname
    #data=Accounts(account_type=account_type,balance=balance,duration=duration,creation_date=creation_date,interest=interest,maturity=maturity,username=username)
    if float(balance)>0:
        obj=Accounts_list.objects.get(username=uname)
        obj.accounts.create(account_type=account_type,balance=balance,Duration=duration,creation_date=creation_date,interest_rate=interest,Maturity_amount=maturity,username=username)
        obj.save()
    return render(request,'create_account.html',{'name':uname})
def view_account_view(request):
    pass
def update_profile_view(request):
    obj=Accounts_list.objects.get(username=uname)
    form=Photo(request.POST,request.FILES)
    context={
        'name':obj.name,
        'dob':obj.Date_of_birth,
        'ms':obj.marital_status,
        'address':obj.Address,
        'aadhar':obj.aadhar,
        'sq':obj.secret_question,
        'email':obj.email,
        'contact':obj.Mobile_number
    }  
    name=""
    Date_of_birth= ""
    marital_status=None
    marital_status1=None
    Address= ""
    aadhar=0
    secret_question=""
    email=""
    Mobile_number=0
    image=""
    if request.method=="POST":
        name=request.POST['name']
        Date_of_birth= request.POST['Date_of_birth']
        marital_status=request.POST.get('marital_status')
        marital_status1=request.POST.get('marital_status1')
        Address= request.POST['Address']
        aadhar=request.POST['aadhar']
        secret_question=request.POST['secret_question']
        email=request.POST['email']
        Mobile_number=request.POST['Mobile_number']
        image=request.FILES.get('img')
        form=Photo(request.POST,request.FILES)
    if name:
        obj.name=name
    if Date_of_birth:
        obj.Date_of_birth=Date_of_birth
    if marital_status=="on":
        obj.marital_status=True
    if marital_status1=="on":
        obj.marital_status=False      
    if Address:
        obj.Address=Address
    if aadhar:
        obj.aadhar=aadhar
    if secret_question:
        obj.secret_question=secret_question
    if email:
        obj.email=email
    if Mobile_number:
        obj.Mobile_number=Mobile_number
    if image:
        obj.image=image
    obj.save() 
    if form.is_valid() :   
        form.save()  
    else:
        form=Photo(request.POST,request.FILES)            
    return render(request,'update_profile.html',context)
def transaction_view(request,my_acc):
    query=Accounts.objects.get(account_no=my_acc)
    context={
        'tr':query.transactions.all(),
        'name':uname
    }
    return render(request,'transaction.html',context)
def verify_view(request):
    ans=""
    if request.method=="POST":
        ans=request.POST['ans']
    if ans=="yes" :
        query=Accounts_list.objects.get(username=uname)
        ootp=query.otp
        mm_no=query.Mobile_number
        account_sid = "ACe1fb1198bf26799435ffc7d6166f545c"
        auth_token = "b0df90d10ea2a6cac77f0bd8292d1aad"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
         body="Hello from spit bank and your one time password for account verification is "+str(ootp),
         from_="+15856394846",
         to="+91"+str(mm_no)
            )
        print("message sent successfully")
        return redirect('verification')   
    return render(request,'verify.html',{})
def verification_view(request):
    gotp=""

    if request.method=="POST":
        gotp=request.POST.get('otp1', False)
    query=Accounts_list.objects.get(username=uname)
    if gotp==query.otp:
        query.is_phone_verified=True
        query.save()
        return HttpResponse('Phone number is verified')    
    return render(request,'verification.html',{})
def scheme_view(request):
    return render(request,'scheme.html',{})
def fp1_view(request):
         em=""
         global f_em
         f_em=""
         queryset=Accounts_list.objects.all()
         em_list=[]
         for instance in queryset:
            em_list.append(instance.email)
         if request.method=="POST":
            em=request.POST.get('email')
         if em in em_list:
              f_em=em 
              context={
                  'em':f_em
              }
              return redirect('fp2')
         return render(request,'fp1.html',{})   
def fp2_view(request):
     my_em=f_em
     ob=Accounts_list.objects.get(email=my_em)
     context={
         'name':ob.name,
         'img':ob.image
     }
     ans=""
     if request.method=="POST":
         ans=request.POST.get('ans1')
         print(ans)
     if ans=="on" :
         return redirect('ask_sq')   
     return render(request,'fp2.html',context) 
def ask_sq_view(request) :
     my_em=f_em
     ob=Accounts_list.objects.get(email=my_em)
     sq=""
     if request.method=="POST":
         sq=request.POST.get('sq')
         if sq==ob.secret_question:
             return redirect('update-password')
     return render(request,'ask_sq.html',{})
def update_password_view(request):
     my_em=f_em
     ob=Accounts_list.objects.get(email=my_em)
     if request.method=="POST":
         password=make_password(request.POST['password'])
         ob.password=password
         ob.save()
         return redirect('login')
     return render(request,'update-password.html',{})  