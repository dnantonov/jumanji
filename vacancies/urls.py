from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (IndexView, VacanciesView, CategoryView,
                    CompanyView, VacancyView, SendApplicationView,
                    MyCompanyView, MyCompanyVacanciesView,
                    MyCompanyVacancyView, MyCompanyEditView,
                    SearchView, MyResumeView, MyResumeCreateView)


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    path('vacancies/cat/<str:category>/', CategoryView.as_view(), name="category"),
    path('companies/<int:company_id>/', CompanyView.as_view(), name="company"),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name="vacancy"),
    path('vacancies/<int:vacancy_id>/send/', SendApplicationView.as_view(), name="send-application"),

    path('mycompany/', login_required(MyCompanyView.as_view()), name="mycompany"),
    path('mycompany/edit/', MyCompanyEditView.as_view(), name="mycompany-edit"),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view(), name="mycompany-vacancies"),
    path('mycompany/vacancies/<int:vacancy_id>/', MyCompanyVacancyView.as_view(), name="mycompany-vacancy"),

    path('search/', SearchView.as_view(), name="search"),
    path('myresume/', MyResumeView.as_view(), name="myresume"),
    path('myresume/create', MyResumeCreateView.as_view(), name="myresume-create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
