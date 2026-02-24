from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Bb, Rubric


def post_save_dispatcher(sender, **kwargs):

    if kwargs["created"]:
        print('Объявление в рубрике "%s" создано' % kwargs["instance"].rubric.name)


post_save.connect(post_save_dispatcher, sender=Bb)


@receiver(post_save, sender=Rubric)
def clear_rubric_cache(sender, **kwargs):
    cache.delete("all_rubrics")
