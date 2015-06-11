__author__ = 'sadaf2605'
from django import template
register = template.Library()
from django.contrib.admin.templatetags import admin_modify

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_line_row(context):
    context = context or {}
    ctx= admin_modify.submit_row(context)

    try:
        print context
        print request.user.group
        if "show_save_as_draft" in context.keys():
            ctx["show_save_as_draft"] = context["show_save_as_draft"]
    except:
        print ""
    ctx["show_save_as_draft"]=True
    return  ctx