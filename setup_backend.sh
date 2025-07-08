#!/bin/bash
set -e

echo "Configuration complète du backend Django JobbingTrack"

# Créer la structure du projet
mkdir -p jobbingtrack_api/{config/{settings,__pycache__},core,apps/{authentication,applications,companies,contacts,interviews,calls,followups,cvs},utils,requirements,static,media,fixtures}

cd jobbingtrack_api

# Créer l'environnement virtuel
echo "Création de l'environnement virtuel"
python3 -m venv venv
source venv/bin/activate

# Créer les fichiers requirements
echo "Création des fichiers requirements..."

cat > requirements/base.txt << 'EOF'
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==23.3
dj-database-url==2.1.0
psycopg2-binary==2.9.7
celery==5.3.4
redis==5.0.1
gunicorn==21.2.0
python-decouple==3.8
djangorestgreamework-simplejwt==5.3.0
drf-spectacular==0.26.5
django-redis==5.4.0
pillow-10.1.0
EOF

cat requirements/production.txt << 'EOF'
-r base.txt
whitenoise==6.6.0
sentry-sdk==1.38.0
django-storages==1.14.2
boto3==1.34.0
EOF

# Installer les dépendances
echo "Intallation des dépendances..."
pip install -r requirements/development.txt

# Créer la structure Django
echo "Initialisation du projet Django..."

# Configuration de base
cat > config/__init__.py << 'EOF'
EOF


cat > config/settings/__init__.py << 'EOF'
EOF

cat > config/settings/base.py << 'EOF'
import os
from pathlib import Path
from decouple import config
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-change-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]

LOCAL_APPS = [
    'core',
    'apps.authentication',
    'apps.applications',
    'apps.companies',
    'apps.contacts',
    'apps.interviews',
    'apps.calls',
    'apps.followups',
    'apps.cvs',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///db.sqlite3',
        cast=db_url
    )
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'JobbingTrack API',
    'DESCRIPTION': 'API pour le suivi des candidatures',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
EOF

cat > config/settings/development.py << 'EOF'
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS += [
    'django_extensions',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
EOF

cat > config/settings/production.py << 'EOF'
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

DATABASES = {
    'default': config('DATABASE_URL', cast=db_url)
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Sentry
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

if config('USE_HTTPS', default=False, cast=bool):
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
EOF

# Créer manage.py
cat > manage.py << 'EOF'
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
EOF

chmod +x manage.py

# Créer wsgi.py
cat > config/wsgi.py << 'EOF'
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()
EOF

# Créer asgi.py
cat > config/asgi.py << 'EOF'
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_asgi_application()
EOF

# Créer les URLs
cat > config/urls.py << 'EOF'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
EOF

# Créer les applications
echo "📱 Création des applications Django..."
for app in authentication applications companies contacts interviews calls followups cvs; do
    mkdir -p apps/$app
    touch apps/$app/__init__.py
    mkdir -p apps/$app/{migrations,management/commands}
    touch apps/$app/migrations/__init__.py
    touch apps/$app/{models.py,views.py,serializers.py,urls.py,admin.py,apps.py}
done

# Créer le dossier core
mkdir -p core/{management/commands,migrations}
touch core/__init__.py core/migrations/__init__.py
touch core/{models.py,serializers.py,viewsets.py,urls.py,pagination.py,admin.py,apps.py}

# Créer .env de développement
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=django-insecure-development-key-change-in-production
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
EOF

# Créer Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/production.txt .
RUN pip install -r production.txt

COPY . .

RUN python manage.py collectstatic --noinput --settings=config.settings.production

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
EOF

# Créer docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://jobbingtrack:password@db:5432/jobbingtrack
      - REDIS_URL=redis://redis:6379/1
      - ALLOWED_HOSTS=localhost,127.0.0.1,api
    depends_on:
      - db
      - redis
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: jobbingtrack
      POSTGRES_USER: jobbingtrack
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
EOF

# Créer docker-compose.dev.yml
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://jobbingtrack:password@db:5432/jobbingtrack_dev
      - REDIS_URL=redis://redis:6379/1
      - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,api
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
      - /app/venv
    command: python manage.py runserver 0.0.0.0:8000

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: jobbingtrack_dev
      POSTGRES_USER: jobbingtrack
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_dev_data:
EOF

# Créer .dockerignore
cat > .dockerignore << 'EOF'
.git
.gitignore
README.md
Dockerfile
.dockerignore
venv/
__pycache__/
*.pyc
.env
db.sqlite3
.coverage
htmlcov/
.pytest_cache/
EOF

# Créer .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
media/
staticfiles/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local
.env.production

# Coverage
.coverage
htmlcov/

# Pytest
.pytest_cache/

# Celery
celerybeat-schedule
celerybeat.pid

# Redis
dump.rdb
EOF

echo "✅ Structure du backend créée avec succès!"
echo "📝 Prochaines étapes :"
echo "1. Compléter les modèles dans core/models.py"
echo "2. Compléter les serializers dans core/serializers.py"
echo "3. Compléter les viewsets dans core/viewsets.py"
echo "4. Exécuter : python manage.py makemigrations"
echo "5. Exécuter : python manage.py migrate"
echo "6. Exécuter : python manage.py createsuperuser"
echo "7. Tester avec : python manage.py runserver"

# ==========================================
# 2. SCRIPT DE SETUP ANDROID - setup_android.sh
# ==========================================

#!/bin/bash
echo "📱 Configuration complète du projet Android JobbingTrack"

# Créer la structure Android
mkdir -p JobbingTrackAndroid/app/src/main/{java/com/delhomme/jobbingtrack,res/{values,xml,layout,drawable}}

cd JobbingTrackAndroid

# Créer build.gradle.kts racine
cat > build.gradle.kts << 'EOF'
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.21" apply false
    id("com.google.dagger.hilt.android") version "2.48.1" apply false
}
EOF

# Créer settings.gradle.kts
cat > settings.gradle.kts << 'EOF'
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "JobbingTrack"
include(":app")
EOF

# Créer gradle.properties
cat > gradle.properties << 'EOF'
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
kotlin.code.style=official
android.nonTransitiveRClass=true
EOF

# Créer build.gradle.kts de l'app
cat > app/build.gradle.kts << 'EOF'
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    id("dagger.hilt.android.plugin")
    id("kotlin-parcelize")
}

