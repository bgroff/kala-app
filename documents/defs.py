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
    'application/vnd.openxmlformats-officedocument.presentationml.template': 'powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': 'powerpoint',
    'application/vnd.ms-powerpoint.addin.macroEnabled.12': 'powerpoint',
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12': 'powerpoint',
    'application/vnd.ms-powerpoint.template.macroEnabled.12': 'powerpoint',
    'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': 'powerpoint',
    'application/x-deb': 'deb',
    'application/zip': 'zip',
    'image/bmp': 'image',
    'image/gif': 'image',
    'image/jpeg': 'image',
    'image/png': 'image',
    'image/tiff': 'image',
    'application/pdf': 'pdf',
    }

CATEGORY_TO_FILE = {
    'word': 'ooo_writer.png',
    'excel': 'ooo_calc.png',
    'powerpoint': 'ooo_impress.png',
    'deb': 'deb.png',
    'zip': 'tar.png',
    'image': 'image.png',
    'pdf': 'pdf.png',
}

def get_icon_for_mime(mime):
    try:
        file = CATEGORY_TO_FILE[MIME_TO_CATEGORY[mime]]
        return 'img/icons/%s' % file
    except KeyError:
        return 'img/icons/unknown.png'

def get_alt_for_mime(mime):
    try:
        return MIME_TO_CATEGORY[mime] + ' file'
    except KeyError:
        return 'Unknown file'