# Generated by Django 2.1.2 on 2019-01-07 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Venter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation_name', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='User/Profile Picture/%Y/%m/%d/', verbose_name='Profile Picture')),
                ('phone_number', models.CharField(blank=True, max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='category',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Venter.Organisation'),
        ),
        migrations.AlterField(
            model_name='header',
            name='header',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='header',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Venter.Organisation'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]