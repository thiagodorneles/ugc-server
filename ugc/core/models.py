# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Publish(models.Model):
    title       = models.CharField(_('Titulo'), max_length=100)
    description = models.TextField(_('Descricao'))
    created_at  = models.DateTimeField(_('Data/Hora'))
    location    = models.CharField(_('Localizacao'), max_length=50, blank=True)
    city        = models.CharField(_('Cidade'), max_length=100, blank=True)
    status      = models.BooleanField(_('Status'))
    # tags        = models.ManyToManyField('Tag', verbose_name=_('Tag'))
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _(u'Publicação')
        verbose_name_plural = _(u'Publicações')
        
    def __unicode__(self):
        return self.title

# class Tags(models.Model):
#     tag = models.CharField(_('Tag'), max_length=30)

#     class Meta:
#         ordering = ['tag']
#         verbose_name = _(u'Tag')
#         verbose_name_plural = _(u'Tags')
    
#     def __unicode__(self):
#         return self.tag
    
# class Midia(models.Model):
#     content = models.URLField(_('Arquivo'))
#     content_type = models.CharField(_('Tipo'), max_length=100)
#     publish = models.ForeignKey('Publish')

#     # class Meta:
#     #     verbose_name = _(u'Arquivo')
#     #     verbose_name_plural = _(u'Arquivos')
    
#     def __unicode__(self):
#         return content
