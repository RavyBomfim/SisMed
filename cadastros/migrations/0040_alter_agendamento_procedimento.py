# Generated by Django 4.2.5 on 2023-11-11 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0039_alter_agendamento_procedimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='procedimento',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
