# Generated by Django 3.1.1 on 2020-09-25 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KlayCalc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('amount', models.IntegerField(default=0)),
                ('donateDate', models.DateTimeField(verbose_name='Date of Donate')),
            ],
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
