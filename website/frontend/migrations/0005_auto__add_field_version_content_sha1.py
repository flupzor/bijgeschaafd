# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Version.content_sha1'
        db.add_column('version', 'content_sha1',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Version.content_sha1'
        db.delete_column('version', 'content_sha1')


    models = {
        u'frontend.article': {
            'Meta': {'object_name': 'Article', 'db_table': "'Articles'"},
            'git_dir': ('django.db.models.fields.CharField', [], {'default': "'old'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_check': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1901, 1, 1, 0, 0)'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1901, 1, 1, 0, 0)'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'frontend.upvote': {
            'Meta': {'object_name': 'Upvote', 'db_table': "'upvotes'"},
            'article_id': ('django.db.models.fields.IntegerField', [], {}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'diff_v1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'diff_v2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upvoter_ip': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'frontend.version': {
            'Meta': {'object_name': 'Version', 'db_table': "'version'"},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['frontend.Article']"}),
            'boring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'content_sha1': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'diff_json': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'v': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['frontend']