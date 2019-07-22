from django.contrib import admin
from .models import *

class CardControlDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ('cc_id', )


# Register your models here.

admin.site.register(CardControlDetail, CardControlDetailsAdmin)
admin.site.register(CardDetail)
admin.site.register(TransactionDetail)
