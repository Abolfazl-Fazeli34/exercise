# Generated by Django 5.2.1 on 2025-05-20 14:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test01', '0005_alter_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_file', models.ImageField(upload_to='images', verbose_name='عکس')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات عکس')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='test01.post')),
            ],
            options={
                'verbose_name': 'عکس',
                'verbose_name_plural': 'عکس ها',
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['-created'], name='test01_imag_created_024c96_idx')],
            },
        ),
    ]
