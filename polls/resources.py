from import_export import resources, fields
from .models import Choice, Factor, Question, Survey
from import_export.widgets import ForeignKeyWidget

class ChoiceResource(resources.ModelResource):
    factor = fields.Field(
        column_name='factor',
        attribute='factor',
        widget=ForeignKeyWidget(Factor, 'factor_name'))#die Daten aus dee Bezugsklasse entnehmen, in diesem Fall aus class Factor
    related_question = fields.Field(
        column_name='related_question',
        attribute='related_question',
        widget=ForeignKeyWidget(Question, 'question_text'))#auch die klasse soll hierein importiert werden
    
    related_survey = fields.Field(
        column_name='related_survey',
        attribute='related_survey',
        widget=ForeignKeyWidget(Survey, 'title'))
    class Meta:
        model = Choice
        # skip_unchanged = True
        # report_skipped = False
        # exclude = ('id',)
        fields = ('id','related_survey','factor','related_question', 'choice_text','votes','score')
        export_order = ('related_survey','factor','related_question', 'choice_text','votes','score')
        import_id_fields = ['id']
    def __str__(self):
        return self.related_question