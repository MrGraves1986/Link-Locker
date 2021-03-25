from django.shortcuts import render, redirect
from django.contrib import messages 
import bcrypt
from .models import User, Link
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=="POST":
        errors=User.objects.validator(request.POST) 
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        
        new_user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/success') 
    return redirect('/') 


def success(request):
    if 'user_id' not in request.session: 
        return redirect('/')
    return render(request, "success.html")        

def login(request):
    if request.method=="POST":
        logged_user=User.objects.filter(email=request.POST['email']) 
        if logged_user: 
            logged_user=logged_user[0] 
            
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/link_page')
    return redirect('/') 


def link_page(request):
    context= {
        'all_links': Link.objects.all() 
    }
    return render(request, "links_home.html", context)  

def logout(request):
    request.session.clear()
    return redirect('/')

def create_link(request):
    if request.method=="POST":
        error=Link.objects.empty_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/link_page')
        Link.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/link_page')
    return redirect('/')

def success_page(request):
    return redirect('/link_page')

def delete_link(request, link_id):
    Link.objects.get(id=link_id).delete()
    return redirect('/link_page')

def contact(request):
    context = {
        "form": ContactForm()
    }
    return render(request, "contact.html", context)

def back(request):
    return redirect('/link_page')              

def contact_form(request):
    # if request.method=="GET":
    #     return redirect('/contact')
    # else: 
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         subject = form.cleaned_data['subject']
    #         sender = form.cleaned_data['sender']
    #         message = form.cleaned_data['message']
    #         try:
    #             send_mail(subject, message, sender,['linklocker@mail.com'])    
    #         except BadHeaderError:
    #             return HttpResponse('Invalid header found.')
    #         return redirect ('/submit_message')        
    # return render(request, "contact.html", {'form': form})

    if request.method=="POST":  
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, sender,['linklocker@mail.com'])    
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ('/submit_message')
    return redirect('/contact')

def submit_message(request):
    return render(request,'message.html')

def new_page(request, link_content):
    return redirect(request, link_content)



     