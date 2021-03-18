from rest_framework.parsers import BaseParser


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
        return stream.read()
