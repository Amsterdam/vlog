from django.core.management import BaseCommand
from reistijden_v1.parser import ReistijdenParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        from pathlib import Path

        from reistijden_v1.serializers import PublicationSerializer

        raw_data = Path(f'data.xml').read_text()
        for chunk in raw_data.split('----'):
            try:
                restructured_data = ReistijdenParser(chunk).restructure_data()
                publication_serializer = PublicationSerializer(data=restructured_data)
                publication_serializer.is_valid(raise_exception=True)
                publication_serializer.save()
            except:
                pass
