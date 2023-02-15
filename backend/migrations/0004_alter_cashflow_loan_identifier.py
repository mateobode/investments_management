# Generated by Django 4.1.7 on 2023-02-14 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_rename_total_expected_interes_amount_loan_total_expected_interest_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow',
            name='loan_identifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='backend.loan'),
        ),
    ]
