from django.contrib.auth import authenticate
from django.test import TestCase
from django.contrib.auth.models import User

from vacancies.forms import ApplicationForm, CompanyForm
from vacancies.models import Specialty, Company, Vacancy, Resume


class VacanciesTestCase(TestCase):
    def setUp(self):
        # Creating test specialties
        self.test_specialty = Specialty.objects.create(code='test1', name='Test 1')
        # Creating test users
        self.test_user = User.objects.create(username='test_user_1', first_name='Test name 1',
                                             last_name='Test last name 1', password='test_pass_1')
        # Creating test companies
        self.test_company = Company.objects.create(name='Test Company 1', employee_count=10,
                                                   location='Test Location 1', owner=self.test_user)
        # Creating test vacancies
        self.test_vacancy = Vacancy.objects.create(title='Test Vacancy 1', specialty=self.test_specialty,
                                                   company=self.test_company)

    def test_index_route(self):
        # Test index route
        url = '/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_vacancies_route(self):
        # Test all vacancies route
        url = '/vacancies/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_category_route(self):
        # Test created category route
        url_category = f'/vacancies/cat/{self.test_specialty.code}/'
        response_category = self.client.get(url_category)
        self.assertEqual(200, response_category.status_code)

    def test_company_route(self):
        # Test created company route
        url_company = f'/companies/{self.test_company.id}/'
        response_company = self.client.get(url_company)
        self.assertEqual(200, response_company.status_code)

    def test_vacancy_route(self):
        # Test created vacancy route
        url_vacancy = f'/companies/{self.test_vacancy.id}/'
        response_vacancy = self.client.get(url_vacancy)
        self.assertEqual(200, response_vacancy.status_code)

    def test_send_application_form(self):
        # Test send application form
        form_data = dict(written_username='Test name', written_phone='+79992117746',
                         vacancy=self.test_vacancy, user=self.test_user)
        form = ApplicationForm(data=form_data)
        self.assertTrue(form.is_valid())


class MyCompanyTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user_1')
        self.test_user.set_password('test_pass_1')
        self.test_user.save()
        self.company = Company.objects.create(name='Test Company', employee_count=10,
                                              location='Test Location', owner=self.test_user)
        self.specialty = Specialty.objects.create(code='test1', name='Test 1')
        self.vacancy = Vacancy.objects.create(title='Test vacancy', specialty=self.specialty,
                                              company=self.company)

    def test_my_company_not_authenticated(self):
        # Test my company page route without authorization.
        url_my_company = '/mycompany/'
        response_my_company = self.client.get(url_my_company)
        self.assertEqual(302, response_my_company.status_code)

    def test_my_company_create(self):
        # Test my company creation.
        url_my_company = '/mycompany/'
        logged_in = self.client.login(username='test_user_1', password='test_pass_1')
        response_my_company = self.client.get(url_my_company)
        self.assertIn(bytes('Информация о&nbsp;компании', 'utf-8'), response_my_company.content)

    def test_my_company_vacancies(self):
        # Test my company vacancies route.
        url_my_vacancies = '/mycompany/vacancies/'
        logged_in = self.client.login(username='test_user_1', password='test_pass_1')
        response_my_vacancies = self.client.get(url_my_vacancies)
        self.assertEqual(200, response_my_vacancies.status_code)
        self.assertIn(bytes('Добавить вакансию', 'utf-8'), response_my_vacancies.content)

    def test_my_company_vacancy(self):
        # Test my company vacancy create route.
        url_my_vacancy = f'/mycompany/vacancies/{self.vacancy.id}/'
        logged_in = self.client.login(username='test_user_1', password='test_pass_1')
        response_my_vacancy = self.client.get(url_my_vacancy)
        self.assertEqual(200, response_my_vacancy.status_code)
        self.assertIn(bytes('Название вакансии', 'utf-8'), response_my_vacancy.content)


class SearchTestCase(TestCase):
    def setUp(self):
        self.query = 'Test'
        self.test_user = User.objects.create(username='test_user_1', first_name='Test name 1',
                                             last_name='Test last name 1', password='test_pass_1')
        self.company = Company.objects.create(name='Test Company 2', employee_count=10,
                                              location='Test Location', owner=self.test_user)
        self.specialty = Specialty.objects.create(code='test1', name='Test 1')
        self.vacancy = Vacancy.objects.create(title='Test vacancy', specialty=self.specialty,
                                              company=self.company)

    def test_vacancy_search(self):
        url = f'/search/?q={self.query}/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertIn(bytes('Поиск вакансий', 'utf-8'), response.content)
        self.assertIn(bytes('Test', 'utf-8'), response.content)


class MyResumeTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user_1')
        self.test_user.set_password('test_pass_1')
        self.test_user.save()
        self.specialty = Specialty.objects.create(code='test1', name='Test 1')
        self.test_resume = Resume.objects.create(user=self.test_user, specialty=self.specialty,
                                                 name='Test Name', surname='Test Surname')

    def test_my_resume(self):
        url = '/myresume/'
        logged_in = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertIn(bytes('Мое резюме', 'utf-8'), response.content)
