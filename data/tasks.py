# uygulama_adi/tasks.py
from celery import shared_task
import pandas as pd
from .models import Tournament
import http.client
import json
import pandas as pd
from datetime import datetime




def RoundData(t,s,r,slug="",prefix=""):


    """
    
https://www.sofascore.com/api/v1/unique-tournament/7/season/61644/events/round/636/slug/playoff-round/prefix/Qualification
https://www.sofascore.com/api/v1/unique-tournament/7/season/61644/events/round/1/slug/

data = RoundData(804,61242,29,"final","")
data = RoundData(7,61644,636,"playoff-round","Qualification")

bu fonksiyonda 5 parametre istenmektedir. 3 tanesi zorunlu diğerleri ise turnuva maçlarında
kullanılmaktadır.Grup maçları için bir düzenleme yapılmamıştır.

    

    
    """

    conn = http.client.HTTPSConnection('www.sofascore.com')
    if slug=="" and prefix=="": 
    
        conn.request(
            'GET',
            '/api/v1/unique-tournament/'+str(t)+'/season/'+str(s)+'/events/round/'+str(r),
        )
        
    elif prefix=="":
         conn.request(
            'GET',
            '/api/v1/unique-tournament/'+str(t)+'/season/'+str(s)+'/events/round/'+str(r)+'/slug/'+str(slug),
        )
    else:
        conn.request(
            'GET',
            '/api/v1/unique-tournament/'+str(t)+'/season/'+str(s)+'/events/round/'+str(r)+'/slug/'+str(slug)+'/prefix/'+str(prefix),
        )
        
    response = conn.getresponse()
    data = json.loads(response.read())["events"]
    data1 = pd.json_normalize(data, sep='_')
    columns_to_select = ["id", "startTimestamp", "tournament_name", "tournament_category_name", "tournament_category_id", 
                "tournament_uniqueTournament_name", "tournament_uniqueTournament_id", "season_name", "season_year", 
                "season_id", "roundInfo_round", "status_type", "homeTeam_name", "homeTeam_nameCode", "homeTeam_id", 
                "awayTeam_name", "awayTeam_nameCode", "awayTeam_id", "homeScore_period1", "homeScore_period2", 
                "homeScore_normaltime", "awayScore_period1", "awayScore_period2", "awayScore_normaltime"]
    

    


    for column in columns_to_select:
        
        
        if column not in data1.columns:
            data1[column] = ""  
            try:
                data1[column]=data1[column].replace("",0).repalce(" ",0)
            except:
                pass
            

    df = data1[columns_to_select]

    #df["UpdateTime"] = datetime.now()
    df=df.fillna("")

    return df



def Roundinfo(t,s):


    """
    
    
    #https://www.sofascore.com/api/v1/unique-tournament/17015/season/61648/rounds
#https://www.sofascore.com/api/v1/unique-tournament/13363/season/57319/rounds
#52,63814
#https://www.sofascore.com/api/v1/unique-tournament/804/season/61242/events/round/29/slug/final
df = Roundinfo(804,61242)
df
# hafta_indices = df[df['week'] == 'Devam'].index
# hafta = dict(df.iloc[hafta_indices[0]])
# data = RoundData(hafta["tournament_id"],hafta["season_id"],hafta["round"],hafta["slug"],hafta["prefix"])
# data.to_excel("Haftanın_Maçları.xlsx")
# data


bu fonksiyon ile ligin hangi haftada olduğu ve biten maçları alınır.
ayrıca ilgili hafta yukarıda koda göre dizayn edilebilir.

    
    """

    conn = http.client.HTTPSConnection('www.sofascore.com')
    conn.request('GET', '/api/v1/unique-tournament/'+str(t)+'/season/'+str(s)+'/rounds')
    response = conn.getresponse()
    data = json.loads(response.read())
    all_round  = pd.DataFrame(data["rounds"])
    all_round["current"] = data["currentRound"]["round"]
    
    all_round["week"] = all_round.apply(
        lambda row: "Devam" if row["round"] == row["current"] 
        else "Biten" if row["round"] < row["current"] 
        else "Baslamadı", axis=1)
    
    # "last" sütununun eklenmesi (Ligin son haftası)
    all_round["last"] = len(all_round)

    all_round["tournament_id"] = t
    all_round["season_id"] = s

    columns_to_select = ['round', 'name', 'slug', 'prefix', 'current', 'week', 'last','tournament_id', 'season_id']
    
    for column in columns_to_select:
        if column not in all_round.columns:
            all_round[column] = ""  
            
    df = all_round[columns_to_select]
    
    #df["UpdateTime"] = datetime.now()
    
    devam_indices = df[df['week'] == 'Devam'].index
    if len(devam_indices) > 1:
        for i in range(devam_indices[0],devam_indices[1]):
            df.loc[i, 'week'] = 'Biten'
            
  
    df = df.fillna("")
    
    return df


from .models import RoundinfoModel



@shared_task
def add_tournaments_from_excel(excel_path):
   
        df = pd.read_excel(excel_path)
        df.columns = df.columns.str.strip()
        
        for index, row in df.iterrows():
            try:
                Tournament.objects.create(
                    season_id=row['season_id'],
                    tournament_id=row['tournament_id'],
                    country_name=row['country_name'],
                    tournament_name=row['tournament_name'],
                    season_name=row['season_name'],
                    season_year=row['season_year'],
                    hasGlobalHighlights=row['hasGlobalHighlights'],
                    hasEventPlayerStatistics=row['hasEventPlayerStatistics'],
                    hasEventPlayerHeatMap=row['hasEventPlayerHeatMap']
                )
            except:
                 pass


