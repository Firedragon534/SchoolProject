# ElectroMarket — Django starter

This is a minimal Django project skeleton for a marketplace where listings must be tested before becoming active.

## How to use (PyCharm)
1. Open this folder in PyCharm (`/mnt/data/electromarket_project` in the environment where this file was created).
2. Create a Python virtual environment (recommend Python 3.10+).
3. Install requirements: `pip install -r requirements.txt`.
4. Run migrations:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Log in to admin (`/admin/`) to manage listings and verifications.

## Notes
- This is a starter skeleton: add stricter validators, tests, and production settings before deploying.
- SECRET_KEY in settings.py should be replaced in production and DEBUG turned off.
