from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (MainView, VacanciesView, CategoryView,
                    CompanyView, VacancyView, SendApplicationView,
                    MyCompanyView, MyCompanyVacanciesView,
                    MyCompanyVacancyView)



urlpatterns = [
    path('', MainView.as_view(), name="index"),
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    path('vacancies/cat/<str:category>/', 
        CategoryView.as_view(), name="category"),
    path('companies/<int:id>/', 
        CompanyView.as_view(), name="company"),
    path('vacancies/<int:id>/', 
        VacancyView.as_view(), name="vacancy"),
    path('vacancies/<int:id>/send/', 
        SendApplicationView.as_view(), name="send-application"),
    path('mycompany/',
        MyCompanyView.as_view(), name="mycompany"),
    path('mycompany/vacancies/',
        MyCompanyVacanciesView.as_view(), name="mycompany-vacancies"),
    path('mycompany/vacancies/<int:id>/',
        MyCompanyVacancyView.as_view(), name="mycompany-vacancy")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
