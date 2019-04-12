from django.contrib import admin
from .models import Property, Property_Sector, Province, Property_Facing, Property_Category, PropertyImages, Country, Password, \
    City, User, UserRole, RolePermission, Role, Permission, PropertyCategoryChoice, PropertySectorChoice, \
    PropertyFacingChoice

# Register your models here.
admin.site.register(User)
admin.site.register(Password)
admin.site.register(Property)
admin.site.register(Property_Category)
admin.site.register(Property_Sector)
admin.site.register(Property_Facing)
admin.site.register(PropertyImages)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(UserRole)
admin.site.register(RolePermission)
admin.site.register(Role)
admin.site.register(Permission)

