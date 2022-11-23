from django.contrib import admin
from .models import PredictModel, TMRTParams, PMVParams, PETParams


class PredictAdmin(admin.ModelAdmin):
    list_display = ['pred_id', 'Global_radiation', 'Surface_temperature', 'Air_temperature', 'Relative_Humidity',
                    'Wind_speed',
                    'Tmrt', 'PMV', 'PET']
    list_filter = ['created', 'updated']


class TMRTAdmin(admin.ModelAdmin):
    list_display = ['vlow', 'low', 'medium', 'high', 'vhigh']


class PMVAdmin(admin.ModelAdmin):
    list_display = ['hot', 'warm', 'slwarm', 'neutral', 'slcool', 'cool', 'cold']


class PETAdmin(admin.ModelAdmin):
    list_display = ['vcold', 'cold', 'cool', 'slcool', 'comfort', 'slwarm', 'warm', 'hot', 'vhot']


admin.site.register(PredictModel, PredictAdmin)
admin.site.register(TMRTParams, TMRTAdmin)
admin.site.register(PMVParams, PMVAdmin)
admin.site.register(PETParams, PETAdmin)
