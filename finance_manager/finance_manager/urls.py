from django.urls import path
from finance import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_income/', views.add_income, name='add_income'),
    path('generate_report/', views.generate_report, name='generate_report'),
]
