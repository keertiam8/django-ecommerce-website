import os
import sys

# adjust path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
import django
django.setup()

from django.apps import apps
Category = apps.get_model('store', 'Category')
Product = apps.get_model('store', 'Product')

print('CATEGORIES (repr):')
for c in Category.objects.all():
    print(repr(c.name))

print('\nPRODUCTS (name -> category repr):')
for p in Product.objects.all():
    cat_name = p.category.name if p.category else None
    print(repr(p.name), '->', repr(cat_name))
