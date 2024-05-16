from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import login , authenticate ,logout
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import TanmirtPostForm , MessageForm ,CommentForm
from .models import TanmirtPost , Message ,Comment , UserProfile

def home(request):
    q=request.GET.get('q')
    if q:
        posts=TanmirtPost.objects.filter(title__icontains=q)
    else:

        posts=TanmirtPost.objects.all()

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if latitude and longitude:
            profile.latitude = latitude
            profile.longitude = longitude
            profile.save()
            return redirect('home')

    context={'posts':posts}
    return render(request,'home.html',context)

def showitem(request,pk):
    item=TanmirtPost.objects.get(pk=pk)
    comments=Comment.objects.filter(post=item)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.post=item
            instance.writer=request.user
            instance.save()
            return redirect('item',pk)
    else:
        form=CommentForm()

    context={'item':item,'comments':comments, 'form':form}
    return render(request,'item.html',context)

def TanmirtMessage(request,userid):
    messages=Message.objects.all()
    receiver=User.objects.get(pk=userid)
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.sender=request.user
            instance.receiver=receiver
            instance.save()
            return redirect('message',userid=userid)
    else:
        form=MessageForm()
    
    context={'receiver':receiver , 'form':form,'messages':messages}
    return render(request,'messages.html',context)

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



