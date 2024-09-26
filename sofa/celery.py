from __future__ import absolute_import, unicode_literals
import os
from celery import Celery





# Django ayarlarını kullanmak için
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofa.settings')

app = Celery('sofa')

# Celery'nin ayarları Django ayarlarından almasını sağla
app.config_from_object('django.conf:settings', namespace='CELERY')

# Projedeki task'leri otomatik bul ve yükle
app.autodiscover_tasks()


app.conf.beat_schedule = {
    
    'turnuva_verileri': {
        'task': 'data.tasks.add_tournaments_from_excel',  # İlk görev
        'schedule': 120.0,  # 2 dakikada bir çalışacak
        'args': ('/home/ahmety/Masaüstü/DjangoPro/testdata/Tournament.xlsx',),  # Excel dosya yolu
    },

    'hafta_bilgileri': {
        'task': 'data.tasks.start_all_roundinfo_tasks',  # İkinci görev
        'schedule': 125.0,  # 2 dakika 5 saniyede bir çalışacak
    },

    'hafta_maclari': {
        'task': 'data.tasks.fetch_and_save_match_data',  # Zincirleme görev
        'schedule': 150.0,  # 2 dakika 30 saniyede bir çalışacak
    }
}



app.conf.timezone = 'Europe/Istanbul'  # Zaman dilimini Istanbul olarak ayarladınız
app.conf.enable_utc = False

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
