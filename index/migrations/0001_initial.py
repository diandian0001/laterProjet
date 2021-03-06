# Generated by Django 2.0.6 on 2020-03-05 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('status', models.BooleanField()),
                ('pic', models.ImageField(upload_to='../static/image')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
