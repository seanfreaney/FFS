# Generated by Django 5.1.1 on 2024-11-03 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_requests', '0004_servicerequest_quote_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('customer', 'Customer Document'), ('owner', 'Owner Document')], default='customer', max_length=20),
        ),
    ]