# Generated by Django 4.1.3 on 2022-11-20 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ushopping', '0002_alter_product_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.CharField(max_length=50),
        ),
    ]