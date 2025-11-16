# Generated migration for adding trigram indexes to improve search performance

from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20181121_0402'),
    ]

    operations = [
        # Enable the pg_trgm extension for trigram similarity searches
        TrigramExtension(),

        # Add trigram index on DocumentVersion.name for fast partial matching
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS document_version_name_trgm_idx ON kala_document_version USING gin (name gin_trgm_ops);",
            reverse_sql="DROP INDEX IF EXISTS document_version_name_trgm_idx;"
        ),

        # Add trigram index on DocumentVersion.description for fast partial matching
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS document_version_description_trgm_idx ON kala_document_version USING gin (description gin_trgm_ops);",
            reverse_sql="DROP INDEX IF EXISTS document_version_description_trgm_idx;"
        ),

        # Add trigram index on Document.name for fast partial matching
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS document_name_trgm_idx ON kala_documents USING gin (name gin_trgm_ops);",
            reverse_sql="DROP INDEX IF EXISTS document_name_trgm_idx;"
        ),
    ]
