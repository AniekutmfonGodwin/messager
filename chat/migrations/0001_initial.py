# Generated by Django 4.0 on 2021-12-09 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilities', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('basemodelmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='utilities.basemodelmixin')),
                ('body', models.TextField(verbose_name='body')),
                ('status', models.CharField(choices=[('READ', 'READ'), ('SEND', 'SEND')], default='SEND', max_length=50, verbose_name='status')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=('utilities.basemodelmixin',),
        ),
    ]