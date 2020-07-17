from django.db import models
from datetime import datetime

# Create your models here.
class Tip(models.Model):
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    match_date = models.DateTimeField()
    prediction = models.CharField(max_length=50)
    prediction_odds = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    home_odds = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    draw_odds = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    away_odds = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    score = models.CharField(max_length=15, null=True)
    status = models.BooleanField(null=True)
    created_at = models.DateTimeField(default=datetime.now)
    is_vip_tip = models.BooleanField(default=False)

    class Meta:
        db_table = 'tips'