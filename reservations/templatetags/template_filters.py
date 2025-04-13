from django import template

register = template.Library()

@register.filter()
def card_background(level):
    if level == 'expert':
        return 'background-color: rgba(33, 150, 250, 0.6);'
    elif level == 'intermediate':
        return 'background-color: rgba(54, 170, 165, 0.6);'
    elif level == 'begginer':
        return 'background-color: rgba(76, 200, 80, 0.6);'
    else:
        return 'background-color: white;'
    

def print_date(date):
    pass
        