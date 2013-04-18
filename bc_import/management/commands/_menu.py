from bc_import.import_from_basecamp import import_groups, import_users, import_projects, import_documents, create_document_from_document_version
from bc_import.models import BCProject, BCDocumentVersion
from companies.models import Companies
import urwid
import requests


class MainMenu():
    def __init__(self, *args, **kwargs):
        palette = [('out', 'default,bold', 'default', 'bold'),]
        self.url = urwid.Edit(('out', u"Basecamp Name:"))
        self.username = urwid.Edit(('out', u"Username:"))

        self.password = urwid.Edit(('out', u"Password:"), mask='*')
        self.confirm = urwid.Edit(('out', u"Confirm Password:"), mask='*')

        self.next = urwid.Button(u'Next')
        self.exit = urwid.Button(u'Exit')
        self.errors = urwid.Text(u"")
        self.pile = urwid.Pile([self.url, self.username, self.password, self.confirm, urwid.Divider(), self.errors,
                                urwid.Divider(), self.next, self.exit])
        self.top = urwid.Filler(self.pile, valign='top')
        urwid.connect_signal(self.next, 'click', self.on_next)
        urwid.connect_signal(self.exit, 'click', self.on_exit_clicked)

        self.main_loop = urwid.MainLoop(self.top)
        self.main_loop.run()

    def on_next(self, button):
        errors = ''
        if not self.url.edit_text:
            errors += ' * The Basecamp Name field is required.\n'
        if not self.username.edit_text:
            errors += ' * The Username field is required.\n'
        if not self.password.edit_text:
            errors += ' * The Password field is required.\n'
        if self.password.edit_text != self.confirm.edit_text:
            errors += ' * The passwords did not match.\n'
        if errors:
            self.errors.set_text(errors)
            return
        self.errors.set_text('')
        url = 'https://%s.basecamphq.com' % self.url.edit_text
        r = requests.get('%s/account.xml' % url, auth=(self.username.edit_text, self.password.edit_text))
        if r.status_code != 200:
            self.errors.set_text('Your input was not correct. Basecamp returned status code: %i' % r.status_code)
            return
        msg = 'Retrieving companies..'
        self.errors.set_text(msg)
        count = import_groups(url, self.username.edit_text, self.password.edit_text)
        msg += '\nRetrieved %i companies\nRetrieving users...' % count
        self.errors.set_text(msg)
        count = import_users(url, self.username.edit_text, self.password.edit_text)
        msg += '\nRetrieved %i users\nRetrieving projects...' % count
        self.errors.set_text(msg)
        count = import_projects(url, self.username.edit_text, self.password.edit_text)
        msg += '\nRetrieved %i projects\nRetrieving document versions...\n' % count
        self.errors.set_text(msg)
        count = 0; i = 0; project_count = BCProject.objects.all().count()
        for project in BCProject.objects.all():
            i += 1
            percentage = 100 * float(i)/float(project_count)
            count += import_documents(url, self.username.edit_text, self.password.edit_text, project.bc_id)
            self.errors.set_text(msg + "Percent complete: %i" % percentage)
        msg += '\nRetrieved %i document versions\nCreating documents...' % count
        self.errors.set_text(msg)
        versions = BCDocumentVersion.objects.all().order_by('bc_collection').distinct('bc_collection')
        for version in versions:
            create_document_from_document_version(version)


    def on_exit_clicked(self, button):
        raise urwid.ExitMainLoop()


def main(url, username, password):
    URL = url
    USERNAME = username
    PASSWORD = password
