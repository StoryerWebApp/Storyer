# Generated by Django 4.1.1 on 2022-10-19 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storyer', '0007_alter_student_preferences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='assigned_group',
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_group', to='storyer.group'),
        ),
    ]
