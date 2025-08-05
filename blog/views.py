from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author, Blog, Keyword, SubTopic
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction



def create_blog(request):
    if request.method == 'POST':
        try:
            print("POST data:", request.POST)
            print("FILES data:", request.FILES)

            # Author creation
            author = Author.objects.create(
                name=request.POST.get('author_name'),
                description=request.POST.get('author_description'),
                photo=request.FILES.get('author_photo')
            )

            # Blog creation
            blog = Blog.objects.create(
                title=request.POST.get('blog_title'),
                photo=request.FILES.get('blog_photo'),
                author=author,
                time_to_read=request.POST.get('time_to_read'),
                published_date=datetime.date.today(),
                detail=request.POST.get('detail')

            )

            # Keywords
            keywords = json.loads(request.POST.get('keywords', '[]'))
            for keyword in keywords:
                kw, created = Keyword.objects.get_or_create(word=keyword)
                blog.keywords.add(kw)

            # Subtopics
            subtopics = json.loads(request.POST.get('subtopics_json', '[]'))
            for subtopic in subtopics:
                SubTopic.objects.create(
                    blog=blog,
                    title=subtopic['title'],
                    description=subtopic['description']
                )

            print("Redirecting to blog_lists...")
            return redirect('blog_lists')

        except Exception as e:
            print("Error in create_blog:", e)
            raise e  # SHOW the real error

    return render(request, 'create_blog.html')

def safe_json_loads(json_str):
    """Safely parse JSON or return empty list if invalid"""
    try:
        return json.loads(json_str) if json_str and json_str.strip() else []
    except json.JSONDecodeError:
        return []
    

@transaction.atomic
def update_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    author = blog.author
    
    if request.method == 'POST':
        try:
            # Update Author
            author.name = request.POST.get('author_name', author.name)
            author.description = request.POST.get('author_description', author.description)
            if 'author_photo' in request.FILES:
                author.photo = request.FILES['author_photo']
            author.save()
            
            # Update Blog
            blog.title = request.POST.get('blog_title', blog.title)
            if 'blog_photo' in request.FILES:
                blog.photo = request.FILES['blog_photo']
            blog.time_to_read = request.POST.get('time_to_read', blog.time_to_read)
            blog.detail = request.POST.get('detail', blog.detail) 
            
            
            
            blog.save()
            
            # Update Keywords
            blog.keywords.clear()
            keywords = safe_json_loads(request.POST.get('keywords'))
            for keyword in keywords:
                if keyword.strip():
                    kw, created = Keyword.objects.get_or_create(word=keyword.strip())
                    blog.keywords.add(kw)
            
            # Handle Subtopics
            subtopics_data = safe_json_loads(request.POST.get('subtopics_json'))
            existing_subtopic_ids = []
            
            for subtopic_data in subtopics_data:
                subtopic_id = subtopic_data.get('id')
                title = subtopic_data.get('title', '').strip()
                description = subtopic_data.get('description', '').strip()
                
                if not title:
                    continue
                    
                if subtopic_id:
                    try:
                        subtopic = SubTopic.objects.get(id=subtopic_id, blog=blog)
                        subtopic.title = title
                        subtopic.description = description
                        subtopic.save()
                        existing_subtopic_ids.append(subtopic.pk)
                    except SubTopic.DoesNotExist:
                        pass
                else:
                    new_subtopic = SubTopic.objects.create(
                        blog=blog,
                        title=title,
                        description=description
                    )
                    existing_subtopic_ids.append(new_subtopic.pk)
            
            # Delete removed subtopics
            SubTopic.objects.filter(blog=blog).exclude(id__in=existing_subtopic_ids).delete()
            
            messages.success(request, 'Blog updated successfully!')
            return redirect('blog_lists')
            
        except Exception as e:
            messages.error(request, f'Error updating blog: {str(e)}')
            return redirect('update_blog', id=blog.pk)
    
    # GET request - prepare context
    keywords = [kw.word for kw in blog.keywords.all()]
    subtopics = SubTopic.objects.filter(blog=blog).order_by('id')
    
    context = {
        'blog': blog,
        'author': author,
        'keywords': json.dumps(keywords),
        'subtopics': subtopics,
       
    }
    return render(request, 'update_blog.html', context)

def blog_lists(request):
    blogs=Blog.objects.all()
    return render(request,'blog_list.html',context={'blogs':blogs})


def delete_blog(request,id):
    blog=get_object_or_404(Blog,id=id)
    blog.delete()
    return redirect('blog_lists')

def blogs(request):
    new_blogs=Blog.objects.all()[0:3]
    old_blogs=Blog.objects.all()[3:]
    context={
        'new_blogs':new_blogs,
        'old_blogs':old_blogs
    }
    return render(request,'blogs.html',context)


def read_blog(request,id):
    blog=get_object_or_404(Blog,id=id)
    blogs= Blog.objects.all().filter(
    ).exclude(id=id).distinct()[:10]
    keywords=blog.keywords.all()
    subtopics = SubTopic.objects.filter(blog=blog)
    context={
        'blog':blog,
        'keywords':keywords,
        'subtopics':subtopics,
        'blogs':blogs 
    }
    return render(request,'blog-post.html',context)