from .models import Tournament ,RoundinfoErrorLog  

import time



@shared_task
def start_all_roundinfo_tasks():

    tournaments = Tournament.objects.all()  # Tüm turnuvaları alıyoruz
    
    for tournament in tournaments:
        print(tournament.tournament_id)
        time.sleep(1)
        try:
            df = Roundinfo(tournament.tournament_id, tournament.season_id)  # API'den veri çekme
            for _, row in df.iterrows():
                RoundinfoModel.objects.update_or_create(
                    tournament_id=row['tournament_id'],  # Model alanı olan `tournament_id`
                    season_id=row['season_id'],  # Model alanı olan `season_id`
                    round=row['round'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                        'prefix': row['prefix'],
                        'current': row['current'],
                        'week': row['week'],
                        'last': row['last'],
                    
                    }
                )

        except Exception as e:
            # Eğer bir hata olursa, ErrorLog modeline kaydediyoruz
            RoundinfoErrorLog.objects.create(
                tournament_id=tournament.tournament_id,
                season_id=tournament.season_id,
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )


            

from celery import shared_task
from .models import RoundinfoModel, MatchInfo, MatchDataError
import http.client
import json
import pandas as pd
from datetime import datetime


@shared_task
def fetch_and_save_match_data():
    # week="Biten" olan turları seç
    #rounds = RoundinfoModel.objects.filter(week="Devam")
    rounds = RoundinfoModel.objects.all()
    for round_info in rounds:
        try:
            # SofaScore API'sinden verileri almak için gerekli parametreler
            tournament_id = round_info.tournament_id
            season_id = round_info.season_id
            round_num = round_info.round
            slug = round_info.slug if round_info.slug else ""
            prefix = round_info.prefix if round_info.prefix else ""
            
            # SofaScore API'sinden verileri çek
            df = RoundData(tournament_id, season_id, round_num, slug, prefix)
            
            # Alınan verileri MatchInfo modeline kaydet
            for index, row in df.iterrows():
                # Her bir sütun için NaN veya boş stringleri kontrol edip uygun değerler atıyoruz
                def clean_score(value):
                    """Boş değerler veya NaN'ları None veya 0 olarak temizler."""
                    if pd.isna(value) or value == '':
                        return None  # Null değerler için None kullanılıyor
                    return value  # Değer uygunsa, olduğu gibi döndür
                
                # Değerlerin temizlenmesi
                homeScore_period1 = clean_score(row["homeScore_period1"])
                homeScore_period2 = clean_score(row["homeScore_period2"])
                homeScore_normaltime = clean_score(row["homeScore_normaltime"])
                awayScore_period1 = clean_score(row["awayScore_period1"])
                awayScore_period2 = clean_score(row["awayScore_period2"])
                awayScore_normaltime = clean_score(row["awayScore_normaltime"])

                # MatchInfo modeline verileri kaydediyoruz
                MatchInfo.objects.update_or_create(
                    idx=row["id"],  # Maçın benzersiz ID'si
                    season_id=row["season_id"],  # Sezon ID'si
                    defaults={
                        'startTimestamp': row["startTimestamp"],
                        'tournament_name': row["tournament_name"],
                        'tournament_category_name': row["tournament_category_name"],
                        'tournament_category_id': row["tournament_category_id"],
                        'tournament_uniqueTournament_name': row["tournament_uniqueTournament_name"],
                        'tournament_uniqueTournament_id': row["tournament_uniqueTournament_id"],
                        'season_name': row["season_name"],
                        'season_year': row["season_year"],
                        'roundInfo_round': row["roundInfo_round"],
                        'status_type': row["status_type"],
                        'homeTeam_name': row["homeTeam_name"],
                        'homeTeam_nameCode': row["homeTeam_nameCode"],
                        'homeTeam_id': row["homeTeam_id"],
                        'awayTeam_name': row["awayTeam_name"],
                        'awayTeam_nameCode': row["awayTeam_nameCode"],
                        'awayTeam_id': row["awayTeam_id"],
                        'homeScore_period1': homeScore_period1,
                        'homeScore_period2': homeScore_period2,
                        'homeScore_normaltime': homeScore_normaltime,
                        'awayScore_period1': awayScore_period1,
                        'awayScore_period2': awayScore_period2,
                        'awayScore_normaltime': awayScore_normaltime,
                    }
                )
        except Exception as e:
            # Eğer bir hata olursa, MatchDataError modeline kaydediyoruz
            MatchDataError.objects.create(
                tournament_id=round_info.tournament_id,  # Hangi turnuvada hata olduğunu kaydediyoruz
                season_id=round_info.season_id,  # Hangi sezonda hata olduğunu kaydediyoruz
                round_num=round_info.round,  # Hangi turda hata olduğunu kaydediyoruz
                slug=slug,  # Slug (opsiyonel)
                prefix=prefix,  # Ön ek (opsiyonel)
                error_message=str(e)  # Hata mesajını kaydediyoruz
            )
