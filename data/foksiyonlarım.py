
import http.client
import json
import ssl

def FullData(date):
    # SSL sertifika doğrulamasını devre dışı bırakma
    context = ssl._create_unverified_context()
    
    # HTTPS bağlantısını oluşturma
    conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
    
    # HTTP isteği yapma
    conn.request('GET', '/api/v1/sport/football/scheduled-events/'+str(date))
    response = conn.getresponse()
    data = json.loads(response.read())["events"]
    
    # İlgili verileri model yapısına dönüştürme
    model_data = {
                'day' : date,
                'data' : data,
                
                }

    return model_data






def MacStats(match_id):
    context = ssl._create_unverified_context()
    
    # HTTPS bağlantısını oluşturma
    conn = http.client.HTTPSConnection('www.sofascore.com', context=context)
    
    conn.request('GET', '/api/v1/event/'+str(match_id)+'/statistics')
    response = conn.getresponse()
    data = json.loads(response.read())["statistics"]


    model_data = {
                   'id':match_id,
                   'data':data
        
    }
    
    # all_data = pd.DataFrame()
  
    # for period_data in data:
    #     period = period_data['period']
    #     for group in period_data['groups']:
    #         group_name = group['groupName']
    #         stats = group['statisticsItems']
            
    #         # Veriyi DataFrame'e çevir
    #         df = pd.json_normalize(stats)
            
    #         # Ekstra sütunlar ekle: period ve groupName
    #         df['period'] = period
    #         df['groupName'] = group_name
            
    #         # Sonuçları ana DataFrame'e ekle
    #         all_data = pd.concat([all_data, df], ignore_index=True)
    #         all_data["match_id"] = match_id
    
    return model_data