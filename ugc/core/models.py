# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse as r
from datetime import datetime
import os
from uuid import uuid4
# from south.modelsinspector import add_introspection_rules
# from django_thumbs.db.models import ImageWithThumbsField

# add_introspection_rules(
#     [
#         (
#             (ImageWithThumbsField, ),
#             [],
#             {
#                 "verbose_name": ["verbose_name", {"default": None}],
#                 "name":         ["name",         {"default": None}],
#                 "width_field":  ["width_field",  {"default": None}],
#                 "height_field": ["height_field", {"default": None}],
#                 "sizes":        ["sizes",        {"default": None}],
#             },
#         ),
#     ],
#     ["^django_thumbs\.db\.models\.ImageWithThumbsField",])


class User(models.Model):
    name          = models.CharField(_('Nome'), max_length=100)
    email         = models.EmailField(_('Email'), max_length=100, blank=True, null=True)
    created_at    = models.DateTimeField(_('Criado em'), auto_now_add=True)
    image_url     = models.CharField(_('Avatar caminho'), max_length=100, blank=True)
    # Twitter
    twitter_user  = models.CharField(_('Twitter username'), max_length=50, blank=True, null=True)
    twitter_id    = models.CharField(_('Twitter ID'), max_length=100, blank=True, null=True)
    twitter_token = models.TextField(_('Twitter Token'), blank=True, null=True)
    # facebook
    facebook_user  = models.CharField(_('Facebook username'), max_length=50, blank=True, null=True)
    facebook_id    = models.CharField(_('Facebook ID'), max_length=100, blank=True, null=True)
    facebook_token = models.TextField(_('Facebook Token'), blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')
        unique_together = ('name', 'twitter_id', 'facebook_id')

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

    def update_block(self):
        self.quant_blocks += 1
        if self.quant_blocks >= 3:
            self.status = False
        self.save()

    @property
    def user_name(self):
        """
        Property created by used in /api/publishs/
        """
        return self.user.name

    @property
    def thumbs(self):
        medias = self.media_set.all()
        if not medias:
            return medias
        return map(lambda w: w.thumbnail.url, medias)

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



def path_and_rename(thumb=False):
    def wrapper(instance, filename):
        ext = 'png'
        if not thumb:
            filename = '{}.{}'.format(uuid4().hex, ext)
        else:
            filename = '{}_thumbnail.{}'.format(uuid4().hex, ext)
        path = 'publishs/{}/'.format(datetime.today().strftime("%Y/%m/%d"))
        return os.path.join(path, filename)
    return wrapper

class Media(models.Model):
    # image = ImageWithThumbsField(upload_to=path_and_rename(), max_length=100, default='', sizes=((126,91)))
    image = models.ImageField(upload_to=path_and_rename(), max_length=100, default='')
    thumbnail = models.ImageField(upload_to=path_and_rename(True), max_length=100, default='')
    publish = models.ForeignKey('Publish', verbose_name=_(u'Publicação'), default=2)

    class Meta:
        verbose_name = _(u'Arquivo')
        verbose_name_plural = _(u'Arquivos')

    def thumb_url(self):
        return self.thumbnail.url
    
    def __unicode__(self):
        return self.image.url

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
 
        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return
 
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (126,91)
 
        DJANGO_TYPE = self.image.file.content_type
 
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
 
        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))
 
        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        #
        # I commented this part since it messes up my png files
        #
        #if image.mode not in ('L', 'RGB'):
        #    image = image.convert('RGB')
 
        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
 
        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
 
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
 
    def save(self):
        # create a thumbnail
        self.create_thumbnail()
 
        super(Media, self).save()