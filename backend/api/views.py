from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import login , authenticate ,logout
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import TanmirtPostForm , MessageForm ,CommentForm,ProfileForm
from .models import TanmirtPost , Message ,Comment , UserProfile
from .utils import haversine

def home(request):
    q=request.GET.get('q')
    distance_range = request.GET.get('distanceRange', 100)
    if q:
        posts=TanmirtPost.objects.filter(title__icontains=q)
    else:

        posts=TanmirtPost.objects.all()
    post_distances = []
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        long1=profile.longitude
        lati1=profile.latitude
        if request.method == 'POST':
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                profile.latitude = latitude
                profile.longitude = longitude
                profile.save()
                return redirect('home')
        
        if lati1 is not None and long1 is not None:
            for post in posts:
                if post.latitude is not None and post.longitude is not None:
                    distance = haversine(lati1, long1, post.latitude, post.longitude)
                    if distance <= float(distance_range):
                        if distance < 1:
                            distance_str = "less than 1 km"
                        else:
                            distance_str = f"{int(distance)} km"
                        post_distances.append((post, distance_str))
                else:
                    post_distances.append((post, "N/A"))
        else:
            post_distances = [(post, "N/A") for post in posts]
    else:
        post_distances = [(post, "N/A") for post in posts]
    context = {'post_distances': post_distances}
    return render(request,'home.html',context)

def TanmirtInbox(request):
    if request.user.is_authenticated:
        # Get all messages where the user is either the sender or receiver, excluding self-conversations
        messages = Message.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)) & ~Q(sender=request.user, receiver=request.user)
        ).order_by('date')

        # Dictionary to keep track of the latest message for each user pair
        user_pairs = {}
        
        for message in messages:
            # Create a sorted tuple key to handle both directions (sender <-> receiver)
            pair_key = tuple(sorted([message.sender.id, message.receiver.id]))
            
            # Only keep the latest message for each pair
            user_pairs[pair_key] = message

    else:
        user_pairs = {}

    context = {"user_pairs": user_pairs}
    return render(request, 'inbox.html', context)


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
                instance.longitude=request.POST.get('longitude')
                instance.latitude=request.POST.get('latitude')
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


def UserProfileView(request,userid):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.latitude=request.POST.get('latitud')
            instance.longitude=request.POST.get('longitud')
            instance.save()
            return redirect('profile',userid)
    else:
        form=ProfileForm(instance=profile)

    context={'form':form, 'profile':profile}
    return render(request,'profile.html',context)



