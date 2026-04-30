from django.shortcuts import render
from django.http import HttpResponse # تأكد من وجود هذا السطر
from .models import Book
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min
from .models import Book, Address, Student
def index(request):
 return render(request, "bookmodule/index.html")
def list_books(request):
 return render(request, 'bookmodule/list_books.html')
def viewbook(request, bookId):
 return render(request, 'bookmodule/one_book.html')
def aboutus(request):
 return render(request, 'bookmodule/aboutus.html')
def links_page(request):
    return render(request, 'bookmodule/links.html')
def formatting_page(request):
    return render(request, 'bookmodule/formatting.html')
def listing_page(request):
    return render(request, 'bookmodule/listing.html')
def tables_page(request):
    return render(request, 'bookmodule/tables.html')

# lab 6 for search
#def search_books(request):
   # return render(request, 'bookmodule/search.html')# دالة مساعدة ترجع قائمة بالكتب




# الخطوة 1: دالة مساعدة ترجع قائمة الكتب الافتراضية

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

# الخطوة 2: تحديث دالة البحث لمعالجة الفورم
def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        
        # الآن عملية الفلترة
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower(): contained = True
            
            if contained: newBooks.append(item)
            
        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
        
    return render(request, 'bookmodule/search.html')

# lab 7 

def simple_query(request):
    # ملاحظة برمجية: المذكرة كاتبة title_icontains بشرطة سفلية واحدة، والصحيح في جانغو شرطتين __ 
    mybooks = Book.objects.filter(title__icontains='Machine') 
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})
# lab 7 task 4 
def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='and').filter(edition__gte=2).exclude(price__lte=100)[:10]
    
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    
#lab 8

def task1(request):
    # نفلتر الكتب اللي سعرها أقل من أو يساوي 80
    mybooks = Book.objects.filter(Q(price__lte=80.0))
    return render(request, 'bookmodule/task1.html', {'books': mybooks})


def task2(request):
    # الطبعة أعلى من 3 وَ (العنوان فيه qu أو المؤلف فيه qu)
    mybooks = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='	Con') | Q(author__icontains='	Con'))
    )
    return render(request, 'bookmodule/task2.html', {'books': mybooks})

def task3(request):
    # استخدام علامة ~ للنفي (NOT)
    mybooks = Book.objects.filter(
        ~Q(edition__gt=3) & ~(Q(title__icontains='	Con') | Q(author__icontains='	Con'))
    )
    return render(request, 'bookmodule/task3.html', {'books': mybooks})

def task4(request):
    # جلب كل الكتب وترتيبها حسب العنوان (title)
    mybooks = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/task4.html', {'books': mybooks})


def task5(request):
    # استخدام دوال التجميع (Aggregation) لحساب الإحصائيات المطلوبة
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/task5.html', {'stats': stats})


def task7(request):
    # نجيب كل المدن ونحسب عدد الطلاب المرتبطين بكل مدينة
    cities_stats = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/task7.html', {'stats': cities_stats})