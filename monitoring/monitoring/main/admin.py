from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import BooleanWidget
from .models import Ditina

class DitinaResource(resources.ModelResource):
    imya = fields.Field(attribute='imya', column_name="Ім'я")
    pryimaie_gormony = fields.Field(
        attribute='pryimaie_gormony',
        column_name="Приймає гормони",
        widget=BooleanWidget()
    )

    class Meta:
        model = Ditina
        fields = ('id', 'imya', 'prizvische', 'vik', 'zrist', 'region', 'pryimaie_gormony', 'data_stvorennia')
        export_order = fields



    def before_export(self, queryset, *args, **kwargs):
        for obj in queryset:
            obj.region = obj.get_region_display()

@admin.register(Ditina)
class DitinaAdmin(ImportExportModelAdmin):
    resource_class = DitinaResource
    list_display = ('id', 'imya', 'prizvische', 'vik', 'zrist', 'region', 'pryimaie_gormony')