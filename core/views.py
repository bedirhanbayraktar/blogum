from django.shortcuts import render
from .models import Post, Blog, Category
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogForm
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User



def post_list(request):
    posts = Post.objects.order_by('-created_date')
    return render(request, 'post_list.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Kayıt olan kullanıcıyı oturum açık hale getirin
            print('user', user)
            print('request',request)
            return redirect('index')  # Kayıt işlemi tamamlandığında ana sayfaya yönlendirin
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('kullanıcıadı', username)
        print('şifre',password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Giriş yapan kullanıcıyı oturum açık hale getirin
            print('kullanıcı girdi')
            return redirect('index')  # Giriş işlemi tamamlandığında ana sayfaya yönlendirin
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    categories = Category.objects.annotate(blog_count=Count('blog')).all()  # Kategoriye ait blog sayıları ile birlikte tüm kategorileri alın
    blogs = Blog.objects.all().order_by('-publication_date')  # Tüm blogları alın
    users = User.objects.all()
    print('users',users)

    for category in categories:
        # Her kategori için o kategoriye ait blogları alın
        category.blogs = Blog.objects.filter(categories=category)

    return render(request, 'index.html', {'blogs': blogs, "categories": categories, "users": users})


def create_blog(request):
    categories_dict = {}  # Kategorileri saklamak için boş bir sözlük oluşturun

    if request.method == 'POST':
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        image_file1 = request.FILES['image_file1']
        image_file2 = request.FILES.get('image_file2')  # İkinci resim (zorunlu değil)
        category_ids = request.POST.getlist('categories')  # Birden çok kategori alabiliriz
        print('kategori', category_ids)

        categories = Category.objects.filter(id__in=category_ids)

        blog = Blog.objects.create(
            title=title,
            comment=comment,
            image_file1=image_file1,
            image_file2=image_file2,  # İkinci resim (zorunlu değil)
            author=request.user  # Oturum açmış kullanıcının kimliğini atayın
        )

        # Kategorileri blog nesnesine ekleyin
        blog.categories.set(categories)

        return redirect('index')

    categories = Category.objects.all()
    return render(request, 'create_blog.html', {'categories': categories})





def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    categories = Category.objects.annotate(blog_count=Count('blog')).all() 

    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('index')  # Düzenleme tamamlandığında ana sayfaya yönlendirin

    else:
        form = BlogForm(instance=blog)  # Düzenleme formunu oluşturun ve mevcut blog verileriyle doldurun


    return render(request, 'edit_blog.html', {'form': form, 'categories': categories, 'blog': blog})


def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        blog.delete()
        return JsonResponse({'message': 'Blog başarıyla silindi.'})

    return render(request, 'delete_blog.html', {'blog': blog})


@csrf_exempt  # CSRF korumasını devre dışı bırakmak için bu dekoratörü kullanın
def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()
        if category_name:
            category = Category.objects.create(name=category_name)
            print(category)
            return JsonResponse({'success': True, 'category_id': category.id})
        else:
            return JsonResponse({'success': False, 'message': 'Kategori adı boş olamaz.'})

    categories = Category.objects.all()
    return render(request, 'create_blog.html', {'categories': categories})


def blog_details(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    categories = Category.objects.annotate(blog_count=Count('blog')).all()  # Kategoriye ait blog sayıları ile birlikte tüm kategorileri alın
    blogs = Blog.objects.all()

    return render(request, 'blog_details.html', {'blog': blog, "categories": categories, "blogs": blogs})
