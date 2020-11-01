# Generated by Django 3.1.2 on 2020-11-01 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=50)),
                ('name', models.CharField(default='', max_length=50)),
                ('request', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='TestEndpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_endpoints', to='api_client.endpoint')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_endpoints', to='api_client.test')),
            ],
        ),
        migrations.CreateModel(
            name='TestCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now=True, null=True)),
                ('num_users', models.PositiveIntegerField(default=0)),
                ('is_finished', models.BooleanField(default=False)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls', to='api_client.test')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('results', models.TextField()),
                ('test_call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='api_client.testcall')),
            ],
        ),
    ]
