# PostgreSQL Kurulumu (Ubuntu)

## Terminal üzerinde PostgreSQL'i şu komutla kurabilirsiniz
    sudo apt update
    sudo apt install postgresql postgresql-contrib
## Kurulum tamamlandıktan sonra PostgreSQL servisini başlatın:
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
## PostgreSQL'e giriş yapın
    sudo -i -u postgres
    psql
## Bir veritabanı ve kullanıcı oluşturun

   CREATE DATABASE django_project_db; <br>
   CREATE USER django_user WITH PASSWORD 'your_password';<br>
   ALTER ROLE django_user SET client_encoding TO 'utf8';<br>
   ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';<br>
   ALTER ROLE django_user SET timezone TO 'UTC';<br>
   GRANT ALL PRIVILEGES ON DATABASE django_project_db TO django_user;<br>

## Django setting.py ayarlama

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_project_db',  # PostgreSQL'de oluşturduğunuz veritabanı adı
        'USER': 'django_user',  # PostgreSQL'de oluşturduğunuz kullanıcı
        'PASSWORD': 'your_password',  # Kullanıcı için belirlediğiniz şifre
        'HOST': 'localhost',  # Eğer aynı makine üzerindeyse localhost
        'PORT': '5432',  # Varsayılan PostgreSQL portu
    }
}

    python manage.py makemigrations
    python manage.py migrate
## Hata

Error loading psycopg2 or psycopg module

    pip install psycopg2
    pip install psycopg2-binary

ERROR: Failed building wheel for psycopg2

    sudo apt update
    sudo apt install python3-dev libpq-dev build-essential
    pip install --upgrade pip wheel setuptools

failed: FATAL:  password authentication failed for user "django_user"
Bu hata, PostgreSQL sunucusuna bağlanmaya çalışırken kullanıcı adı ve şifre doğrulamasında bir sorun yaşandığını belirtir. 
Hata mesajında, "password authentication failed" diyor, yani django_user kullanıcısının kimlik doğrulaması için girilen şifre doğru değil.

Şifreyi sıfırlamak için şu komutu çalıştırın:
    ALTER USER django_user WITH PASSWORD 'new_password';<br>

Sistemi tekrar çalıştır.
    sudo systemctl status postgresql<br>
    sudo systemctl start postgresql <br>

ERROR : django.db.migrations.exceptions.MigrationSchemaMissing: Unable to create the django_migrations table (permission denied for schema public
Şema üzerinde gerekli izinleri vermek için şu komutları çalıştırın<br>
    GRANT ALL PRIVILEGES ON DATABASE django_project_db TO django_user;<br>
    ALTER USER django_user CREATEDB;<br>

Veritabanındaki public şeması üzerinde de izinleri güncelleyin.<br>
    GRANT ALL ON SCHEMA public TO django_user;<br>

Kullanıcınızın yetkilerini kontrol etmek için<br>
    \du<br>

Öncelikle, PostgreSQL'deki django_user kullanıcısının gerçekten yetkilere sahip olup olmadığını doğrulamanız önemlidir. <br>
    \du <br>
komutuyla kullanıcıya verilen izinleri ve varsayılan yetkileri kontrol edin<br>
    GRANT ALL PRIVILEGES ON DATABASE django_project_db TO django_user;<br>
    GRANT ALL ON SCHEMA public TO django_user;<br>
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO django_user;<br>

ÇÖZÜM : Veritabanı Sahipliği Sorunu (Owner)<br>
    ALTER DATABASE django_project_db OWNER TO django_user;<br>
    ALTER SCHEMA public OWNER TO django_user;<br>






