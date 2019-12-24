from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from wallet import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserLanguages)
admin.site.register(models.Balance)
admin.site.register(models.Account)
admin.site.register(models.Trade)
admin.site.register(models.Transaction)
admin.site.register(models.CreditCard)
admin.site.register(models.ProofTransactionSlip)
admin.site.register(models.Ticket)
