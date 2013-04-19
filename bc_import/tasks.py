from datetime import datetime
import urllib
import uuid
from defusedxml import ElementTree
from django.conf import settings
from django.utils import timezone
from djcelery import celery
from bc_import.models import BCCompany, BCPerson, BCProject, BCDocumentVersion
from documents.models import Documents, DocumentVersion
import requests


BASE_URL = 'basecamphq.com'


@celery.task
def import_groups(service, username, password):
    r = requests.get('https://%s.%s/companies.xml' % (service, BASE_URL), auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    xml = ElementTree.fromstring(r.text)
    count = 0; created = 0
    for company in xml.findall('company'):
        bc_id = company.find('id').text

        try:
            bc_company = BCCompany.objects.get(bc_id=bc_id)
        except BCCompany.DoesNotExist:
            bc_company = BCCompany(bc_id=bc_id)
            created += 1
        bc_company.name = company.find('name').text
        bc_company.address = company.find('address-one').text
        bc_company.address1 = company.find('address-two').text
        bc_company.country = 'US' # Not Correct
        bc_company.city = company.find('city').text
        bc_company.state = 'HI' # Not Correct #company.find('state').text
        bc_company.locale = company.find('locale').text
        bc_company.fax = company.find('phone-number-fax').text
        bc_company.phone = company.find('phone-number-office').text
        bc_company.web = company.find('web-address').text
        bc_company.timezone = settings.TIME_ZONE
        bc_company.save()
        count += 1
    import_users.delay(service, username, password)
    return count, created


@celery.task
def import_users(service, username, password):
    r = requests.get('https://%s.%s/people.xml' % (service, BASE_URL), auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    xml = ElementTree.fromstring(r.text)
    count = 0; created = 0
    for person in xml.findall('person'):
        bc_id = person.find('id').text
        try:
            p = BCPerson.objects.get(bc_id=bc_id)
        except BCPerson.DoesNotExist:
            p = BCPerson(bc_id=bc_id)
            created += 1
        p.date_joined = datetime.strptime(person.find('created-at').text, '%Y-%m-%dT%H:%M:%SZ')
        p.is_active = person.find('deleted').text
        p.access_new_projects = True if person.find('has-access-to-new-projects').text == 'true' else False
        p.im_handle = person.find('im-handle').text
        p.im_service = person.find('im-service').text
        p.fax = person.find('phone-number-fax').text
        p.home = person.find('phone-number-home').text
        p.mobile = person.find('phone-number-mobile').text
        p.office = person.find('phone-number-office').text
        p.ext = person.find('phone-number-office-ext').text
        p.title = person.find('title').text
        p.last_updated = datetime.strptime(person.find('updated-at').text, '%Y-%m-%dT%H:%M:%SZ').replace(
            tzinfo=timezone.utc)
        p.first_name = person.find('first-name').text
        p.last_name = person.find('last-name').text
        p.company = BCCompany.objects.get(bc_id=person.find('company-id').text)
        p.timezone = person.find('time-zone-name').text
        p.username = person.find('user-name').text
        p.is_superuser = True if person.find('administrator').text == 'true' else False
        p.email = person.find('email-address').text
        p.avatar_url = person.find('avatar-url').text
        if p.username is None:
            p.username = p.email
            p.is_active = False
        p.save()
        count += 1
    import_projects.delay(service, username, password)
    return count, created


@celery.task
def import_projects(service, username, password):
    r = requests.get('https://%s.%s/projects.xml' % (service, BASE_URL), auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    xml = ElementTree.fromstring(r.text)
    count = 0; created = 0
    for project in xml.findall('project'):
        bc_id = project.find('id').text
        try:
            p = BCProject.objects.get(bc_id=bc_id)
        except BCProject.DoesNotExist:
            p = BCProject(bc_id=bc_id)
            created += 1
        p.name = project.find('name').text
        if project.find('last-changed-on').text is not None:
            p.changed = datetime.strptime(project.find('last-changed-on').text, '%Y-%m-%dT%H:%M:%SZ')
        p.created = datetime.strptime(project.find('created-on').text, '%Y-%m-%d')
        p.is_active = project.find('status').text
        p.company = BCCompany.objects.get(bc_id=project.find('company').find('id').text)
        p.save()
        count += 1
    import_documents.delay(service, username, password)
    return count, created


@celery.task
def import_documents(service, username, password):
    count = 0; created = 0
    for project in BCProject.objects.all():
        n = 0
        while True:
            r = requests.get('https://%s.%s/projects/%s/attachments.xml?n=%i' % (service, BASE_URL, project.bc_id, n),
                             auth=(username, password))
            if r.status_code != 200:
                return str(r.status_code) + 'https://%s.%s/projects/%s/attachments.xml?n=%i' % (service, BASE_URL, project.bc_id, n)
            xml = ElementTree.fromstring(r.text)

            documents = xml.findall('attachment')
            for document in documents:
                bc_id = document.find('id').text
                try:
                    d = BCDocumentVersion.objects.get(bc_id=bc_id)
                except BCDocumentVersion.DoesNotExist:
                    d = BCDocumentVersion(bc_id=bc_id)
                    created += 1
                d.created = datetime.strptime(document.find('created-on').text, '%Y-%m-%dT%H:%M:%SZ')
                d.bc_size = document.find('byte-size').text
                d.bc_category = document.find('category-id').text
                d.bc_collection = document.find('collection').text
                d.bc_latest = True if document.find('current').text == 'true' else False
                d.description = document.find('description').text
                d.name = document.find('name').text
                try:
                    d.person = BCPerson.objects.get(bc_id=document.find('person-id').text)
                except BCPerson.DoesNotExist:
                    d.person = None
                d.bc_project = BCProject.objects.get(bc_id=document.find('project-id').text)
                d.bc_url = document.find('download-url').text
                d.save(save_document=False)
                count += 1
            if len(documents) >= 100:
                n += 100
            else:
                break
    create_document_from_document_versions.delay()
    return count, created


@celery.task
def create_document_from_document_versions():
    created = 0
    for version in BCDocumentVersion.objects.all().order_by('bc_collection').distinct('bc_collection'):
        if version.document is None:
            document = Documents.objects.create(name=version.name, project=version.bc_project, date=version.created)
            created += 1
        else:
            document = version.document
        for document_version in BCDocumentVersion.objects.filter(bc_collection=version.bc_collection):
            document_version.document = document
            document_version.save()
        latest = DocumentVersion.objects.filter(document=document).latest()
        document.date = latest.created
        document.save()
    return created


@celery.task
def download_document(document, username, password):
    r = requests.get(document.bc_url, auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    file_name = urllib.unquote(r.url.split('/')[-1:][0])
    file_path = settings.DOCUMENT_ROOT + str(document.uuid)
    f = open(file_path, 'w')
    f.write(r.content)
    f.close()
    document.file = file_path
    document.name = file_name
    document.mime = r.headers['content-type'].split(';')[0]
    document.save()
    return r.status_code
