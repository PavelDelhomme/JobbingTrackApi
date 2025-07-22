import requests
import json
import os
import sys
import time

class JobbingTrackApiTester:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
        self.refresh_token = None
        self.user_id = None
    
    def register(self, email, password, first_name="Test", last_name="User"):
        """
        Teste l'inscription d'un utilisateur
        """
        url = f"{self.base_url}/auth/register/"
        data = {
            "email": email,
            "password": password,
            "password2": password,
            "first_name": first_name,
            "last_name": last_name
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            result = response.json()
            self.token = result.get('access')
            self.refresh_token = result.get('refresh')
            self.user_id = result.get('user', {}).get('id')
            print(f"✅ Inscription réussie: {email}")
            return True
        else:
            print(f"❌ Erreur lors de l'inscription: {response.status_code}")
            print(response.text)
            return False
    
    def login(self, email, password):
        """
        Teste la connexion d'un utilisateur
        """
        url = f"{self.base_url}/auth/login/"
        data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get('access')
            self.refresh_token = result.get('refresh')
            print(f"✅ Connexion réussie: {email}")
            return True
        else:
            print(f"❌ Erreur lors de la connexion: {response.status_code}")
            print(response.text)
            return False
    
    def get_me(self):
        """
        Teste la récupération des informations utilisateur
        """
        url = f"{self.base_url}/auth/me/"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            self.user_id = result.get('id')
            print(f"✅ Récupération utilisateur réussie: {result.get('email')}")
            return result
        else:
            print(f"❌ Erreur lors de la récupération utilisateur: {response.status_code}")
            print(response.text)
            return None
    
    def create_company(self, name="Test Company", website="", industry=""):
        """
        Teste la création d'une entreprise
        """
        url = f"{self.base_url}/companies/"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "name": name,
            "website": website,
            "industry": industry,
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Création entreprise réussie: {name}")
            return result
        else:
            print(f"❌ Erreur lors de la création entreprise: {response.status_code}")
            print(response.text)
            return None
    
    def create_application(self, title, company_id, company_name):
        """
        Teste la création d'une candidature
        """
        url = f"{self.base_url}/applications/"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "title": title,
            "company_id": company_id,
            "company_name": company_name,
            "application_ts": int(time.time() * 1000)
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Création candidature réussie: {title}")
            return result
        else:
            print(f"❌ Erreur lors de la création candidature: {response.status_code}")
            print(response.text)
            return None
    
    def sync(self, timestamp=0):
        """
        Teste la synchronisation
        """
        url = f"{self.base_url}/sync/?updated_after={timestamp}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Synchronisation réussie")
            return result
        else:
            print(f"❌ Erreur lors de la synchronisation: {response.status_code}")
            print(response.text)
            return None
    
    def client_sync(self, data):
        """
        Teste la synchronisation client
        """
        url = f"{self.base_url}/client-sync/"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Synchronisation client réussie")
            return result
        else:
            print(f"❌ Erreur lors de la synchronisation client: {response.status_code}")
            print(response.text)
            return None
    
    def run_full_test(self):
        """
        Exécute un test complet de l'API
        """
        # 1. Inscription
        email = f"test{int(time.time())}@example.com"
        password = "Test1234!"
        self.register(email, password)
        
        # 2. Connexion
        self.login(email, password)
        
        # 3. Récupération utilisateur
        self.get_me()
        
        # 4. Création entreprise
        company = self.create_company("Google")
        
        # 5. Création candidature
        application = self.create_application(
            "Développeur Python",
            company.get('id'),
            company.get('name')
        )
        
        # 6. Synchronisation
        sync_data = self.sync()
        
        # 7. Test de synchronisation client
        client_data = {
            "companies": [
                {
                    "id": company.get('id'),
                    "name": "Google (modifié)",
                    "website": "https://google.com"
                }
            ]
        }
        client_sync = self.client_sync(client_data)
        
        print("\n🎉 Test complet terminé!")

if __name__ == "__main__":
    tester = JobbingTrackApiTester()
    tester.run_full_test()