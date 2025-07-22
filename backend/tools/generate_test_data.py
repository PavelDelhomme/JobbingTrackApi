# tools/generate_test_data.py
import os
import sys
import django
import uuid
import random
import time
from datetime import datetime, timedelta

# Configurer Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.companies.models import Company
from apps.applications.models import Application
from apps.interviews.models import Interview
from apps.calls.models import Call
from apps.followups.models import FollowUp
from apps.contacts.models import Contact
from apps.events.models import Event

User = get_user_model()

def create_test_user(email, password="Test1234!"):
    """Crée un utilisateur de test"""
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'id': str(uuid.uuid4()),
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Utilisateur créé: {email}")
    else:
        print(f"ℹ️ Utilisateur existe déjà: {email}")
    
    return user

def create_companies(user, count=5):
    """Crée des entreprises de test"""
    companies = []
    company_names = [
        "Google", "Microsoft", "Amazon", "Apple", "Facebook",
        "Netflix", "Twitter", "LinkedIn", "Airbnb", "Uber"
    ]
    
    for i in range(count):
        name = company_names[i % len(company_names)]
        if i > 0:
            name = f"{name} {i}"
            
        timestamp = int(time.time() * 1000)
        company = Company.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            name=name,
            website=f"https://{name.lower().replace(' ', '')}.com",
            industry="Technology",
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )
        companies.append(company)
        print(f"✅ Entreprise créée: {name}")
    
    return companies

def create_applications(user, companies, count=10):
    """Crée des candidatures de test"""
    applications = []
    job_titles = [
        "Développeur Python", "Développeur Full-Stack", "Data Scientist",
        "Chef de Projet", "Développeur Mobile", "DevOps Engineer",
        "UX Designer", "Product Manager", "QA Engineer", "System Administrator"
    ]
    
    for i in range(count):
        company = random.choice(companies)
        title = job_titles[i % len(job_titles)]
        
        # Date aléatoire dans les 30 derniers jours
        days_ago = random.randint(0, 30)
        application_date = datetime.now() - timedelta(days=days_ago)
        application_ts = int(application_date.timestamp() * 1000)
        
        timestamp = int(time.time() * 1000)
        application = Application.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            title=title,
            company=company,
            company_name=company.name,
            application_ts=application_ts,
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )
        applications.append(application)
        print(f"✅ Candidature créée: {title} chez {company.name}")
    
    return applications

def create_interviews(user, applications, count=5):
    """Crée des entretiens de test"""
    interviews = []
    
    for i in range(min(count, len(applications))):
        application = applications[i]
        
        # Date d'entretien aléatoire dans les 7 prochains jours
        days_future = random.randint(1, 7)
        interview_date = datetime.now() + timedelta(days=days_future)
        interview_ts = int(interview_date.timestamp() * 1000)
        
        timestamp = int(time.time() * 1000)
        interview = Interview.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            title=f"Entretien pour {application.title}",
            application_id=application.id,
            company_id=application.company.id,
            interview_ts=interview_ts,
            duration_minutes=random.choice([30, 45, 60, 90]),
            is_remote=random.choice([True, False]),
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )
        interviews.append(interview)
        print(f"✅ Entretien créé pour {application.title}")
    
    return interviews

def create_followups(user, applications, count=8):
    """Crée des relances de test"""
    followups = []
    
    for i in range(min(count, len(applications))):
        application = applications[i]
        
        # Date de relance aléatoire dans les 3 prochains jours
        days_future = random.randint(0, 3)
        followup_date = datetime.now() + timedelta(days=days_future)
        followup_ts = int(followup_date.timestamp() * 1000)
        
        timestamp = int(time.time() * 1000)
        followup = FollowUp.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            title=f"Relance pour {application.title}",
            application_id=application.id,
            company_id=application.company.id,
            followup_ts=followup_ts,
            description=f"Vérifier l'avancement de ma candidature",
            is_completed=False,
            created_at=timestamp,
            updated_at=timestamp,
            is_deleted=False,
            is_archived=False
        )
        followups.append(followup)
        print(f"✅ Relance créée pour {application.title}")
    
    return followups

def generate_test_data():
    """Génère un ensemble complet de données de test"""
    # Créer utilisateur
    user = create_test_user("test@jobbingtrack.com")
    
    # Créer entreprises
    companies = create_companies(user, 5)
    
    # Créer candidatures
    applications = create_applications(user, companies, 10)
    
    # Créer entretiens
    interviews = create_interviews(user, applications, 5)
    
    # Créer relances
    followups = create_followups(user, applications, 8)
    
    print("\n🎉 Génération des données de test terminée!")
    print(f"📊 Résumé:")
    print(f"- 1 utilisateur")
    print(f"- {len(companies)} entreprises")
    print(f"- {len(applications)} candidatures")
    print(f"- {len(interviews)} entretiens")
    print(f"- {len(followups)} relances")

if __name__ == "__main__":
    generate_test_data()