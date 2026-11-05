from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0017_invoice_google_drive_url_lpo_google_drive_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lpo',
            name='currency',
            field=models.CharField(
                max_length=3,
                choices=[
                    ('AED', 'AED - UAE Dirham'),
                    ('INR', 'INR - Indian Rupee'),
                ],
                default='AED',
            ),
        ),
    ]