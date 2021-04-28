from vacancies.data import specialties, companies, jobs
from vacancies.models import Specialty, Company, Vacancy


for s in specialties:
    Specialty.objects.create(code=s["code"], name=s["title"])

for c in companies:
    Company.objects.create(id=c["id"], name=c["title"], logo=c["logo"], employee_count=c["employee_count"], 
                           location=c["location"], description=c["description"])


for j in jobs:
    Vacancy.objects.create(id=j["id"], title=j["title"], specialty=Specialty.objects.get(code=j["specialty"]), 
                           company=Company.objects.get(id=j["company"]), salary_from=j["salary_from"], salary_to=j["salary_to"], 
                           published_at=j["posted"], skills=j["skills"], description=j["description"])