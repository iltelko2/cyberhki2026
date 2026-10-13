from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_security_demo_user(apps, schema_editor):
	user_model = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
	user_model.objects.using(schema_editor.connection.alias).get_or_create(
		username='admin',
		defaults={'password': make_password(None)},
	)


class Migration(migrations.Migration):
	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.RunPython(create_security_demo_user, migrations.RunPython.noop),
	]
