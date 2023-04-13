# Generated by Django 3.2.16 on 2023-04-13 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('contacts', models.ManyToManyField(blank=True, related_name='tags', to='automation.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automation.emaillist')),
                ('tags', models.ManyToManyField(blank=True, related_name='segments', to='automation.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='emailcampaign',
            name='segments',
            field=models.ManyToManyField(blank=True, to='automation.Segment'),
        ),
    ]