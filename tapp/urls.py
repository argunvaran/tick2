# uygulama_adi/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_case/', views.add_case, name='add_case'),
    path('product_list/', views.product_list, name='product_list'),
    path('test/', views.test_view, name='test_view'),
    path('my-form/', views.my_view, name='my-form'),
    path('user_cases/', views.user_cases, name='user_cases'),
    path('report/', views.report_page, name='report'),
    path('intersection_report/', views.intersection_report, name='intersection_report'),
    path('inter-test/', views.intersection_report1, name='inter-test'),
    path('intersection_report2/', views.intersection_report2, name='intersection_report2'),
    path('intersection_report3/', views.intersection_report3, name='intersection_report3'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),   
    path('edit_case/<int:case_id>/', views.edit_case, name='edit_case'),
    path('all_cases/', views.all_cases, name='all_cases'),
    path('export_to_excel_cases/', views.export_to_excel_cases, name='export_to_excel_cases'),
    
]


