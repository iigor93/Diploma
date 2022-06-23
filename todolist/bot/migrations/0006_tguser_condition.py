# Generated by Django 4.0.4 on 2022-06-23 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_tguser_user_tgid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='condition',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Начальное состояние'), (2, 'Ожидание названия для категории'), (3, 'Ожидание названия для цели')], default=1, verbose_name='состояние'),
        ),
    ]
