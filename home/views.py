from django.shortcuts import render
from operator import attrgetter
from blog.models import BlogPost ,comment

def home_screen_view(request):

    context ={}

    blog_posts = sorted(BlogPost.objects.all().order_by('-id')[:4], key=attrgetter('date_updated'), reverse=True)

    context['blog_posts'] = blog_posts


       
    return render(request, "home/home.html", context)


def fakepage_view(request):

    return render(request, "home/fakepage.html",{})

def Robotbehaviour_view(request):

    return render(request, "home/Robot.html",{})

def commentnumber_view(request):

    return render(request, "home/commentsnumber.html",{})