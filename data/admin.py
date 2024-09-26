
from django.contrib import admin
from .models import Tournament

class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        'season_id', 
        'tournament_id',
        'tournament_name', 
        'country_name', 
        'season_name', 
        'season_year', 
        'hasGlobalHighlights', 
        'hasEventPlayerStatistics',  # Bu alanı ekledik
        'hasEventPlayerHeatMap'  # Bu alanı ekledik
    )
    list_filter = ('tournament_name', 'country_name', 'season_year', 'hasGlobalHighlights')
    search_fields = ('tournament_name', 'country_name', 'season_name', 'season_year')
    list_editable = ('hasGlobalHighlights', 'hasEventPlayerStatistics', 'hasEventPlayerHeatMap')

    fieldsets = (
        (None, {
            'fields': ('season_id', 'tournament_id', 'country_name', 'tournament_name', 'season_name', 'season_year')
        }),
        ('Özellikler', {
            'fields': ('hasGlobalHighlights', 'hasEventPlayerStatistics', 'hasEventPlayerHeatMap'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Tournament, TournamentAdmin)


import pandas as pd
from django.http import HttpResponse
from .models import RoundinfoModel

@admin.action(description="Seçilen Roundinfo verilerini Excel'e indir")
def export_to_excel(modeladmin, request, queryset):
    # Queryset'ten alınan verileri bir DataFrame'e dönüştürüyoruz
    data = queryset.values(
        'tournament_id', 'season_id', 'round', 'name', 'slug', 'prefix', 'current', 'week', 'last', 'UpdateTime'
    )
    df = pd.DataFrame.from_records(data)

    # Zaman dilimi farkını kaldırıyoruz (Excel bunu desteklemediği için)
    if 'UpdateTime' in df.columns:
        df['UpdateTime'] = df['UpdateTime'].dt.tz_localize(None)

    # Excel dosyasına aktarmak için HTTP response oluşturuyoruz
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=roundinfo.xlsx'

    # DataFrame'i Excel dosyasına yazıyoruz
    df.to_excel(response, index=False, engine='openpyxl')

    return response



class RoundinfoModelAdmin(admin.ModelAdmin):
    list_display = ('round', 'name', 'current', 'week', 'last', 'tournament_id', 'season_id', 'UpdateTime')  # Liste görünümü
    list_filter = ('week', 'current', 'last')  # Filtreleme
    search_fields = ('name', 'slug', 'tournament_id', 'season_id')  # Arama yapılacak alanlar
    ordering = ('-UpdateTime',)  # Güncelleme zamanına göre sıralama (en son güncellenenler önce)
    actions = [export_to_excel]

admin.site.register(RoundinfoModel, RoundinfoModelAdmin)







from .models import MatchInfo

class MatchInfoAdmin(admin.ModelAdmin):
    list_display = ('homeTeam_name', 'awayTeam_name', 'tournament_name', 'status_type', 'roundInfo_round', 'homeScore_normaltime', 'awayScore_normaltime', 'UpdateTime')  # Liste görünümü
    list_filter = ('tournament_name', 'status_type', 'roundInfo_round')  # Filtreleme
    search_fields = ('homeTeam_name', 'awayTeam_name', 'tournament_name', 'season_year')  # Arama yapılacak alanlar
    ordering = ('-startTimestamp',)  # Maç zamanına göre sıralama (en yeni maçlar önce)

admin.site.register(MatchInfo, MatchInfoAdmin)




from django.contrib import admin
from .models import RoundinfoErrorLog

@admin.register(RoundinfoErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('tournament_id', 'season_id', 'error_message', 'created_at')  # Görüntülenecek alanlar





from .models import MatchDataError

# MatchDataError modelini admin paneline ekliyoruz
@admin.register(MatchDataError)
class MatchDataErrorAdmin(admin.ModelAdmin):
    list_display = ('tournament_id', 'season_id', 'round_num', 'slug', 'prefix', 'error_message', 'created_at')
    search_fields = ('tournament_id', 'season_id', 'round_num', 'slug', 'prefix')
    list_filter = ('tournament_id', 'season_id', 'created_at')
    readonly_fields = ('created_at',)
