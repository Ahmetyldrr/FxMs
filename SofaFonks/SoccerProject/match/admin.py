from django.contrib import admin
from django.contrib import admin
from .models import Result, GoalTime, MacBaskisi, OyuncuPerformans, MacIstatistik
import pandas as pd
import sqlite3
from django.conf import settings
from functions.result import FullData

# GoalTime modelini admin paneline ekleyelim
@admin.register(GoalTime)
class GoalTimeAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'time', 'incident_type', 'is_home', 'match_id')
    search_fields = ('player_name', 'incident_type')
    list_filter = ('is_home', 'incident_type')

# MacBaskisi modelini admin paneline ekleyelim
@admin.register(MacBaskisi)
class MacBaskisiAdmin(admin.ModelAdmin):
    list_display = ('minute', 'value', 'match_id')
    list_filter = ('minute',)

# OyuncuPerformans modelini admin paneline ekleyelim
@admin.register(OyuncuPerformans)
class OyuncuPerformansAdmin(admin.ModelAdmin):
    list_display = ('bs_name', 'bs_position', 'bs_team', 'bs_minutesPlayed', 'bs_rating', 'match_id')
    search_fields = ('bs_name', 'bs_position', 'bs_team')
    list_filter = ('bs_team', 'bs_position')

# MacIstatistik modelini admin paneline ekleyelim
@admin.register(MacIstatistik)
class MacIstatistikAdmin(admin.ModelAdmin):
    list_display = ('name', 'homeValue', 'awayValue', 'key', 'period', 'match_id')
    search_fields = ('name', 'key')
    list_filter = ('period', 'key')



####### VERİ ÇEKME FONKSİYONLARI ###########################


def ResultDataCek(modeladmin, request, queryset):
       
    df = FullData("2024-08-31")
    db_path = settings.DATABASES['default']['NAME']
    conn = sqlite3.connect(db_path)
    df.to_sql('match_result', conn, if_exists='append', index=False)
    conn.close()

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    actions = [ResultDataCek] 
