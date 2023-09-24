from django.shortcuts import render , redirect
from .models import Product ,Customer,Case,User
from .forms import CaseForm , CaseFilterForm
from .forms import ProductForm, CustomerForm
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime



def index(request):
    return render(request, 'index.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm()
    
    products = Product.objects.all()
    
    context = {
        'form': form,
        'products': products,
    }
    
    return render(request, 'add_product.html', context)    

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_customer')
    else:
        form = CustomerForm()
    
    customers = Customer.objects.all()
    
    context = {
        'form': form,
        'customer': customers,
    }
    
    return render(request, 'add_customer.html', context)    

def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            # Oturum açmış olan kullanıcının case'ini oluşturun
            new_case = form.save(commit=False)
            new_case.user = request.user  # Kullanıcıyı atayın
            new_case.save()
            return redirect('user_cases')  # Kullanıcının case'lerini görüntüleyeceği sayfaya yönlendirin
    else:
        form = CaseForm()

    context = {
        'form': form
    }
    return render(request, 'add_case.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def test_view(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            new_case = form.save(commit=False)
            new_case.user = request.user  # Kullanıcıyı atayın
            new_case.save()
            return redirect('test_view')
    else:
        form = CaseForm()

    products = Product.objects.all()
    customers = Customer.objects.all()
    
    context = {
        'form': form,
        'products': products,
        'customers': customers,
    }
    return render(request, 'test.html',context)

def my_view(request):
    
    return render(request, 'my_template.html')

def user_cases(request):
    # Kullanıcının kendi case'lerini alın
    user_cases = Case.objects.filter(user=request.user)
    
    context = {
        'user_cases': user_cases
    }

    return render(request, 'user_cases.html', context)

def report_page(request):

    caseusers = Case.objects.all()

    cases = Case.objects.all()

    casetimes = {}

    casetimest = {}

    for caseuser in caseusers:
        customer = caseuser.customer
        start_time = caseuser.start_time
        end_time = caseuser.end_time
        if start_time and end_time:  # Hem start_time hem de end_time değerleri varsa
            duration = caseuser.duration()  # duration() methodunu çağırabiliriz
            if customer in casetimes:
                casetimes[customer] += duration
            else:
                casetimes[customer] = duration

    for _case in cases:
        product = _case.product
        start_time = _case.start_time
        end_time = _case.end_time
        if start_time and end_time:  # Hem start_time hem de end_time değerleri varsa
            duration = _case.duration()  # duration() methodunu çağırabiliriz
            if product in casetimest:
                casetimest[product] += duration
            else:
                casetimest[product] = duration


    context = {
        'casetimes': casetimes,
        'casetimest': casetimest,
    }

    return render(request, 'report_page.html', context)

def intersection_report(request):
    cases = Case.objects.all()
    customer_times = {}
    product_times = {}

    for case in cases:
        customer = case.customer
        product = case.product
        duration = case.duration()

        # Süre None (Boş) ise sıfıra eşitle
        if duration is None:
            duration = 0

        if customer in customer_times:
            customer_times[customer] += duration
        else:
            customer_times[customer] = duration

        if product in product_times:
            product_times[product] += duration
        else:
            product_times[product] = duration

    context = {
        'customer_times': customer_times,
        'product_times': product_times,
    }

    return render(request, 'intersection_report.html', context)

def intersection_report1(request):
    cases = Case.objects.all()
    customer_times = {}
    product_times = {}
    user_times = {}

    for case in cases:
        customer = case.customer
        product = case.product
        user = case.user
        duration = case.duration()

        # Süre None (Boş) ise sıfıra eşitle
        if duration is None:
            duration = 0

        # Müşteri bazlı süre hesaplama
        if customer in customer_times:
            customer_times[customer] += duration
        else:
            customer_times[customer] = duration

        # Ürün bazlı süre hesaplama
        if product in product_times:
            product_times[product] += duration
        else:
            product_times[product] = duration

        # Kullanıcı bazlı süre hesaplama
        if user in user_times:
            user_times[user] += duration
        else:
            user_times[user] = duration

    context = {
        'customer_times': customer_times,
        'product_times': product_times,
        'user_times': user_times,
    }

    return render(request, 'inter-test.html', context)

def intersection_report2(request):
    users = User.objects.all()  # Tüm kullanıcıları al
    user_casetimes = {}  # Kullanıcıların harcadığı saatleri saklamak için bir sözlük oluştur

    for user in users:
        cases = Case.objects.filter(user=user)  # Kullanıcının tüm case'lerini al
        total_hours = 0  # Toplam saat sayısını sıfırla

        for case in cases:
            if case.start_time and case.end_time:
                duration = case.duration()  # Case'in süresini dakika cinsinden al
                total_hours += duration  # Toplam saati güncelle

        user_casetimes[user] = total_hours  # Kullanıcının harcadığı saatleri sözlüğe ekle

    context = {
        'user_casetimes': user_casetimes,
    }

    return render(request, 'intersection_report2.html', context)

def intersection_report3(request):
    users = User.objects.all()
    customers = Customer.objects.all()
    products = Product.objects.all()

    user_casetimes = {}
    customer_casetimes = {}
    product_casetimes = {}

    for user in users:
        user_cases = Case.objects.filter(user=user)
        total_hours = sum([case.duration() for case in user_cases if case.duration() is not None])
        user_casetimes[user] = total_hours

    for customer in customers:
        customer_cases = Case.objects.filter(customer=customer)
        total_hours = sum([case.duration() for case in customer_cases if case.duration() is not None])
        customer_casetimes[customer] = total_hours

    for product in products:
        product_cases = Case.objects.filter(product=product)
        total_hours = sum([case.duration() for case in product_cases if case.duration() is not None])
        product_casetimes[product] = total_hours

    context = {
        'user_casetimes': user_casetimes,
        'customer_casetimes': customer_casetimes,
        'product_casetimes': product_casetimes,
    }

    return render(request, 'intersection_report3.html', context)


def export_to_excel(request):
    # Rapor verilerini alın
    caseusers = Case.objects.filter(user=request.user)
    cases = Case.objects.all()
    
    casetimes = {}
    casetimest = {}

    for caseuser in caseusers:
        customer = caseuser.customer
        start_time = caseuser.start_time
        end_time = caseuser.end_time
        if start_time and end_time:
            duration = caseuser.duration()
            if customer in casetimes:
                casetimes[customer] += duration
            else:
                casetimes[customer] = duration

    for _case in cases:
        product = _case.product
        start_time = _case.start_time
        end_time = _case.end_time
        if start_time and end_time:
            duration = _case.duration()
            if product in casetimest:
                casetimest[product] += duration
            else:
                casetimest[product] = duration

    # Verileri bir DataFrame'e dönüştürün
    df_customers = pd.DataFrame(list(casetimes.items()), columns=['Müşteri', 'Toplam Harcanan Saat'])
    df_products = pd.DataFrame(list(casetimest.items()), columns=['Ürün', 'Toplam Harcanan Saat'])

    # Excel dosyasına aktarın
    with pd.ExcelWriter('rapor.xlsx', engine='xlsxwriter') as writer:
        df_customers.to_excel(writer, sheet_name='Müşteri Raporu', index=False)
        df_products.to_excel(writer, sheet_name='Ürün Raporu', index=False)

    # Excel dosyasını HttpResponse ile döndürün
    with open('rapor.xlsx', 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=rapor.xlsx'

    return response

# def edit_case(request, case_id):
#     case = Case.objects.get(id=case_id)

#     if request.method == 'POST':
#         form = CaseForm(request.POST, instance=case)
#         if form.is_valid():
#             form.save()
#             return redirect('user_cases')
#     else:
#         form = CaseForm(instance=case)

#     context = {
#         'form': form,
#         'case': case,
#     }

#     return render(request, 'edit_case.html', context)

# def all_cases(request):

#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     start_time = request.GET.get('start_time')
#     end_time = request.GET.get('end_time')

#     form = CaseFilterForm(request.GET)
    
#     if form.is_valid():
#         start_date = form.cleaned_data.get('start_date')
#         end_date = form.cleaned_data.get('end_date')
#         start_time = form.cleaned_data.get('start_time')
#         end_time = form.cleaned_data.get('end_time')
#     # Tarih aralığı
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     # Saat aralığı
#     start_time = request.GET.get('start_time')
#     end_time = request.GET.get('end_time')

#     # Tarih ve saat aralığına göre filtreleme yapın
#     if start_date and end_date:
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
#         cases = cases.filter(start_time__range=(start_date, end_date))

#     if start_time and end_time:
#         cases = cases.filter(start_time__time__range=(start_time, end_time))

#     query = request.GET.get('q')  # Arama sorgusunu alın

#     # Sorgu yoksa veya boşsa tüm case'leri getirsin
#     if not query:
#         cases = Case.objects.all()
#     else:
#         # Sorguyu title ve description üzerinde ara
#         cases = Case.objects.filter(Q(title__icontains=query) | Q(description1__icontains=query) | Q(description2__icontains=query))

#     context = {
#         'cases': cases,
#         'query': query,
#     }
    
#     return render(request, 'all_cases.html', context)

def all_cases(request):
    # Tarih aralığı
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Saat aralığı
    start_time_str = request.GET.get('start_time')
    end_time_str = request.GET.get('end_time')

    # Tarih dizgilerini datetime nesnelerine çevirin
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        start_date = None
        end_date = None

    # Saat dizgilerini datetime nesnelerine çevirin
    if start_time_str and end_time_str:
        start_time = datetime.strptime(start_time_str, '%H:%M')
        end_time = datetime.strptime(end_time_str, '%H:%M')
    else:
        start_time = None
        end_time = None

    # Tarih ve saat aralığına göre filtreleme yapın
    cases = Case.objects.all()

    if start_date and end_date:
        cases = cases.filter(start_time__date__range=(start_date, end_date))

    if start_time and end_time:
        cases = cases.filter(start_time__time__range=(start_time, end_time))

    query = request.GET.get('q')  # Arama sorgusunu alın

    # Sorgu yoksa veya boşsa tüm case'leri getirsin
    if not query:
        cases = cases.all()
    else:
        # Sorguyu title ve description üzerinde ara
        cases = cases.filter(Q(title__icontains=query) | Q(description1__icontains=query) | Q(description2__icontains=query))

    context = {
        'cases': cases,
        'query': query,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'start_time': start_time_str,
        'end_time': end_time_str,
    }
    
    return render(request, 'all_cases.html', context)

def edit_case(request, case_id):
    case = Case.objects.get(id=case_id)

    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('user_cases')
    else:
        # Mevcut tarihleri form alanlarında göstermek için başlangıç ve bitiş saatlerini formatlayın
        start_time = case.start_time.strftime('%Y-%m-%dT%H:%M')
        end_time = case.end_time.strftime('%Y-%m-%dT%H:%M')
        initial_data = {
            'start_time': start_time,
            'end_time': end_time,
        }
        form = CaseForm(instance=case, initial=initial_data)

    context = {
        'form': form,
        'case': case,
    }

    return render(request, 'edit_case.html', context)

# def export_to_excel_cases(request):
#     query = request.GET.get('q')  # Arama sorgusunu alın

#     # Sorgu yoksa veya boşsa tüm case'leri getirsin
#     if not query:
#         cases = Case.objects.all()
#     else:
#         # Sorguyu title ve description üzerinde ara
#         cases = Case.objects.filter(Q(title__icontains=query) | Q(description1__icontains=query) | Q(description2__icontains=query))

#     # Case verilerini bir veri çerçevesine yerleştirin
#     data = {
#     'Title': [case.title for case in cases],
#     'Description1': [case.description1 for case in cases],
#     'Description2': [case.description2 for case in cases],
#     'Start Time': [case.start_time.replace(tzinfo=None) if case.start_time else None for case in cases],
#     'End Time': [case.end_time.replace(tzinfo=None) if case.end_time else None for case in cases],
#     'Status': [case.status for case in cases],
#     }

#     df = pd.DataFrame(data)

#     # Veriyi bir Excel dosyasına yazın
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="cases.xlsx"'
#     df.to_excel(response, index=False)

#     return response

def export_to_excel_cases(request):
    query = request.GET.get('q')  # Arama sorgusunu alın

    # Sorgu yoksa veya boşsa tüm case'leri getirsin
    if query:
        
        cases = Case.objects.filter(Q(title__icontains=query) | Q(description1__icontains=query) | Q(description2__icontains=query))
    else:
        # Sorguyu title ve description üzerinde ara
        cases = Case.objects.all()
        

    # Veriyi bir Excel dosyasına yazın
    data = {
        'Title': [case.title for case in cases],
        'Description1': [case.description1 for case in cases],
        'Description2': [case.description2 for case in cases],
        'Start Time': [case.start_time.replace(tzinfo=None) if case.start_time else None for case in cases],
        'End Time': [case.end_time.replace(tzinfo=None) if case.end_time else None for case in cases],
        'Status': [case.status for case in cases],
    }

    df = pd.DataFrame(data)

    # Veriyi bir Excel dosyasına yazın
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="filtered_cases.xlsx"'
    df.to_excel(response, index=False)

    return response

































