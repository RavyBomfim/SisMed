# Generated by Django 4.2.5 on 2023-10-13 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_alter_agendamento_consulta_retorno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='data_cadastro',
            field=models.DateField(verbose_name='Data de Cadastro'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='data_cadastro',
            field=models.DateField(verbose_name='Data de Cadastro'),
        ),
    ]
