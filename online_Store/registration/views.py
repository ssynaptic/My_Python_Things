from django.shortcuts import (render,
                              redirect)
from registration.models import User
from time import sleep
import re

# Create your views here.
def registration(request):
    return render(request=request,
                  template_name="signup.html",
                  context={})

def registering(request):
    provided_name = request.POST["name"]
    provided_email = request.POST["email"]
    provided_password = request.POST["password"]

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, provided_email):
        # print(provided_name, provided_email, provided_password)
        output = "Welcome To Our Platform, You will be redirected to the login page"
        user = User.objects.create(name=provided_name,
                                   email=provided_email,
                                   password=provided_password)


    return render(request=request,
                   template_name="registering.html",
                   context={"params": output})
                
def to_login(request):
    sleep(10)
    return redirect("signup")