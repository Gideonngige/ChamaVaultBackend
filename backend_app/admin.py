from django.contrib import admin
from . models import Chamas, Members, Contributions, Loans, Notifications

# Register your models here.
admin.site.register(Chamas)
admin.site.register(Members)
admin.site.register(Contributions)
admin.site.register(Loans)
admin.site.register(Notifications)