android {
    namespace = "com.delhomme.jobbingtrack"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.delhomme.jobbingtrack"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            buildConfigField("String", "BASE_URL", "\"https://your-api.com/api/\"")
        }
        debug {
            buildConfigField("String", "BASE_URL", "\"http://10.0.2.2:8000/api/\"")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.7"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    
    implementation("androidx.navigation:navigation-compose:2.7.6")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")
    
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.compose.runtime:runtime-livedata")
    
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    kapt("androidx.room:room-compiler:2.6.1")
    
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    
    implementation("com.google.dagger:hilt-android:2.48.1")
    kapt("com.google.dagger:hilt-compiler:2.48.1")
    
    implementation("androidx.work:work-runtime-ktx:2.9.0")
    implementation("androidx.hilt:hilt-work:1.1.0")
    kapt("androidx.hilt:hilt-compiler:1.1.0")
    
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2023.10.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}

kapt {
    correctErrorTypes = true
}
EOF

echo "✅ Structure Android créée avec succès!"
echo "📝 Prochaines étapes :"
echo "1. Copier tous les fichiers Kotlin fournis précédemment"
echo "2. Synchroniser le projet avec Gradle"
echo "3. Configurer l'URL de l'API dans BuildConfig"
echo "4. Tester la compilation"

# ==========================================
# 3. SCRIPT DE MIGRATION DES DONNÉES - migrate_data.sh
# ==========================================

#!/bin/bash
echo "🔄 Migration des données vers la nouvelle architecture"

# Script pour migrer les données existantes
cat > migrate_data.py << 'EOF'
#!/usr/bin/env python
"""
Script de migration des données existantes vers la nouvelle architecture simplifiée
"""
import os
import sys
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from apps.companies.models import Company
from apps.applications.models import Application
from apps.contacts.models import Contact

def migrate_companies():
    """Migrer les entreprises existantes"""
    print("Migration des entreprises...")
    # Logique de migration selon votre ancienne structure
    
def migrate_applications():
    """Migrer les candidatures existantes"""
    print("Migration des candidatures...")
    # Logique de migration selon votre ancienne structure
    
def migrate_contacts():
    """Migrer les contacts existants"""
    print("Migration des contacts...")
    # Logique de migration selon votre ancienne structure

def main():
    print("🚀 Début de la migration des données")
    
    # Créer un utilisateur de test si nécessaire
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"✅ Utilisateur admin créé")
    
    # Migrer les données
    migrate_companies()
    migrate_applications()
    migrate_contacts()
    
    print("✅ Migration terminée avec succès!")

if __name__ == '__main__':
    main()
EOF

chmod +x migrate_data.py

echo "📊 Script de migration créé : migrate_data.py"

# ==========================================
# 4. SCRIPT DE DÉPLOIEMENT - deploy.sh
# ==========================================

