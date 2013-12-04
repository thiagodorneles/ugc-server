# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse as r


class User(models.Model):
    name          = models.CharField(_('Nome'), max_length=100)
    email         = models.EmailField(_('Email'), max_length=100)
    created_at    = models.DateTimeField(_('Criado em'), auto_now_add=True)
    image_url     = models.CharField(_('Avatar caminho'), max_length=100, blank=True)
    # Twitter
    twitter_user  = models.CharField(_('Twitter username'), max_length=50, blank=True)
    twitter_id    = models.CharField(_('Twitter ID'), max_length=100, blank=True)
    twitter_token = models.CharField(_('Twitter Token'), max_length=100, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')

    def __unicode__(self):
        return self.name


class Publish(models.Model):
    title        = models.CharField(_('Titulo'), max_length=100)
    description  = models.TextField(_('Descricao'))
    created_at   = models.DateTimeField(_('Criado em'), auto_now_add=True)
    location     = models.CharField(_(u'Localização'), max_length=50, blank=True)
    city         = models.CharField(_('Cidade'), max_length=100, blank=True)
    status       = models.BooleanField(_('Status'), default=True)
    tags         = models.ManyToManyField('Tag', verbose_name=_('Tag'), related_name='publish', symmetrical=False)
    quant_views  = models.IntegerField(_(u'Visualizações'), default=0)
    quant_blocks = models.IntegerField(_('Bloqueios'), default=0)
    user         = models.ForeignKey('User', verbose_name=_(u'Usuário'))
    
    class Meta:
        unique_together = ('title', 'description')
        ordering = ['-created_at']
        verbose_name = _(u'Publicação')
        verbose_name_plural = _(u'Publicações')
        
    def __unicode__(self):
        return self.title

    def update_views(self):
        self.quant_views += 1
        self.save()

    @property
    def user_name(self):
        """
        Property created by used in /api/publishs/
        """
        return self.user.name

class Tag(models.Model):
    tag        = models.CharField(_('Tag'), max_length=30, unique=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status     = models.BooleanField(_(u'Situação'), default=True)

    class Meta:
        ordering = ['tag']
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')
    
    def __unicode__(self):
        return self.tag
    
class Media(models.Model):
    
#     content = models.URLField(_('Arquivo'))
#     content_type = models.CharField(_('Tipo'), max_length=100)
#     publish = models.ForeignKey('Publish')

    class Meta:
        verbose_name = _(u'Arquivo')
        verbose_name_plural = _(u'Arquivos')
    
#     def __unicode__(self):
#         return content
