# Generated by Django 4.0.6 on 2022-07-30 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drinker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tonic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GinTonicEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(4, 'Verygood'), (3, 'Good'), (2, 'Average'), (1, 'Bad')])),
                ('created', models.DateTimeField(verbose_name='Rated on')),
                ('drinker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matrix.drinker')),
                ('gin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matrix.gin')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matrix.ingredient')),
                ('tonic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='matrix.tonic')),
            ],
        ),
    ]
