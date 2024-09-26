import pandas as pd

def check_excel_columns(excel_path):
    # Excel dosyasını oku
    df = pd.read_excel(excel_path)
    # Sütun isimlerini yazdır
    print("Sütun İsimleri: ", df.columns)

# Excel dosyanızın sütun isimlerini görmek için bu fonksiyonu çağırın
check_excel_columns("Tournaments.xlsx")
