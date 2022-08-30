# Generated by Django 4.0.6 on 2022-07-28 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newcart', '0018_order_payment_id_alter_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='addaddress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='addaddress',
            name='email',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='addaddress',
            name='phonenumber',
            field=models.CharField(max_length=120, null=True),
        ),
    ]