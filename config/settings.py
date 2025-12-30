import os
from pathlib import Path
from datetime import timedelta  # <--- ADICIONE ESTA LINHA DE VOLTA
from dotenv import load_dotenv

# 1. Define a pasta base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Define o caminho exato do arquivo .env
env_path = BASE_DIR / '.env'

# 3. Carrega o arquivo forçando o caminho
load_dotenv(dotenv_path=env_path)

# --- DIAGNÓSTICO (Opcional: Mostra se achou o arquivo) ---
print(f"Procurando .env em: {env_path}")
print(f"Arquivo existe? {env_path.exists()}")
# ---------------------------------------------------------

# SEGURANÇA
# Tenta pegar do .env, se falhar usa a chave insegura
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-FALLBACK-KEY')

# DEBUG
# Lê a string, remove espaços e compara. Se for 'False', vira False.
# Se não existir no .env, assume False (Produção) por segurança.
debug_value = os.environ.get('DEBUG', 'False')
DEBUG = debug_value.strip() == 'True'

print(f"Valor no .env: {debug_value} -> DEBUG final: {DEBUG}")

ALLOWED_HOSTS = ['*']
# Aplicação (Seção 5.1 e 9)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps (Seção 4.1)
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',

    # Local Apps (Domínios do Negócio - Seção 5.2)
    'core',  # Autenticação e Usuários
    'clientes',
    'estoque',
    'servicos'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS headers
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
        'DIRS': [BASE_DIR / 'templates'], # Preparado para templates globais
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

# Banco de Dados (Seção 4.2)
# Configuração padrão SQLite para início rápido.
# Será alterado para PostgreSQL via variáveis de ambiente na fase de infra.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Autenticação (Seção 7 e 9.1)
# CRÍTICO: Define que usaremos nosso próprio modelo de usuário
AUTH_USER_MODEL = 'core.User'

# Validação de Senha (Seção 7.3)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos Estáticos e Mídia (Seção 4.5 e 9.5)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuração do Django Rest Framework (Seção 4.1)
REST_FRAMEWORK = {
    # Por padrão, apenas usuários autenticados podem acessar a API
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Configuração de Autenticação (Login)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication', # Para testar no navegador
        'rest_framework.authentication.BasicAuthentication',   # Para testes simples
    ],
    # Paginação (para não carregar 1000 produtos de uma vez no celular)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Configuração JWT (Seção 7.1)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Configuração de ID Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Diagnóstico de Variáveis (Pode apagar depois)
print(f"--- DIAGNÓSTICO ---")
print(f"DEBUG está valendo: {DEBUG}")
print(f"SECRET_KEY começa com: {SECRET_KEY[:5]}...")
print(f"-------------------")

