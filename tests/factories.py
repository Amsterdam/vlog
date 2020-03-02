import factory
from django.contrib.auth.models import Permission, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    @factory.post_generation
    def permissions(obj, create, extracted, **kwargs):
        if not extracted:
            extracted = []

        for perm in extracted:
            label, codename = perm.split('.')
            obj.user_permissions.set([
                Permission.objects.get(
                    content_type__app_label=label, codename=codename
                )
            ])
