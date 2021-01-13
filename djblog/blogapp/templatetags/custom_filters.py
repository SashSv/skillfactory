from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    value = value
    bad_words = ['бля','Бля','Жопа','жопа']

    for word in bad_words:
        stars = '*' * len(word)
        value = value.replace(word, stars)

    return value