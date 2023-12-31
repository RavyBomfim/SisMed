# Generated by Django 4.2.5 on 2023-10-16 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0013_especialidade_valor_consulta_delete_tabelapreco'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='agendamedico',
            name='data',
        ),
        migrations.RemoveField(
            model_name='agendamedico',
            name='horarios_disponiveis',
        ),
        migrations.AlterField(
            model_name='agendamedico',
            name='medico',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cadastros.medico'),
        ),
        migrations.CreateModel(
            name='HorarioDisponivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_disponivel', models.TimeField()),
                ('disponivel', models.BooleanField(default=True)),
                ('agenda', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cadastros.dataagenda')),
            ],
        ),
        migrations.AddField(
            model_name='dataagenda',
            name='agenda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.agendamedico'),
        ),
    ]
