
# sofa/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django projenizin ayarlarını belirtin
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofa.settings')

app = Celery('sofa')

# Celery'yi Django ayarlarıyla yapılandırın
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django'daki tüm task'leri otomatik olarak yükler
app.autodiscover_tasks()


# app.conf.beat_schedule = {
    
#     'turnuva_verileri': {
#         'task': 'data.tasks.add_tournaments_from_excel',  # İlk görev
#         'schedule': 120.0,  # 2 dakikada bir çalışacak
#         'args': ('/home/ahmety/Masaüstü/DjangoPro/testdata/Tournament.xlsx',),  # Excel dosya yolu
#     },

#     'hafta_bilgileri': {
#         'task': 'data.tasks.start_all_roundinfo_tasks',  # İkinci görev
#         'schedule': 125.0,  # 2 dakika 5 saniyede bir çalışacak
#     },

#     'hafta_maclari': {
#         'task': 'data.tasks.fetch_and_save_match_data',  # Zincirleme görev
#         'schedule': 150.0,  # 2 dakika 30 saniyede bir çalışacak
#     }
# }



app.conf.timezone = 'Europe/Istanbul'  # Zaman dilimini Istanbul olarak ayarladınız
app.conf.enable_utc = False

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
