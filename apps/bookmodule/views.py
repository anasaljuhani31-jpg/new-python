from django.shortcuts import render
from django.http import HttpResponse # تأكد من وجود هذا السطر
from .models import Book

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