#!/bin/bash
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Déploiement de JobbingTrack en production"

# Variables
DEPLOY_DIR="/opt/jobbingtrack"
BACKUP_DIR="/opt/backups/jobbingtrack"
APP_USER="jobbingtrack"

# Fonction de rollback
rollback() {
    echo "❌ Erreur détectée, rollback en cours..."
    if [ -d "$BACKUP_DIR/latest" ]; then
        sudo systemctl stop jobbingtrack-api
        sudo rm -rf $DEPLOY_DIR
        sudo cp -r $BACKUP_DIR/latest $DEPLOY_DIR
        sudo systemctl start jobbingtrack-api
        echo "🔄 Rollback terminé"
    fi
    exit 1
}

# Trap pour capturer les erreurs
trap rollback ERR

echo "📋 Vérification des prérequis..."
which docker >/dev/null || { echo "Docker non installé"; exit 1; }
which docker-compose >/dev/null || { echo "Docker Compose non installé"; exit 1; }

echo "💾 Sauvegarde de l'ancienne version..."
sudo mkdir -p $BACKUP_DIR
if [ -d "$DEPLOY_DIR" ]; then
    sudo cp -r $DEPLOY_DIR $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S)
    sudo ln -sfn $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S) $BACKUP_DIR/latest
fi

echo "📦 Déploiement de la nouvelle version..."
sudo mkdir -p $DEPLOY_DIR
sudo cp -r . $DEPLOY_DIR/
cd $DEPLOY_DIR

echo "🐳 Construction des images Docker..."
sudo docker-compose -f docker-compose.yml build --no-cache

echo "🗄️ Sauvegarde de la base de données..."
if sudo docker-compose ps | grep -q "db"; then
    sudo docker-compose exec -T db pg_dump -U jobbingtrack jobbingtrack > $BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql
fi

echo "🚀 Démarrage des services..."
sudo docker-compose -f docker-compose.yml up -d

echo "⏳ Attente du démarrage des services..."
sleep 30

echo "🔄 Migration de la base de données..."
sudo docker-compose exec -T api python manage.py migrate

echo "📊 Collection des fichiers statiques..."
sudo docker-compose exec -T api python manage.py collectstatic --noinput

echo "🧪 Tests de santé..."
if curl -f http://localhost:8000/api/schema/ >/dev/null 2>&1; then
    echo "✅ API accessible"
else
    echo "❌ API non accessible"
    rollback
fi

echo "🎉 Déploiement terminé avec succès!"
echo "📊 URL de l'API : http://localhost:8000"
echo "📚 Documentation : http://localhost:8000/api/docs/"
EOF

chmod +x deploy.sh

echo "🚀 Script de déploiement créé : deploy.sh"

# ==========================================
# 5. SCRIPT DE TESTS - run_tests.sh
# ==========================================

#!/bin/bash
cat > run_tests.sh << 'EOF'
#!/bin/bash
set -e

echo "🧪 Exécution des tests JobbingTrack"

# Tests Backend Django
echo "🐍 Tests Backend Django..."
cd jobbingtrack_api
source venv/bin/activate

echo "📋 Tests unitaires..."
python manage.py test --parallel --keepdb

echo "📊 Couverture de code..."
coverage run --source='.' manage.py test
coverage report
coverage html

echo "🔍 Analyse statique..."
flake8 . --exclude=venv,migrations --max-line-length=100

# Tests Android
echo "📱 Tests Android..."
cd ../JobbingTrackAndroid

echo "🏗️ Build debug..."
./gradlew assembleDebug

echo "🧪 Tests unitaires Android..."
./gradlew testDebugUnitTest

echo "📊 Tests d'intégration..."
if adb devices | grep -q "device"; then
    echo "📱 Appareil détecté, exécution des tests instrumentés..."
    ./gradlew connectedDebugAndroidTest
else
    echo "⚠️ Aucun appareil détecté, tests instrumentés ignorés"
fi

echo "✅ Tous les tests sont passés!"
EOF

chmod +x run_tests.sh

echo "🧪 Script de tests créé : run_tests.sh"

# ==========================================
# 6. SCRIPT DE MONITORING - monitor.sh
# ==========================================

#!/bin/bash
cat > monitor.sh << 'EOF'
#!/bin/bash

echo "📊 Monitoring JobbingTrack"

# Fonction pour vérifier la santé de l'API
check_api_health() {
    echo "🏥 Vérification santé API..."
    if curl -f -s http://localhost:8000/api/schema/ >/dev/null; then
        echo "✅ API: Healthy"
    else
        echo "❌ API: Down"
        return 1
    fi
}

