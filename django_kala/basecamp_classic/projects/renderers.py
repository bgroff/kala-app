from io import StringIO

from django.db.models import QuerySet
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_text
from rest_framework.renderers import BaseRenderer


class XMLProjectRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'
    item_tag_name = 'project'
    root_tag_name = 'projects'

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
        if not data.get('projects', False) and not data.get('request_user', False):
            self._to_errors(data, xml)
            xml.endDocument()
            return stream.getvalue()

        # If users are a list, deal with that
        if type(data['projects']) is QuerySet:
            xml.startElement('projects', {'type': 'array'})

            self._to_xml(data['projects'], data['request_user'], xml)

            xml.endElement('projects')
        # Otherwise just render a company
        else:
            self.render_projects(data['projects'], data['request_user'], xml)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, companies, request_user, xml):
        for company in companies:
            self.render_projects(company, request_user, xml)

    def render_projects(self, project, request_user, xml):
            xml.startElement('project', {})
            xml.startElement('id', {'type': 'integer'})
            xml.characters(smart_text(project.id))
            xml.endElement('id')

            xml.startElement('name', {})
            xml.characters(smart_text(project.name))
            xml.endElement('name')

            xml.startElement('announcement', {})
            try:
                xml.characters(smart_text(project.announcement if project.announcement else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('announcement')

            xml.startElement('show-announcements', {})
            try:
                xml.characters(smart_text(project.show_announcements if project.show_announcements else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('show-announcements')
            xml.startElement('show-writeboards', {})
            try:
                xml.characters(smart_text(project.show_writeboards if project.show_writeboards else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('show-writeboards')
            xml.startElement('start-page', {})
            try:
                xml.characters(smart_text(project.start_page if project.start_page else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('start-page')
            xml.startElement('status', {})
            try:
                xml.characters(smart_text(project.status if project.status else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('status')
            xml.startElement('created-on', {'type': 'date'})
            try:
                xml.characters(smart_text(project.created if project.created else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('created-on')
            xml.startElement('last-changed-on', {'type': 'date'})
            try:
                xml.characters(smart_text(project.changed if project.changed else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('last-changed-on')

            xml.startElement('company', {})

            xml.startElement('id', {'type': 'integer'})
            xml.characters(smart_text(project.company.id))
            xml.endElement('id')
            xml.startElement('name', {})
            xml.characters(smart_text(project.company.name))
            xml.endElement('name')

            xml.endElement('company')

            xml.endElement('project')

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

        if data.get('company', False):
            xml.startElement('company', {})
            for error in data['company']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('company')

        xml.endElement('errors')
