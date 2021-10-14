from django.db import connection
from django_test_migrations.contrib.unittest_case import MigratorTestCase


class TestDataMigration(MigratorTestCase):

    def get_model(self, model_name):
        """
        Get a model as in the state it would be at the end of the 'migrate_to'
        state (defined by sub-classes).

        :param model_name: The name of the model to retrieve.

        :return: Django model.
        """
        return self.new_state.apps.get_model('reistijden_v1', model_name)

    def create_objects(self, model_name, *object_dicts):
        """
        Create some objects of the given ``model_name``.

        :param model_name: The name of the model to create instances of
        :param object_dicts: Iterable of dicts which will be passed as keyword
                             arguments to the model.

        :return: Tuple of instances (one for each given object_dict).
        """
        model = self.get_model(model_name)
        objects = tuple(model(**object_dict) for object_dict in object_dicts)
        model.objects.bulk_create(objects)
        return objects

    def call_command(self, command_cls):
        """
        Call the command and check that there were no errors.
        """
        command = command_cls()
        with connection.cursor() as cursor:
            command.migrate(cursor)
            _, errors = command.validate(cursor)
        self.assertEqual(errors, 0)
