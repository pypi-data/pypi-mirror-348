import re

import markdown
from django.urls import reverse
from django.utils.translation import gettext as _

from wiki.plugins.attachments import models

ATTACHMENT_RE = re.compile(r'.*(\[attachment\:(?P<id>\d+)\]).*', re.IGNORECASE)


class AttachmentExtension(markdown.Extension):
    """ Abbreviation Extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Insert AbbrPreprocessor before ReferencePreprocessor. """
        md.preprocessors.register(AttachmentPreprocessor(md), 'dw-attachments', 20)

class AttachmentPreprocessor(markdown.preprocessors.Preprocessor):
    """django-wiki attachment preprocessor - parse text for [attachment:id] references. """

    def run(self, lines):
        new_text = []
        for line in lines:
            m = ATTACHMENT_RE.match(line)
            if m:
                attachment_id = m.group('id').strip()
                try:
                    attachment = models.Attachment.objects.get(articles=self.markdown.article,
                                                               id=attachment_id, current_revision__deleted=False)
                    url = reverse('wiki:attachments_download', kwargs={'article_id': self.markdown.article.id,
                                                                       'attachment_id':attachment.id,})
                    line = line.replace(m.group(1), """<span class="attachment"><a href="%s" title="%s">%s</a>""" % 
                                        (url, _("Click to download file"), attachment.original_filename))
                except models.Attachment.DoesNotExist:
                    line = line.replace(m.group(1), """<span class="attachment attachment-deleted">Attachment with ID #%s is deleted.</span>""" % attachment_id)                    
            new_text.append(line)
        return new_text
