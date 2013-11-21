# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Publish', fields ['description', 'title']
        db.create_unique(u'core_publish', ['description', 'title'])


    def backwards(self, orm):
        # Removing unique constraint on 'Publish', fields ['description', 'title']
        db.delete_unique(u'core_publish', ['description', 'title'])


    models = {
        u'core.publish': {
            'Meta': {'ordering': "['-created_at']", 'unique_together': "(('title', 'description'),)", 'object_name': 'Publish'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']