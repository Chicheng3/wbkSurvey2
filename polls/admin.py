from django.contrib import admin
from polls.resources import ChoiceResource
from .models import Choice, Factor, Question, Survey,User
from . import models
from import_export.admin import ExportMixin, ImportExportModelAdmin
from django.apps import apps


"""
ermöglicht die benutzerdefinierte Reihenfolge der Seitenmenü
"""
"""
from django.contrib import admin  
from django.utils.text import capfirst  
from collections import OrderedDict as SortedDict
  
def find_model_index(name):  
    count = 0  
    for model, model_admin in admin.site._registry.items():  
        if capfirst(model._meta.verbose_name_plural) == name:  
            return count  
        else:  
            count += 1  
    return count  
          
def index_decorator(func):  
    def inner(*args, **kwargs):  
        templateresponse = func(*args, **kwargs)  
        for app in templateresponse.context_data['app_list']:  
            app['models'].sort(key=lambda x: find_model_index(x['name']))  
        return templateresponse  
    return inner  
  
registry = SortedDict()  
registry.update(admin.site._registry)  
admin.site._registry = registry  
admin.site.index = index_decorator(admin.site.index)  
admin.site.app_index = index_decorator(admin.site.app_index)  

# 指定导航顺序
apps_index = ["Factor", "Survey", "Question", "Choice", "User"]


def find_app_index(app_label):
    app = apps.get_app_config(app_label)
    main_menu_index = getattr(app, 'main_menu_index', 9999)
    return main_menu_index


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        app_list = templateresponse.context_data['app_list']
        app_list.sort(key=lambda r: find_app_index(r['app_label']))
        print("app_list:", app_list)
        for app in app_list:
            if app["app_label"] == "polls":
                # 按照指定顺序排序
                models = app["models"]
                new_models = []
                for i in models:
                    model_name = i["object_name"]
                    pos = apps_index.index(model_name)
                    new_models.append({"pos": pos, "model": i})
                new_models.sort(key=lambda s: s["pos"])
                # app['models'].sort(key=lambda x: find_model_index(x['name']))
                models = [x["model"] for x in new_models]
                app["models"] = models
                print("models:", models)
        return templateresponse

    return inner

"""

'''admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)'''


admin.site.site_header = "wbkSurvey Management"
admin.site.site_title = 'wbkSurvey Management'
admin.site.index_title = 'wbkSurvey Management'

"""
Darstellung vom User Modell in Django Admin
"""
admin.site.register(models.Factor)
admin.site.register(models.Dimension)
"""
Erweiterung der Question um Choice Felder
"""

class ChoiceInline(admin.TabularInline):
     model=Choice
     extra=4

"""
Erweiterung der Survey um Question Felder
"""

class QuestionInline(admin.TabularInline):
    model=Question
    extra=4

"""
Darstellung vom Survey Modell in Django Admin
"""

class SurveyAdmin(admin.ModelAdmin):
    fields= ['title','pub_date','impl_level','factor','showing']
    list_display = ('title','pub_date')
    inlines = [QuestionInline]
admin.site.register(Survey, SurveyAdmin)

"""
Darstellung vom Question Modell in Django Admin
"""
class QuestionAdmin(admin.ModelAdmin):
    
    fields= ['question_text','related_survey','factor','impl_level','pub_date'] #Eingabenfelder für Question in Django Admin
    search_fields = ['question_text','factor']
    list_display = ('question_text','related_survey','factor','impl_level','pub_date','get_vote_count') #Ansicht zur Question in der Datenbank
    list_filter= ['factor','impl_level', 'related_survey']
    inlines = [ChoiceInline]
    raw_id_fields =['related_survey']

admin.site.register(Question, QuestionAdmin)



"""
Darstellung vom Choice Modell in Django Admin
"""
class ChoiceAdmin(ImportExportModelAdmin):
# class ChoiceAdmin(ExportMixin, admin.ModelAdmin):#export only
    fields= ['related_survey','choice_text','related_question','score','factor', 'stellengröße'] 
    list_display = ('choice_text','related_survey','related_question','votes','score','factor', 'stellengröße')  
    list_filter = ['factor','related_survey']
    #autocomplete_fields = ['factor']

    resource_class = ChoiceResource
    def has_add_permission(self, request): #versteckt die Hinzufügen Taste
        return False
admin.site.register(Choice, ChoiceAdmin)


"""
Darstellung vom User Modell in Django Admin
"""
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'occupation', 'email', 'message', 'pub_date')
    def has_add_permission(self, request): #versteckt die Hinzufügen Taste
        return False
admin.site.register(User, UserAdmin)



