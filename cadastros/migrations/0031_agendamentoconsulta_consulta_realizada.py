# Generated by Django 4.2.5 on 2023-10-25 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0030_remove_agendamentoconsulta_data_hora_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamentoconsulta',
            name='consulta_realizada',
            field=models.BooleanField(default=False),
        ),
    ]