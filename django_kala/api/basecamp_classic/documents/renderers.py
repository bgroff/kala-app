from io import StringIO

from django.db.models import QuerySet
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_text
from rest_framework.renderers import BaseRenderer


class XMLDocumentRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'
    item_tag_name = 'document'
    root_tag_name = 'documents'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        # If we do not have companies or request_user then we have errors
        if not data.get('documents', False) and not data.get('request_user', False):
            self._to_errors(data, xml)
            xml.endDocument()
            return stream.getvalue()

        # If users are a list, deal with that
        if type(data['documents']) is QuerySet:
            xml.startElement('documents', {'type': 'array'})

            self._to_xml(data['documents'], data['request_user'], xml)

            xml.endElement('documents')
        # Otherwise just render a company
        else:
            self.render_document(data['documents'], data['documents'].get_latest(), data['request_user'], xml)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, documents, request_user, xml):
        for document in documents:
            for version in document.documentversion_set.all():
                self.render_document(document, version, request_user, xml)

    def render_document(self, document, version, request_user, xml):
        xml.startElement('document', {})

        xml.startElement('id', {'type': 'integer'})
        xml.characters(smart_text(version.uuid))
        xml.endElement('id')

        xml.startElement('collection', {'type': 'integer'})
        xml.characters(smart_text(document.id))
        xml.endElement('collection')

        xml.startElement('name', {})
        xml.characters(smart_text(document.name))
        xml.endElement('name')

        xml.startElement('byte-size', {})
        xml.characters(smart_text(version.size))
        xml.endElement('byte-size')

        xml.startElement('created-on', {})
        xml.characters(smart_text(version.created.isoformat()))
        xml.endElement('created-on')

        xml.startElement('person-id', {'type': 'integer'})
        xml.characters(smart_text(version.user.pk))
        xml.endElement('person-id')

        xml.startElement('collection', {'type': 'integer'})
        xml.characters(smart_text(document.pk))
        xml.endElement('collection')

        xml.startElement('project-id', {'type': 'integer'})
        xml.characters(smart_text(document.project.pk))
        xml.endElement('project-id')

        xml.startElement('download-url', {})
        xml.characters(smart_text(version.url))
        xml.endElement('download-url')

        xml.startElement('category-id', {'type': 'integer'})
        try:
            xml.characters(smart_text(document.category.id if document.category else ''))
        except AttributeError:
            xml.characters(smart_text(''))
        xml.endElement('category-id')

        xml.startElement('description', {})
        try:
            xml.characters(smart_text(document.description if document.description else ''))
        except AttributeError:
            xml.characters(smart_text(''))
        xml.endElement('description')

        xml.endElement('document')

    def _to_errors(self, data, xml):
        xml.startElement('errors', {})
        if data.get('id', False):
            xml.startElement('id', {'type': 'integer'})
            for error in data['id']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('id')

        if data.get('name', False):
            xml.startElement('name', {})
            for error in data['name']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('name')

        if data.get('size', False):
            xml.startElement('byte-size', {})
            for error in data['size']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('byte-size')

        if data.get('created', False):
            xml.startElement('created-on', {})
            for error in data['address']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('created-on')

        if data.get('user', False):
            xml.startElement('person-id', {})
            for error in data['user']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('person-id')

        if data.get('project', False):
            xml.startElement('project-id', {})
            for error in data['project']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('project')

        if data.get('url', False):
            xml.startElement('download-url', {})
            for error in data['url']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('download-url')

        if data.get('category', False):
            xml.startElement('category-id', {})
            for error in data['category']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('category-id')

        xml.endElement('errors')
