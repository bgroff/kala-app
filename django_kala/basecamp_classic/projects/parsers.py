"""
Provides XML parsing support.
"""
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

import defusedxml.ElementTree as etree
import dateparser


class XMLProjectParser(BaseParser):
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
                data['id'] = int(str(field.text).strip())
            if field.tag == 'name':
                data['name'] = str(field.text)

            if field.tag == 'announcement':
                data['announcement'] = str(field.text)
            if field.tag == 'show-announcements':
                data['show_announcements'] = str(field.text)
            if field.tag == 'show-writeboards':
                data['show_writeboards'] = str(field.text)
            if field.tag == 'start-page':
                data['start_page'] = str(field.text)
            if field.tag == 'status':
                data['status'] = str(field.text)

            if field.tag == 'created-on':
                data['created'] = dateparser.parse(str(field.text))
            if field.tag == 'last-changed-on':
                data['changed'] = str(field.text)

            if field.tag == 'company':
                for _field in field:
                    if _field.tag == 'id':
                        data['company'] = int(str(_field.text).strip())
                    if field.tag == 'name':
                        data['company_name'] = str(_field.text)

        return data


class XMLCategoryParser(BaseParser):
    """
    XML category parser.
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
                data['id'] = int(str(field.text).strip())
            if field.tag == 'name':
                data['name'] = str(field.text)
            if field.tag == 'type':
                data['type'] = str(field.text)
            if field.tag == 'project-id':
                data['project'] = int(str(field.text).strip())

            if field.tag == 'elements-count':
                data['elements_count'] = str(field.text)
        return data
