from django.urls import path

from .views import (MainView, VacanciesView, CategoryView,
                    CompanyView, VacancyView)


urlpatterns = [
    path('', MainView.as_view(), name="index"),
    path('vacancies/', 
        VacanciesView.as_view(), name="vacancies"),
    path('vacancies/cat/<str:category>/',
        CategoryView.as_view(), name="category"),
    path('companies/<int:id>/', 
        CompanyView.as_view(), name="company"),
    path('vacancies/<int:id>/', 
        VacancyView.as_view(), name="vacancy"),
    
]
