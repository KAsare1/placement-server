from django.contrib import admin
from .models import Program, Choice, Results, ConsiderationRequest, Placement
from django.core.exceptions import ValidationError
import csv
from django.http import HttpResponse

def export_choices_to_csv(modeladmin, request, queryset):
    """
    Exports selected Choice model data to CSV
    """
    # Set the HTTP response with CSV format
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="choices_data.csv"'

    writer = csv.writer(response)

    # Write the headers for the CSV file
    writer.writerow(['Student', 'email', 'First Choice', 'Second Choice', 'Third Choice'])  # Adjust these as needed

    # Write the data rows
    for obj in queryset:
        writer.writerow([obj.student, obj.email, obj.first_choice, obj.second_choice, obj.third_choice])

    return response

export_choices_to_csv.short_description = "Export Selected Choices to CSV"

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_type', 'major', 'second_major', 'minor', 'program')

    def save_model(self, request, obj, form, change):
        try:
            print(f"Attempting to save Program - Type: {obj.program_type}, Major: {obj.major}, Second Major: {obj.second_major}, Minor: {obj.minor}")
            obj.save()
            self.message_user(request, "Program saved successfully.")
        except ValidationError as e:
            self.message_user(request, f"Validation error: {str(e)}", level='ERROR')
        except Exception as e:
            self.message_user(request, f"Error saving Program: {str(e)}", level='ERROR')
            print(f"Exception details: {type(e).__name__} - {str(e)}")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['program_type'].widget.attrs['onchange'] = 'updateFieldVisibility(this.value);'
        return form

    class Media:
        js = ('js/program_admin.js',)

# Keep your other admin registrations as they are
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'email','first_choice', 'second_choice', 'third_choice')
    actions = [export_choices_to_csv]

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('student', 'students_id', 'results', 'CGPA')

@admin.register(ConsiderationRequest)
class ConsiderationRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'Results', 'CGPA', 'choice', 'explanation')

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'placement')



