# Generated by Django 4.2.5 on 2023-10-18 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0024_alter_horariomedico_dia_semana'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horariomedico',
            name='medico',
        ),
        migrations.CreateModel(
            name='AgendaMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medico', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cadastros.medico')),
            ],
        ),
        migrations.AddField(
            model_name='horariomedico',
            name='agenda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.agendamedico'),
        ),
    ]