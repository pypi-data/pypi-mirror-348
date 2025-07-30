from django.db.models import signals
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_notify.models import Subscription, notify
from wiki import models as wiki_models
from wiki.core.plugins import registry
from wiki.models.pluginbase import ArticlePlugin
from wiki.plugins.notifications import \
    ARTICLE_EDIT  # TODO: Is this bad practice?
from wiki.plugins.notifications import settings


class ArticleSubscription(ArticlePlugin, Subscription):
    
    def __unicode__(self):
        return (_("%(user)s subscribing to %(article)s (%(type)s)") % 
                {'user': self.settings.user.username,
                 'article': self.article.current_revision.title,
                 'type': self.notification_type.label})

    class Meta:
        db_table = 'wiki_notifications_articlesubscription'


def default_url(article, urlpath=None):
    try:
        if not urlpath:
            urlpath = wiki_models.URLPath.objects.get(article=article)
        url = reverse('wiki:get', kwargs={'path': urlpath.path})
    except wiki_models.URLPath.DoesNotExist:
        url = reverse('wiki:get', kwargs={'article_id': article.id})
    return url


def post_article_revision_save(instance, **kwargs):
    if kwargs.get('created', False):
        url = default_url(instance.article)
        if instance.deleted:
            notify(_('Article deleted: %s') % instance.title, ARTICLE_EDIT,
                   target_object=instance.article, url=url)
        elif instance.previous_revision:
            notify(_('Article modified: %s') % instance.title, ARTICLE_EDIT,
                   target_object=instance.article, url=url)
        else:
            notify(_('New article created: %s') % instance.title, ARTICLE_EDIT,
                   target_object=instance, url=url)


# Whenever a new revision is created, we notifý users that an article
# was edited
signals.post_save.connect(post_article_revision_save, sender=wiki_models.ArticleRevision,)

# TODO: We should notify users when the current_revision of an article is
# changed...

##################################################
# NOTIFICATIONS FOR PLUGINS
##################################################
for plugin in registry.get_plugins():
    
    notifications = getattr(plugin, 'notifications', [])
    for notification_dict in notifications:
        def plugin_notification(instance, **kwargs):
            if notification_dict.get('ignore', lambda x: False)(instance):
                return
            if kwargs.get('created', False) == notification_dict.get('created', True):
                url = None
                if 'get_url' in notification_dict:
                    url = notification_dict['get_url'](instance)
                else:
                    url = default_url(notification_dict['get_article'](instance))
                
                message = notification_dict['message'](instance)
                notify(message, notification_dict['key'],
                       target_object=notification_dict['get_article'](instance), url=url)

        signals.post_save.connect(plugin_notification, sender=notification_dict['model'])
