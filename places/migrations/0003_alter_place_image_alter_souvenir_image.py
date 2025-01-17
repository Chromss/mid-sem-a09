# Generated by Django 5.1.3 on 2024-12-20 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_alter_comment_options_remove_place_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='places/images/'),
        ),
        migrations.AlterField(
            model_name='souvenir',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='souvenirs/images/'),
        ),
    ]
