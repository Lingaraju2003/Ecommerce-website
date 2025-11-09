# A helper script (optional) to create sample products and a superuser.
# Usage: python seed.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_mini.settings')
django.setup()
from django.contrib.auth.models import User
from shop.models import Product
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin','admin@example.com','Admin@123')
Product.objects.all().delete()
Product.objects.create(name='Wireless Mouse', slug='wireless-mouse', price=299, stock=50, description='A nice mouse')
Product.objects.create(name='Bluetooth Headphones', slug='bt-headphones', price=1299, stock=20, description='Good sound')
print('Seeded DB with admin/Admin@123 and sample products.')
