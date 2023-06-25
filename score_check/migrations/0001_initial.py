# Generated by Django 4.2.2 on 2023-06-19 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReferenceSubject', to='base.schoolinfo')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReferenceSubject', to='base.semesterinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=10)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReferenceSubject', to='score_check.referencegrade')),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceSubsubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subsubject', models.CharField(max_length=10)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReferenceSubject', to='score_check.referencesubject')),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_name', models.CharField(max_length=50)),
                ('score_list', models.CharField(max_length=200)),
                ('subsubject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ReferenceSubsubject', to='score_check.referencesubsubject')),
            ],
        ),
    ]