from django.contrib import admin

# Register your models here.
from carts_app.models import *
# admin.site.register(Role)
# admin.site.register(User)
admin.site.register(Item)
# admin.site.register(Cart)
admin.site.register(RoleMapping)
class RoleAdmin(admin.ModelAdmin):
	list_display = ['role_id','role_name']
admin.site.register(Role,RoleAdmin)

class UserAdmin(admin.ModelAdmin):
	list_display = ['user_id','full_name','user_name','password','session_token','exp_date']
admin.site.register(User,UserAdmin)

class CartAdmin(admin.ModelAdmin):
	list_display = ['user_id','item_id','cart_date']
admin.site.register(Cart,CartAdmin)