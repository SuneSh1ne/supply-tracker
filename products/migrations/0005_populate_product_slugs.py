from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_product_slugs(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    for product in Product.objects.all().order_by("pk"):
        base_slug = slugify(unidecode(product.name)) or "product"
        product.slug = f"{base_slug}-{product.pk}"
        product.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_product_slug"),
    ]

    operations = [
        migrations.RunPython(populate_product_slugs, migrations.RunPython.noop),
    ]
