from django.contrib import admin

from company_app.models import Company, HrManager, FavoriteResume, Card, Vacancy, Offer

admin.site.register(Company)
admin.site.register(HrManager)
admin.site.register(FavoriteResume)
admin.site.register(Card)
admin.site.register(Vacancy)
admin.site.register(Offer)