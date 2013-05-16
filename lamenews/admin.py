from lamenews import models

from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'creator',
        'create_date',
    )
    filter_horizontal = (
        'tags',
    )

class TagAdmin(admin.ModelAdmin):
    pass

class VotesAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Votes, VotesAdmin)