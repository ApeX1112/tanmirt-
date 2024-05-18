from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login , authenticate ,logout
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.html import format_html

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
    if q:
        search_query=q
    else:
        search_query=''
    context = {'post_distances': post_distances , 'search_query':search_query}
    return render(request,'home.html',context)

def Tanmirtnotifications(request):
    if request.user.is_authenticated:
        user_posts=TanmirtPost.objects.filter(user=request.user)

        latest_comments=Comment.objects.filter(post__in=user_posts).order_by('-date')

        notifications = []
    for comment in latest_comments:
        time_ago = timesince(comment.date, now())
        post_link = format_html("<a href='/item/{0}'>{1}</a>", comment.post.id, comment.post.title)
        notification = format_html(
            "<div class='notification'>"
            "<h1>{0}</h1>"
            "<p>commented on your post {1}</p>"
            "<p>{2} ago</p>"
            "</div>",
            comment.writer.username,
            post_link,
            time_ago
        )
        notifications.append(notification)

    
    context = {
        'notifications': notifications
    }
    return render(request,'Notifications.html',context)

def TanmirtInbox(request):
    if request.user.is_authenticated:
        
        messages = Message.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)) & ~Q(sender=request.user, receiver=request.user)
        ).order_by('date')

        
        user_pairs = {}
        
        for message in messages:
            
            pair_key = tuple(sorted([message.sender.id, message.receiver.id]))
            
            
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

def PostDelete(request,pk):
    post = get_object_or_404(TanmirtPost, pk=pk)
    post.delete()

    return redirect('home')

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



