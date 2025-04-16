# Generated by Django 5.2 on 2025-04-10 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analisis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfertaEmpleo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portal', models.CharField(max_length=50)),
                ('titulo', models.CharField(max_length=255)),
                ('empresa', models.CharField(max_length=255)),
                ('ubicacion', models.CharField(max_length=255)),
                ('salario', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_publicacion', models.DateField()),
                ('habilidades', models.ManyToManyField(related_name='ofertas', to='analisis.habilidad')),
            ],
        ),
    ]
