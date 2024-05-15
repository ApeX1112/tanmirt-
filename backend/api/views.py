from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import login , authenticate ,logout
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import TanmirtPostForm
from .models import TanmirtPost

def home(request):
    posts=TanmirtPost.objects.all()
    context={'posts':posts}
    return render(request,'home.html',context)

def Post_on_Tanmirt(request):
    my_posts=TanmirtPost.objects.filter(user=request.user)
    

    if request.method=='POST':
        if request.user.is_authenticated:
            form=TanmirtPostForm(request.POST,request.FILES)

            if form.is_valid():
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                return redirect('myposts')
        else:
            return HttpResponse("you must register or login to post on tanmirt")
    else:
        form=TanmirtPostForm()

    context={'form':form}
    return render(request,"Add_post.html",context)


def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
                
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    
    if request.method == 'POST':
        
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form = MyUserCreationForm()
    return render(request,'register.html',{'form':form})


def LogoutUser(request):
    logout(request)

    return redirect('home')
