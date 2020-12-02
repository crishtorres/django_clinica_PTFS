# Generated by Django 3.1.3 on 2020-11-28 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Turnos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('asistencia', models.CharField(choices=[('P', 'Pendiente'), ('A', 'Asistió'), ('F', 'Faltó')], max_length=1)),
                ('observacion', models.CharField(max_length=250)),
                ('id_medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.pacientes')),
            ],
        ),
    ]
