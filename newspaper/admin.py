from django.contrib import admin

from newspaper.models import Comment, Post,Category,Tag,Contact,Newsletter
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Newsletter)
admin.site.register(Comment)

