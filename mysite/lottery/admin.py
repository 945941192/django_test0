from django.contrib import admin

# Register your models here.


# from django.contrib import admin
# from django import forms
# from django.utils.html import format_html_join
# from django.utils.safestring import mark_safe
# from django.core import urlresolvers
import lottery.models as m






admin.site.register(m.Item)
admin.site.register(m.Person)