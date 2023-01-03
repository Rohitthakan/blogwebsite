from django.shortcuts import render, HttpResponse
from blog.models import Blog, Contact
import math
# Create your views here.
def home(request):
    return render(request, 'index.html')

def blog(request):
    no_of_posts = 3
    page = request.GET.get('page')
    if page is None:
        page=1
    else:
        page=int(page)

    blog = Blog.objects.all()
    length = len(blog)
    blog=blog[(page-1)*no_of_posts : page*no_of_posts]
    if page>1:
        prev = page-1
    else:
        prev = None
    
    if page<math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None

    context = {'blogs' : blog, 'prev' : prev, 'nxt' : nxt}
    return render(request, 'bloghome.html', context)

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    context = {'blog' : blog}
    return render(request, 'blogpost.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        ins = Contact(name=name, email=email, phone=phone, desc=desc)
        ins.save()
    return render(request, 'contact.html')

def search(request):
    search = request.GET.get('search')
    queryposts = Blog.objects.filter(title__icontains = search)
    length = len(queryposts)
    if length<1:
        queryposts = Blog.objects.filter(content__icontains = search)
    context = {'queryposts' : queryposts}
    return render(request, 'search.html', context)
