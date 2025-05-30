# Generated by Django 5.1.6 on 2025-05-07 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0034_contributions_last_penalty_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributions',
            name='last_penalty_date',
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('penalty_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('penalty_date', models.DateTimeField(auto_now_add=True)),
                ('contribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_app.contributions')),
            ],
        ),
    ]
