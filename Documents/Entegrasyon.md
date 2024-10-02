# Github projesini klonla

    root@ubuntu-s-1vcpu-512mb-10gb-fra1-01:/home# git clone https://github.com/Ahmetyldrr/SofaPro.git

# Postgresql Veritabanı Oluştur

    sudo -u postgres psql
    
bu komut ile postress e gireriz.

Eski veritabanım vardı bunu siliyorum.

    /l

bu komut ile veritabanım listelenir

        postgres=# psql -U ahmet      
        
        postgres-# \l
                                                                  List of databases
                       Name       |  Owner   | Encoding | Locale Provider | Collate |  Ctype  | ICU Locale | ICU Rules |      Access privileges       
                ------------------+----------+----------+-----------------+---------+---------+------------+-----------+------------------------------
                 postgres         | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | 
                 proje_veritabani | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | =Tc/postgres                +
                                  |          |          |                 |         |         |            |           | postgres=CTc/postgres       +
                                  |          |          |                 |         |         |            |           | proje_kullanici=CTc/postgres
                 soccer_db        | ahmet    | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | =Tc/ahmet                   +
                                  |          |          |                 |         |         |            |           | ahmet=CTc/ahmet
                 template0        | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | =c/postgres                 +
                                  |          |          |                 |         |         |            |           | postgres=CTc/postgres
                 template1        | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | =c/postgres                 +
                                  |          |          |                 |         |         |            |           | postgres=CTc/postgres
                (5 rows)



        DROP DATABASE proje_veritabani;
        DROP DATABASE soccer_db;

Yeni Durumda gereksiz veri tabanları silinmiş olur.

                                                       List of databases
         Name    |  Owner   | Encoding | Locale Provider | Collate |  Ctype  | ICU Locale | ICU Rules |   Access privileges   
      -----------+----------+----------+-----------------+---------+---------+------------+-----------+-----------------------
       postgres  | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | 
       template0 | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | =c/postgres          +
                 |          |          |                 |         |         |            |           | postgres=CTc/postgres
       template1 | postgres | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           | =c/postgres          +
                 |          |          |                 |         |         |            |           | postgres=CTc/postgres

        


şimdi yeni bir veritabanı oluşturarak gerekli yetkileri verelim.

    CREATE DATABASE soccer_database;
    CREATE USER ahmet WITH PASSWORD "ahmet123"
    ALTER ROLE ahmet SET client_encoding TO 'utf8';
    ALTER ROLE ahmet SET default_transaction_isolation TO 'read committed';
    ALTER ROLE ahmet SET timezone TO 'Europe/Istanbul';
    GRANT ALL PRIVILEGES ON DATABASE soccer_database TO ahmet;

Yetkilendirme;
    ALTER DATABASE soccer_database OWNER TO ahmet;
    ALTER SCHEMA public OWNER TO ahmet;

bu işlemlerden sonra veritabanı eklenmiş olacaktır.

# Settings.py Dosyası Ayarları

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'soccer_database',
            'USER': 'ahmet',
            'PASSWORD': 'ahmet123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

bu komutlardan sonra;

    python manage.py makemigrations
    python manage.py migrate
    
komutları ile projede veritabanı oluşur.

  


  

    