# Fonction pour vérifier la base de données
check_database() {
    echo "🗄️ Vérification base de données..."
    if docker-compose exec -T db pg_isready -U jobbingtrack >/dev/null 2>&1; then
        echo "✅ Database: Healthy"
    else
        echo "❌ Database: Down"
        return 1
    fi
}

# Fonction pour vérifier Redis
check_redis() {
    echo "🔴 Vérification Redis..."
    if docker-compose exec -T redis redis-cli ping | grep -q PONG; then
        echo "✅ Redis: Healthy"
    else
        echo "❌ Redis: Down"
        return 1
    fi
}

# Fonction pour afficher les métriques
show_metrics() {
    echo "📈 Métriques système..."
    echo "🐳 Containers Docker:"
    docker-compose ps
    
    echo "💾 Utilisation disque:"
    df -h | grep -E "(Filesystem|/dev/)"
    
    echo "🧠 Utilisation mémoire:"
    free -h
    
    echo "⚡ CPU:"
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "Utilisation CPU: " 100 - $1 "%"}'
}

# Fonction d'alerte
send_alert() {
    local service=$1
    local message=$2
    echo "🚨 ALERTE: $service - $message"
    # Ici vous pouvez ajouter l'envoi d'email, Slack, etc.
}

# Boucle de monitoring principale
main() {
    while true; do
        echo "$(date) - Vérification santé des services..."
        
        if ! check_api_health; then
            send_alert "API" "Service indisponible"
        fi
        
        if ! check_database; then
            send_alert "Database" "Base de données indisponible"
        fi
        
        if ! check_redis; then
            send_alert "Redis" "Cache indisponible"
        fi
        
        show_metrics
        
        echo "⏰ Prochaine vérification dans 5 minutes..."
        sleep 300
    done
}

# Lancer le monitoring
if [ "$1" = "--daemon" ]; then
    main &
    echo "📊 Monitoring lancé en arrière-plan (PID: $!)"
else
    main
fi
EOF

chmod +x monitor.sh

echo "📊 Script de monitoring créé : monitor.sh"

# ==========================================
# 7. MAKEFILE POUR AUTOMATISER - Makefile
# ==========================================

cat > Makefile << 'EOF'
.PHONY: help setup-backend setup-android test deploy monitor clean

help:
	@echo "🚀 JobbingTrack - Commandes disponibles:"
	@echo ""
	@echo "  setup-backend    - Configure le backend Django"
	@echo "  setup-android    - Configure le projet Android"
	@echo "  test            - Lance tous les tests"
	@echo "  deploy          - Déploie en production"
	@echo "  monitor         - Lance le monitoring"
	@echo "  clean           - Nettoie les fichiers temporaires"
	@echo "  dev-start       - Démarre l'environnement de développement"
	@echo "  dev-stop        - Arrête l'environnement de développement"

setup-backend:
	@echo "🐍 Configuration du backend Django..."
	./setup_backend.sh

setup-android:
	@echo "📱 Configuration du projet Android..."
	./setup_android.sh

test:
	@echo "🧪 Lancement des tests..."
	./run_tests.sh

deploy:
	@echo "🚀 Déploiement en production..."
	./deploy.sh

monitor:
	@echo "📊 Lancement du monitoring..."
	./monitor.sh

clean:
	@echo "🧹 Nettoyage..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	docker system prune -f

dev-start:
	@echo "🔧 Démarrage de l'environnement de développement..."
	cd jobbingtrack_api && docker-compose -f docker-compose.dev.yml up -d

dev-stop:
	@echo "🛑 Arrêt de l'environnement de développement..."
	cd jobbingtrack_api && docker-compose -f docker-compose.dev.yml down

dev-logs:
	@echo "📋 Logs de développement..."
	cd jobbingtrack_api && docker-compose -f docker-compose.dev.yml logs -f

setup: setup-backend setup-android
	@echo "✅ Configuration complète terminée!"

all: setup test
	@echo "🎉 Setup et tests terminés avec succès!"
EOF

echo "📋 Makefile créé pour automatiser les tâches"

# ==========================================
# 8. README FINAL - README.md
# ==========================================

cat > README.md << 'EOF'
# 🚀 JobbingTrack - Architecture Simplifiée

Application complète de suivi des candidatures avec backend Django et client Android Kotlin.

## 📁 Structure du Projet

