# -*- coding: utf-8 -*-

from django import template


register=template.Library()



@register.filter(name='rightunderscore')
def rightunderscore(value):
    truncd = value.split("_")
    first=1
    res=''
    for i in truncd:
        if first:
            first=0
        else:
            res=res+"_"+str(i)

    return res
rightunderscore.isSafe=True


