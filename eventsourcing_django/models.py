# -*- coding: utf-8 -*-
import os

from django.db import models

def prefix_db_table(name: str) -> str:
    prefix = os.getenv("DJANGO_EVENTSOURCING_TABLES_PREFIX", None)
    if prefix is None: return name
    return f"{prefix.lower().rstrip('_')}_{name}"

class StoredEventRecord(models.Model):

    id = models.BigAutoField(primary_key=True)

    # Application name.
    application_name = models.CharField(max_length=32)

    # Originator ID (e.g. an entity or aggregate ID).
    originator_id = models.UUIDField()

    # Position (index) of item in sequence.
    originator_version = models.BigIntegerField()

    # Topic of the item (e.g. path to domain event class).
    topic = models.TextField()

    # State of the item (serialized dict, possibly encrypted).
    state = models.BinaryField()

    class Meta:
        unique_together = (
            ("application_name", "originator_id", "originator_version"),
            ("application_name", "id"),
        )
        db_table = prefix_db_table("stored_events")


class SnapshotRecord(models.Model):

    uid = models.BigAutoField(primary_key=True)

    # Application name.
    application_name = models.CharField(max_length=32)

    # Originator ID (e.g. an entity or aggregate ID).
    originator_id = models.UUIDField()

    # Position (index) of item in sequence.
    originator_version = models.BigIntegerField()

    # Topic of the item (e.g. path to domain event class).
    topic = models.TextField()

    # State of the item (serialized dict, possibly encrypted).
    state = models.BinaryField()

    class Meta:
        unique_together = (("application_name", "originator_id", "originator_version"),)
        db_table = prefix_db_table("snapshots")


class NotificationTrackingRecord(models.Model):

    uid = models.BigAutoField(primary_key=True)

    # Application name.
    application_name = models.CharField(max_length=32)

    # Upstream application name.
    upstream_application_name = models.CharField(max_length=32)

    # Notification ID.
    notification_id = models.BigIntegerField()

    class Meta:
        unique_together = (
            (
                "application_name",
                "upstream_application_name",
                "notification_id",
            ),
        )
        db_table = prefix_db_table("notification_tracking")
