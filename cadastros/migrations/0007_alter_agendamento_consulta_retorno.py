# Generated by Django 4.2.5 on 2023-10-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_remove_funcionario_data_cadastro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento_consulta',
            name='retorno',
            field=models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], max_length=4),
        ),
    ]