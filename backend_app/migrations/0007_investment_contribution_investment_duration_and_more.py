# Generated by Django 5.1.6 on 2025-03-24 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0006_investment_expenses_investment_contribution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment_contribution',
            name='investment_duration',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='loans',
            name='approved_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to='backend_app.members'),
        ),
    ]
