import random
from django import template

register = template.Library()


@register.filter('rand_select_giffy_url')
def shuffle_giffys(giffy_list):
    random_index = random.randint(0, len(giffy_list) - 1)
    return giffy_list[random_index]
