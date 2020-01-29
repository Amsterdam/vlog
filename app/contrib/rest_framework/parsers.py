from rest_framework.parsers import BaseParser
from contrib.rest_framework.renderers import PlainTextRenderer


class PlainTextParser(BaseParser):
    """
    Parser for form data.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as a URL encoded form,
        and returns the resulting QueryDict.
        """
        parser_context = parser_context or {}
        return stream.read()