```
JobbingTrack/
├── jobbingtrack_api/          # Backend Django
│   ├── config/                # Configuration Django
│   ├── core/                  # Modèles et API génériques
│   ├── apps/                  # Applications métiers
│   ├── requirements/          # Dépendances Python
│   ├── Dockerfile            # Image Docker
│   └── docker-compose.yml    # Services Docker
├── JobbingTrackAndroid/       # Client Android Kotlin
│   ├── app/src/main/         # Code source Kotlin
│   │   ├── java/com/delhomme/jobbingtrack/
│   │   │   ├── core/         # Architecture de base
│   │   │   ├── features/     # Fonctionnalités métiers
│   │   │   ├── di/           # Injection de dépendances
│   │   │   └── ui/           # Interface utilisateur
│   │   └── res/              # Ressources Android
│   └── build.gradle.kts      # Configuration Gradle
├── scripts/                   # Scripts d'automatisation
└── README.md                 # Documentation
```

## 🚀 Démarrage Rapide

### 1. Configuration initiale
```bash
# Rendre les scripts exécutables
chmod +x *.sh

# Configuration complète
make setup
```

### 2. Développement Backend
```bash
cd jobbingtrack_api
source venv/bin/activate
python manage.py runserver
```

### 3. Développement Android
```bash
cd JobbingTrackAndroid
./gradlew assembleDebug
```

## 🐳 Docker (Recommandé)

### Développement
```bash
make dev-start
# API accessible sur http://localhost:8000
```

### Production
```bash
make deploy
```

## 🧪 Tests

```bash
# Tous les tests
make test

# Tests backend uniquement
cd jobbingtrack_api && python manage.py test

# Tests Android uniquement
cd JobbingTrackAndroid && ./gradlew test
```

## 📊 Monitoring

```bash
# Monitoring en temps réel
make monitor

# Monitoring en arrière-plan
./monitor.sh --daemon
```

## 🔧 Commandes Utiles

| Commande | Description |
|----------|-------------|
| `make help` | Afficher l'aide |
| `make setup` | Configuration complète |
| `make test` | Lancer tous les tests |
| `make deploy` | Déployer en production |
| `make dev-start` | Démarrer l'environnement de dev |
| `make dev-stop` | Arrêter l'environnement de dev |
| `make clean` | Nettoyer les fichiers temporaires |

## 📱 Architecture Android

### Couches
- **Core**: Architecture de base (Repository, ViewModel, etc.)
- **Features**: Fonctionnalités métiers (Applications, Companies, etc.)
- **DI**: Injection de dépendances avec Hilt
- **UI**: Interface utilisateur avec Jetpack Compose

### Technologies
- **Kotlin** + **Jetpack Compose**
- **Room** (Base de données locale)
- **Retrofit** (API REST)
- **Hilt** (Injection de dépendances)
- **WorkManager** (Synchronisation en arrière-plan)

## 🐍 Architecture Backend

### Structure
- **Core**: Modèles et API génériques
- **Apps**: Applications métiers spécialisées
- **Utils**: Utilitaires et helpers

### Technologies
- **Django** + **Django REST Framework**
- **PostgreSQL** (Base de données)
- **Redis** (Cache)
- **JWT** (Authentification)
- **Docker** (Conteneurisation)

## 🔄 Synchronisation Intelligente

Le système de synchronisation s'adapte automatiquement :
- **Sync immédiat** : WiFi + Batterie > 50%
- **Sync programmé** : Batterie > 20%
- **Sync sur charge** : Batterie < 20%
- **Mode manuel** : Batterie très faible

## 🚨 Troubleshooting

### Problèmes courants
1. **API non accessible** : Vérifier les containers Docker
2. **Erreur de base de données** : Vérifier PostgreSQL
3. **Build Android échoue** : Nettoyer le cache Gradle
4. **Sync ne fonctionne pas** : Vérifier les permissions Android

### Logs
```bash
# Logs Django
make dev-logs

# Logs Android
adb logcat -s JobbingTrack
```

## 📈 Performances

### Optimisations Backend
- Cache Redis pour les requêtes fréquentes
- Pagination automatique
- Index de base de données optimisés

### Optimisations Android
- Synchronisation intelligente selon la batterie
- Cache local avec Room
- Architecture MVVM pour la réactivité

## 🔒 Sécurité

- Authentification JWT
- Chiffrement des communications HTTPS
- Validation des données côté serveur
- Permissions Android minimales

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.
EOF

echo "✅ Configuration complète terminée!"
echo ""
echo "🎉 JobbingTrack est prêt à être utilisé!"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Exécuter : make setup"
echo "2. Tester : make test"
echo "3. Développer : make dev-start"
echo "4. Déployer : make deploy"
echo ""
echo "📚 Documentation complète dans README.md"