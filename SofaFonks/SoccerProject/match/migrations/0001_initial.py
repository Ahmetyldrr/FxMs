# Generated by Django 5.1 on 2024-09-08 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalTime',
            fields=[
                ('time', models.IntegerField()),
                ('incident_type', models.CharField(max_length=50)),
                ('is_home', models.BooleanField()),
                ('incident_class', models.CharField(max_length=50)),
                ('player_name', models.CharField(max_length=100)),
                ('assist1_name', models.CharField(blank=True, max_length=100, null=True)),
                ('match_id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MacBaskisi',
            fields=[
                ('minute', models.IntegerField()),
                ('value', models.IntegerField()),
                ('match_id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MacIstatistik',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('home', models.CharField(blank=True, max_length=50, null=True)),
                ('away', models.CharField(blank=True, max_length=50, null=True)),
                ('compareCode', models.IntegerField()),
                ('statisticsType', models.CharField(max_length=50)),
                ('valueType', models.CharField(max_length=50)),
                ('homeValue', models.FloatField()),
                ('awayValue', models.FloatField()),
                ('renderType', models.IntegerField()),
                ('key', models.CharField(max_length=50)),
                ('period', models.CharField(max_length=50)),
                ('groupName', models.CharField(max_length=100)),
                ('match_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('homeTotal', models.FloatField(blank=True, null=True)),
                ('awayTotal', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OyuncuPerformans',
            fields=[
                ('bs_team', models.CharField(max_length=10)),
                ('bs_name', models.CharField(max_length=100)),
                ('bs_shortName', models.CharField(max_length=50)),
                ('bs_position', models.CharField(max_length=2)),
                ('bs_jerseyNumber', models.IntegerField()),
                ('bs_country', models.CharField(max_length=100)),
                ('bs_userCount', models.IntegerField()),
                ('bs_marketValueCurrency', models.CharField(max_length=3)),
                ('bs_minutesPlayed', models.IntegerField()),
                ('bs_rating', models.FloatField()),
                ('at_totalPass', models.IntegerField()),
                ('at_accuratePass', models.IntegerField()),
                ('at_goalAssist', models.IntegerField()),
                ('at_shotOffTarget', models.IntegerField()),
                ('at_onTargetScoringAttempt', models.IntegerField()),
                ('at_bigChanceMissed', models.IntegerField()),
                ('at_expectedGoals', models.FloatField()),
                ('at_expectedAssists', models.FloatField()),
                ('at_keyPass', models.IntegerField()),
                ('at_totalLongBalls', models.IntegerField()),
                ('at_accurateLongBalls', models.IntegerField()),
                ('at_touches', models.IntegerField()),
                ('at_possessionLostCtrl', models.IntegerField()),
                ('de_aerialWon', models.IntegerField()),
                ('de_duelLost', models.IntegerField()),
                ('de_duelWon', models.IntegerField()),
                ('de_challengeLost', models.IntegerField()),
                ('de_dispossessed', models.IntegerField()),
                ('de_totalContest', models.IntegerField()),
                ('de_wonContest', models.IntegerField()),
                ('de_outfielderBlock', models.IntegerField()),
                ('de_totalTackle', models.IntegerField()),
                ('de_fouls', models.IntegerField()),
                ('de_interceptionWon', models.IntegerField()),
                ('de_totalClearance', models.IntegerField()),
                ('go_saves', models.IntegerField()),
                ('go_goalsPrevented', models.FloatField()),
                ('go_penaltySave', models.IntegerField()),
                ('home_formation', models.CharField(max_length=10)),
                ('away_formation', models.CharField(max_length=10)),
                ('match_id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('tarih', models.CharField(max_length=50)),
                ('custom_id', models.CharField(max_length=50)),
                ('match_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('start_timestamp', models.BigIntegerField()),
                ('tournament_name', models.CharField(max_length=255)),
                ('tournament_category_name', models.CharField(max_length=100)),
                ('season_name', models.CharField(max_length=100)),
                ('season_year', models.CharField(max_length=10)),
                ('tournament_unique_tournament_id', models.IntegerField()),
                ('season_id', models.BigIntegerField()),
                ('round_info_round', models.IntegerField()),
                ('status_type', models.CharField(max_length=50)),
                ('home_team_name', models.CharField(max_length=100)),
                ('home_team_name_code', models.CharField(max_length=10)),
                ('home_team_id', models.IntegerField()),
                ('home_score_display', models.IntegerField()),
                ('home_score_period1', models.IntegerField()),
                ('home_score_period2', models.IntegerField()),
                ('away_team_name', models.CharField(max_length=100)),
                ('away_team_name_code', models.CharField(max_length=10)),
                ('away_team_id', models.IntegerField()),
                ('away_score_display', models.IntegerField()),
                ('away_score_period1', models.IntegerField()),
                ('away_score_period2', models.IntegerField()),
            ],
        ),
    ]