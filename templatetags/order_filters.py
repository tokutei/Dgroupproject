from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """指定されたキーで辞書から値を取得"""
    return dictionary.get(key)
