from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
import requests
from django.views.decorators.cache import never_cache
from myfirepro.firebase_config import db
from django.contrib.auth import logout

def Register(request):
    if request.method=="POST":
        n = request.POST.get("name")
        e = request.POST.get("email")
        p = request.POST.get("password")
        pn = request.POST.get("phone_number")
        g = request.POST.get("gender")
        a = request.POST.get("address")

        if not n or not e or not p or not pn or not g or not a:
            messages.error("All Fields Required")
            return redirect("reg")
        if len(p) < 8:
            messages.error(request, "Password Must Be 8 Characters Long")
            return redirect("reg")

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={settings.FIRE}"
        payload = {

            "email": e,
            "password": p,
            "returnSecureToken":True
        }
        response = requests.post(url,payload)

        if response.status_code == 200:
            errorMsg = response.json()
        db.collection("registration").add({
            "Name" : n,
            "Email" : e,
            "Password" : p,
            "Phone" : pn,
            "Gender" : g,
            "Address" : a
        })
        messages.success(request, "User Has Been Register")
        return redirect("reg")

    return render(request,"myapp/userregistration.html")

def login(req):
    if req.method == "POST":
        e = req.POST.get("email")
        p = req.POST.get("password")

        if not e or not p:
            messages.error(req,"All Fields Are Required")
            return redirect("log")

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIRE}"
        payload = {
            "email":e,
            "password":p,
            "returnSecureToken":True
        }
        response = requests.post(url,json=payload)

        if response.status_code == 200:
            userinfo = response.json()
            req.session["email"] = userinfo.get("email")
            return redirect("index")
        else:
            error = response.json().get("error",{}).\
                get("message","Message Not Found")
            print(error)
        if error == "INVALID_LOGIN_CREDENTIALS":
            messages.error(req,"Invalid Credentials, Login Again")
        elif error == "INVALID_PASSWORD":
            messages.error(req,"Password is Correct")
            return redirect("log")
    return render(req,"myapp/login.html")

@never_cache
def Index(request):
    email = request.session.get("email")
    if not email:
        return redirect("login")
    return render(request,"myapp/Index.html",{"email": email})


def Service(request):
    return render(request,"myapp/Service.html")

def Service_details(request):
    return render(request,"myapp/service-details.html")

def Blog(request):
    return render(request,"myapp/Blog.html")

def Blog_details(request):
    return render(request,"myapp/blog-details.html")

def Contact(request):
    if request.method == "POST":
        n = request.POST.get("name")
        e = request.POST.get("email")
        s = request.POST.get("subject")
        m = request.POST.get("message")


        contact_data = {
            "name": n,
            "email": e,
            "subject": s,
            "message": m
        }
        db.collection("contacts").add(contact_data)

        messages.success(request, "Your Message Has Been Sent Successfully!")
        return redirect("con")

    return render(request, "myapp/Contact.html")

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login')
