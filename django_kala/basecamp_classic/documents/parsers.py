"""
Provides XML parsing support.
"""
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

import defusedxml.ElementTree as etree
import dateparser


class XMLDocumentParser(BaseParser):
    """
    XML company parser.
    """

    media_type = 'application/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """

        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        parser = etree.DefusedXMLParser(encoding=encoding)
        try:
            tree = etree.parse(stream, parser=parser, forbid_dtd=True)
        except (etree.ParseError, ValueError) as exc:
            raise ParseError(detail=str(exc))
        data = self._xml_convert(tree.getroot())

        return data

    def _xml_convert(self, element):
        """
        convert the xml `element` into the corresponding python object
        """
        data = {}

        fields = list(element)
        for field in fields:
            if field.tag == 'id':
                data['id'] = str(field.text)

            if field.tag == 'name':
                data['name'] = str(field.text)

            if field.tag == 'description':
                data['description'] = str(field.text)

            if field.tag == 'byte-size':
                data['size'] = str(field.text)

            if field.tag == 'category-id' and field.text:
                data['category'] = int(str(field.text))

            if field.tag == 'created-on':
                data['created'] = dateparser.parse(field.text)

            if field.tag == 'person-id':
                data['person'] = int(str(field.text))

            if field.tag == 'project-id':
                data['project'] = int(str(field.text))

            if field.tag == 'download-url':
                data['url'] = str(field.text)

            if field.tag == 'collection':
                data['collection'] = str(field.text)

        return data
