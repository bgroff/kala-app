from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from projects.models import Export


class ExportView(View):

    @method_decorator(login_required)
    def get(self, request, token, *args, **kwargs):
        export = get_object_or_404(Export, key=token)
        manager = settings.PLATFORM_MANAGER()
        return redirect(manager.get_export_url(export))
