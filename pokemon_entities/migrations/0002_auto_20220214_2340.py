# Generated by Django 3.1.14 on 2022-02-14 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evolution', to='pokemon_entities.pokemon'),
        ),
    ]