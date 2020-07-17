# Generated by Django 3.0.8 on 2020-07-05 21:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team', models.CharField(max_length=50)),
                ('away_team', models.CharField(max_length=50)),
                ('match_date', models.DateTimeField()),
                ('prediction', models.CharField(max_length=50)),
                ('odds', models.DecimalField(decimal_places=2, max_digits=3)),
                ('score', models.CharField(max_length=15, null=True)),
                ('status', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('is_vip_tip', models.BooleanField(default=False)),
            ],
        ),
    ]
