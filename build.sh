#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Seed initial categories and admin account if not already present
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
from services.models import Category

# 1. Create default categories
for name in ['Mechanic', 'Plumber', 'Electrician', 'House Cleaning', 'Carpenter']:
    Category.objects.get_or_create(name=name)

# 2. Create superuser if ADMIN_PASSWORD is set in Render Environment Variables
User = get_user_model()
admin_pass = os.getenv('ADMIN_PASSWORD', 'AdminPass123!')
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', email='admin@example.com', password=admin_pass)
    print('Superuser admin created!')
"