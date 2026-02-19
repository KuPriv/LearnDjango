import os
import uuid
from django.utils import timezone


def get_timestamp_path(instance, filename):
    ext = filename.split(".")[-1]
    timestamp = timezone.now().strftime("%Y_%m_%d_%H_%M_%S")
    unique_id = uuid.uuid4().hex
    return f"uploads/{timestamp}_{unique_id}.{ext}"
