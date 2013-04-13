MIME_TO_CATEGORY = {
    'application/msword': 'word',
    'application/msword': 'word',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'word',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': 'word',
    'application/vnd.ms-word.document.macroEnabled.12': 'word',
    'application/vnd.ms-word.template.macroEnabled.12': 'excel',
    'application/vnd.ms-excel': 'excel',
    'application/vnd.ms-excel': 'excel',
    'application/vnd.ms-excel': 'excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template': 'excel',
    'application/vnd.ms-excel.sheet.macroEnabled.12': 'excel',
    'application/vnd.ms-excel.template.macroEnabled.12': 'excel',
    'application/vnd.ms-excel.addin.macroEnabled.12': 'excel',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12': 'excel',
    'application/vnd.ms-powerpoint': 'powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.template': 'powerpoin',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': 'powerpoint',
    'application/vnd.ms-powerpoint.addin.macroEnabled.12': 'powerpoint',
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12': 'powerpoint',
    'application/vnd.ms-powerpoint.template.macroEnabled.12': 'powerpoint',
    'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': 'powerpoint',

    }

def get_icon_for_mime(mime):
    try:
        category = MIME_TO_CATEGORY[mime]
        return 'icons/%s.png' % category
    except KeyError:
        return 'icons/unknown.png'

