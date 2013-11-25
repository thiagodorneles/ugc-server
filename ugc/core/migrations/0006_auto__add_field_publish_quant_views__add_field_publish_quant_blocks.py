# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Publish.quant_views'
        db.add_column(u'core_publish', 'quant_views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Publish.quant_blocks'
        db.add_column(u'core_publish', 'quant_blocks',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Publish.quant_views'
        db.delete_column(u'core_publish', 'quant_views')

        # Deleting field 'Publish.quant_blocks'
        db.delete_column(u'core_publish', 'quant_blocks')


    models = {
        u'core.publish': {
            'Meta': {'ordering': "['-created_at']", 'unique_together': "(('title', 'description'),)", 'object_name': 'Publish'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'quant_blocks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quant_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'publish'", 'symmetrical': 'False', 'to': u"orm['core.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['core']