from django.db import migrations


def migrate_delivery_statuses(apps, schema_editor):
    Delivery = apps.get_model("deliveries", "Delivery")
    Delivery.objects.filter(is_cancelled=True).update(status="cancelled")
    Delivery.objects.filter(is_cancelled=False).update(status="active")


def reverse_delivery_statuses(apps, schema_editor):
    Delivery = apps.get_model("deliveries", "Delivery")
    Delivery.objects.filter(status="cancelled").update(is_cancelled=True)
    Delivery.objects.exclude(status="cancelled").update(is_cancelled=False)


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0002_delivery_status'),
    ]

    operations = [
        migrations.RunPython(
            migrate_delivery_statuses,
            reverse_delivery_statuses,
        ),
    ]
