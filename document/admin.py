from worry.document.models import Document, Comment
from django.contrib import admin


class DocumentAdmin(admin.ModelAdmin) :
	list_display = ('title',  'category', 'category_name', 'module_id', 'module_name', 'format_date')
	search_fields = ['title', 'content']
	


	def format_date(self, obj):
		return obj.pub_date.strftime('%d %b %Y %H:%M')
	format_date.short_description = 'Date'
	format_date.admin_order_field = 'date'

class DocumentShopAdmin(DocumentAdmin) :
	def queryset(self, request):
		qs = super(DocumentShopAdmin, self).queryset(request)
		return qs.filter(category='2')

class DocumentWorryBoardAdmin(DocumentAdmin) :
	actions = ['move_to_shop']
	def move_to_shop(self, request, queryset) :
		rows_updated = queryset.update(category='2', category_name='shop')
		if rows_updated == 1:
			message_bit = "1 document was"
		else:
			message_bit = "%s documents were" % rows_updated
		self.message_user(request, "%s successfully updated as shop category." % message_bit)
	move_to_shop.short_description = "Move document to shop category"

	def queryset(self, request):
		qs = super(DocumentWorryBoardAdmin, self).queryset(request)
		return qs.filter(category='1')

class Shop(Document):
	class Meta:
		proxy = True

class WorryBoard(Document) :
	class Meta :
		proxy = True


admin.site.register(Document, DocumentAdmin)
admin.site.register(Shop, DocumentShopAdmin)
admin.site.register(WorryBoard, DocumentWorryBoardAdmin)
admin.site.register(Comment)
# admin.site.register(File)
