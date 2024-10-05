# tests.py
from django.test import TestCase
from celery.result import EagerResult
from .tasks import fetch_and_save_match_data
from .models import MatchInfo, MatchDataError, RoundinfoModel

class CeleryTaskTest(TestCase):
    
    def setUp(self):
        # Test için gerekli verileri hazırlayın.
        RoundinfoModel.objects.create(
            tournament_id=1,
            season_id=1,
            round=1,
            slug="",
            prefix="",
            week="Devam",
            name="Test Round",
            current=1,
            last=1
        )
    
    def test_fetch_and_save_match_data(self):
        """
        fetch_and_save_match_data Celery görevini test eder.
        """

        # Görevi çalıştır.
        result = fetch_and_save_match_data.delay()

        # Görevin tamamlanmasını bekle.
        self.assertEqual(result.status, 'SUCCESS')

        # Eager mode'da çalıştırdığımız için sonuçları kontrol edebiliriz.
        if isinstance(result, EagerResult):
            result = result.get()
        
        # MatchInfo modeli doldu mu kontrol edelim.
        match_data_count = MatchInfo.objects.count()
        self.assertGreater(match_data_count, 0, "Maç bilgileri MatchInfo modeline eklenmedi.")
        
        # Herhangi bir hata oluştu mu kontrol edelim.
        error_count = MatchDataError.objects.count()
        self.assertEqual(error_count, 0, "Veri işleme sırasında bir hata oluştu ve MatchDataError modeline eklendi.")
