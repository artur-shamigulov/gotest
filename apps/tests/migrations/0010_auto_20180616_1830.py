# Generated by Django 2.0.3 on 2018-06-16 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_auto_20180616_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestKlassDepenceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('klass', models.CharField(blank=True, max_length=255, null=True, verbose_name='Класс вопроса')),
                ('count', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='testklassdepenceitems',
            name='test_klass_depence',
        ),
        migrations.AlterModelOptions(
            name='testklassdepence',
            options={'verbose_name': 'Настройка классов теста', 'verbose_name_plural': 'Настройки классов теста'},
        ),
        migrations.AlterField(
            model_name='appointedtest',
            name='test_klass_depence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.TestKlassDepence', verbose_name='Настройка классов теста'),
        ),
        migrations.AlterField(
            model_name='availabletest',
            name='test_klass_depence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.TestKlassDepence', verbose_name='Настройка классов теста'),
        ),
        migrations.DeleteModel(
            name='TestKlassDepenceItems',
        ),
        migrations.AddField(
            model_name='testklassdepenceitem',
            name='test_klass_depence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.TestKlassDepence', verbose_name='Настройка классов теста'),
        ),
    ]