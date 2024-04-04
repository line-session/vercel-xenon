# Generated by Django 5.0.3 on 2024-04-01 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='medicament',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=10)),
                ('prix', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('dateExpiration', models.DateField()),
                ('stockDisponible', models.IntegerField()),
            ],
        ),
    ]
