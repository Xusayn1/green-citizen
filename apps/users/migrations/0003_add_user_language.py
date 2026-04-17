from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_managers_remove_user_date_joined_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[
                    ("RU", "Russian"),
                    ("EN", "English"),
                    ("CRL", "Cyrillic"),
                    ("UZ", "Uzbek"),
                ],
                default="EN",
                max_length=5,
            ),
        ),
    ]
