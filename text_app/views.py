# from django.views import generic
# from .models import TblText

from .models import TblLanguage, TblReason, TblGrade, TblTextType, TblText, TblSentence, TblMarkup, TblTag, TblTokenMarkup, TblToken
from .forms import TextCreationForm, get_annotation_form, SearchTextForm, AssessmentModify, MetaModify
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from copy import deepcopy
from django.db.models import F, Q
from right_app.views import check_permissions_work_with_annotations, check_permissions_show_text, check_permissions_edit_text
from user_app.models import TblTeacher, TblUser, TblStudent
import datetime


# Test

# class TextList(generic.ListView):
#     queryset = TblText.objects
#     template_name = 'corpus.html'

def show_files(request, language = None, text_type = None):
    # Для выбора языка
    if not request.user.is_authenticated:
        return redirect('home')
    elif request.user.is_teacher:
        form_search = SearchTextForm()
        
    # if request.POST['corpus_search']:
        # return redirect(request) 
    
    if language == None:
        try:
            list_language = TblLanguage.objects.all()
            print(list_language)
            return render(request, "corpus.html", context= {'list_language': list_language, 'form_search': form_search})
            
        # except TblLanguage.DoesNotExist:
        # TODO: прописать исключение для каждой ошибки?
        except:
            return(render(request, "corpus.html", context = {'error': True, 'text_html':'<div id = "Text_found_err">404 Not Found<\div>'}))

    # Для выбора типа текста
    elif text_type == None:
        language_object = TblLanguage.objects.filter(language_name=language)
        if len(language_object) == 0:
            return(render(request, "corpus.html", context = {'error': True, 'text_html':'Language not found'}))
        else:
            language_id = language_object.first().id_language
        
        list_text_type = TblTextType.objects.filter(language_id=language_id)
        if len(list_text_type) == 0:
            return(render(request, "corpus.html", context = {'error': True, 'text_html':'Text type not found'}))
        else:
            return(render(request, "corpus.html", context= {'list_text_type': list_text_type, 'form_search': form_search}))
        
    # Для выбора текста
    else:
        language_object = TblLanguage.objects.filter(language_name=language)
        if len(language_object) == 0:
            return(render(request, "corpus.html", context = {'error': True, 'text_html':'Language not found'}))
        else:
            language_id = language_object.first().id_language

        text_type_object = TblTextType.objects.filter(language_id=language_id, text_type_name=text_type)
        if len(text_type_object) == 0:
            return(render(request, "corpus.html", context = {'error': True, 'text_html':'Text type not found'}))
        else:
            text_type_id = text_type_object.first().id_text_type
        
        order_by = ''
        if request.GET:
            order_by = request.GET.get('order_by', 'defaultOrderField')
        if check_permissions_show_text(request.user.id_user):
            if order_by == '':
                list_text = TblText.objects.filter(language_id=language_id, text_type_id=text_type_id)
            else:
                list_text = TblText.objects.filter(language_id=language_id, text_type_id=text_type_id).order_by(order_by)
        else:
            if order_by == '':
                list_text = TblText.objects.filter(language_id=language_id, text_type_id=text_type_id, user_id=request.user.id_user)
            else:
                list_text = TblText.objects.filter(language_id=language_id, text_type_id=text_type_id, user_id=request.user.id_user).order_by(order_by)
            
        list_text_and_user = []
        for text in list_text:
            user = TblUser.objects.filter(id_user=text.user_id).first()
            if user.name == 'empty':
                list_text_and_user.append([text, ''])
            else:
                list_text_and_user.append([text, user.last_name + ' ' + user.name])
            
        return(render(request, "corpus.html", context= {'work_with_file': True, 'list_text_and_user': list_text_and_user, 'language_selected': language, 'form_search': form_search}))
    
    return(render(request, "corpus.html", context = {'text_html':'<div id = "Text_found_err">404 Not Found<\div>'}))
  
def corpus_search(request):
    if request.POST:
        form_search = SearchTextForm(request.POST)
        # Entry.objects.all().filter(pub_date__year=2006)
        filters = Q()
        if form_search.data['header']:
            filters &= Q(header = form_search.data['header'])
        if form_search.data['user']:
            filters &= Q(user_id = form_search.data['user'])
        if form_search.data['language']:
            filters &= Q(language_id = form_search.data['language'])
        if form_search.data['text_type']:
            filters &= Q(text_type_id = form_search.data['text_type'])
        if form_search.data['create_date']:
            filters &= Q(create_date = form_search.data['create_date'])
        if form_search.data['modified_date']:
            filters &= Q(modified_date = form_search.data['modified_date'])
        
        list_text = TblText.objects.filter(filters)
        
    else:
        form_search = SearchTextForm()
        return(render(request, "corpus_search.html", context= {'form_search': form_search}))
        
    return(render(request, "corpus_search.html", context= {'form_search': form_search, 'list_text': list_text}))
  
def new_text(request, language = None, text_type = None):
    
    # Проверка на выбранный язык и тип текста
    if language != None and text_type != None:
        
        language_object = TblLanguage.objects.filter(language_name = language)
        if len(language_object) != 0:
            language_id = language_object[0].id_language
        else:
            return render(request, 'corpus.html')
            
        text_type_objects = TblTextType.objects.filter(language_id = language_id, text_type_name = text_type)
        if len(text_type_objects) == 0:
            return render(request, 'corpus.html')
    else:
        return render(request, 'corpus.html')

    
    if request.method == 'POST':
        from nltk.tokenize import sent_tokenize, word_tokenize
        form_text = TextCreationForm(request.user, language_object[0], text_type_objects[0], data=request.POST)
        
        if form_text.is_valid():
            text = form_text.save()
            count_sent = 0
            for sent in sent_tokenize(text.text):
                sent_object = TblSentence(
                    text_id = text,
                    text = sent,
                    order_number = count_sent
                )
                print(sent_object)
                sent_object.save()
                print(sent_object)
                count_sent += 1
                
                count_token = 0
                for token in word_tokenize(sent):
                    token_object = TblToken(
                        sentence_id = sent_object.id_sentence,
                        text = token,
                        order_number = count_token
                    )
                    token_object.save()
                    
                    count_token += 1

            return redirect('/corpus/' + language + '/' + text_type)
        else:
            # print(form_text.errors)
            pass
            
    else:
        form_text = TextCreationForm(request.user, language_object[0], text_type_objects[0])
        
    return render(request, 'new_text.html', {'form_text': form_text})

def _drop_none(info_dict:dict, ignore:list):
    result = {}
    for key in info_dict.keys():
        if key not in ignore and \
            (info_dict[key] == None or (type(info_dict[key]) == int and info_dict[key] < 0)):
            
            result[key] = 'Не указано'
        else:
            result[key] = info_dict[key]
    return(result)

def _get_text_info(text_id:int):
    '''
    Function for getting meta information

    params:
    text_id (int) -- id of current text

    return:
    dict of metatags 
    '''
    raw_info = TblText.objects.filter(id_text = text_id).values(
        'header',
        'user_id',
        'user_id__name',
        'user_id__last_name',
        'creation_course',
        'create_date',
        'text_type_id__text_type_name',
        'emotional_id__emotional_name',
        'write_tool_id__write_tool_name',
        'write_place_id__write_place_name',
        'education_level',
        'self_rating',
        'student_assesment',
        'assessment',
        'teacher_id__user_id__name',
        'teacher_id__user_id__last_name',
        'pos_check',
        'pos_check_user_id__name',
        'pos_check_user_id__last_name',
        'error_tag_check',
        'error_tag_check_user_id__name',
        'error_tag_check_user_id__last_name'
    ).all()[0]

    group_number = TblStudent.objects.filter(user_id = raw_info['user_id'])\
        .values('group_number')\
            .all()[0]['group_number']

    raw_info = _drop_none(raw_info,['assessment','pos_check','error_tag_check'])
    raw_info['assessment'] = False if not raw_info['assessment']\
         or raw_info['assessment'] < 0 else raw_info['assessment']

    assessment_name = str(raw_info['teacher_id__user_id__name']) + ' ' +\
             str(raw_info['teacher_id__user_id__last_name'])
    assessment_name = 'Не указано' if assessment_name == 'Не указано Не указано' else assessment_name

    pos_name = str(raw_info['pos_check_user_id__name']) + ' ' +\
            str(raw_info['pos_check_user_id__last_name'])
    pos_name = 'Не указано' if pos_name == 'Не указано Не указано' else pos_name

    error_name =  str(raw_info['error_tag_check_user_id__name']) + ' ' +\
            str(raw_info['error_tag_check_user_id__last_name'])
    error_name = 'Не указано' if error_name == 'Не указано Не указано' else error_name

    return({

        # Информация о тексте
        'text_name':raw_info['header'],
        'text_type':raw_info['text_type_id__text_type_name'],
        'course':raw_info['creation_course'],
        'create_date':raw_info['create_date'],
        
        #Информация об авторе

        'author_name':str(raw_info['user_id__name']) + '  ' + str(raw_info['user_id__last_name']),
        'group_number':group_number,

        #Мета. информация
        'emotional':raw_info['emotional_id__emotional_name'],
        'write_tool':raw_info['write_tool_id__write_tool_name'],
        'write_place':raw_info['write_place_id__write_place_name'],
        'education_level':raw_info['education_level'],
        'self_rating':raw_info['self_rating'],
        'student_assessment':raw_info['student_assesment'],

        #Оценка работы
        'assessment': raw_info['assessment'],

        'teacher_name': assessment_name,

        'pos_check':raw_info['pos_check'],
        'pos_check_name': pos_name,

        'error_check':raw_info['error_tag_check'],
        'error_check_name': error_name

    })


#Form for assessments modify proccesing
def assessment_form(request, text_id = 1, **kwargs):
    if check_permissions_work_with_annotations(request.user.id_user, text_id):
    
        initial_values = TblText.objects.filter(id_text = text_id).values(
                'assessment',
                'pos_check',
                'error_tag_check').all()[0]

        if request.method == "POST":
                # instance = get_object_or_404(TblText, id_text = text_id)
                instance = TblText.objects.get(id_text = text_id)
                form = AssessmentModify(initial_values, request.user.is_teacher,
                                request.POST or None, 
                                instance=instance)

                if form.is_valid():
                    assessment = form.cleaned_data['assessment']
                    pos_check = form.cleaned_data['pos_check']
                    error_tag_check = form.cleaned_data['error_tag_check']
        
                    if assessment != initial_values['assessment'] and request.user.is_teacher:
                        teacher_id = TblTeacher.objects.get(user_id = request.user.id_user)
                        print(teacher_id)
                        form.instance.teacher = teacher_id
                    
                    if pos_check != initial_values['pos_check']:
                        form.instance.pos_check_user = TblUser.objects.get(id_user =\
                             request.user.id_user)
                        form.instance.pos_check_date = datetime.date.today()#.strftime('%Y-%M-%d')

                    if error_tag_check != initial_values['error_tag_check']:
                        form.instance.error_tag_check_user = TblUser.objects.get(id_user =\
                             request.user.id_user)
                        form.instance.error_tag_check_date = datetime.date.today()#.strftime('%Y-%M-%d')
                        

                    form.save()
                return(redirect(request.path[:request.path.rfind('/')+1]))
        else:
            form = AssessmentModify(initial_values, request.user.is_teacher)
            return(render(request, 'assessment_form.html', {
                'right':True,
                'form':form
                }))
        
    else:
        return(render(request, 'assessment_form.html', {'right':False}))


#Form for meta modify
def meta_form(request, text_id = 1, **kwargs):
    if  request.user.id_user == TblText.objects\
        .filter(id_text = text_id).values('user_id')[0]['user_id']:
        
        initial_values = TblText.objects.filter(id_text = text_id).values(
                            'emotional',
            'write_tool',
            'write_place',
            'education_level',
            'self_rating',
            'student_assesment').all()[0]

        if request.method == "POST":
            # instance = get_object_or_404(TblText, id_text = text_id)
            instance = TblText.objects.get(id_text = text_id)
            form = MetaModify(initial_values,
                            request.POST or None, 
                            instance=instance)
            
            if form.is_valid():
                form.save()
            return(redirect(request.path[:request.path.rfind('/')+1]))
        else:
            form = MetaModify(initial_values)
            return(render(request, 'meta_form.html', {
                'right':True,
                'form':form
                }))
    else:
        return(render(request, 'meta_form.html', {'right':False}))


def show_text(request, text_id = 1, language = None, text_type = None):
    text_info  = TblText.objects.filter(id_text = text_id).values('header','language_id', 'language_id__language_name', 'user_id').all()
    if text_info.exists() and check_permissions_show_text(request.user.id_user, text_id):
        header = text_info[0]['header']
        text_language_name = text_info[0]['language_id__language_name']
        text_language = text_info[0]['language_id']
        tags = TblTag.objects.filter(tag_language_id = text_language).values('id_tag','tag_text','tag_text_russian', 'tag_parent','tag_color').all()
        tags_info = []
        if tags.exists():
            for element in tags:
                parent_id = 0
                if element['tag_parent']>0:
                    parent_id = element['tag_parent']
                spoiler = False
                for child in tags:
                    if element['id_tag'] == child['tag_parent']:
                        spoiler = True
                        break
                tags_info.append({
                    'isspoiler':spoiler,
                    'tag_id':element['id_tag'],
                    'tag_text':element['tag_text'],
                    'tag_text_russian':element['tag_text_russian'],
                    'parent_id':parent_id,
                    'tag_color':element['tag_color']
                })
        reasons = TblReason.objects.filter(reason_language_id = text_language).values('id_reason','reason_name')
        grades = TblGrade.objects.filter(grade_language_id = text_language).values('id_grade','grade_name')
        annotation_form = get_annotation_form(grades,reasons)

        ann_right = check_permissions_work_with_annotations(request.user.id_user, text_id)
        text_owner = True if request.user.id_user == text_info[0]['user_id'] else False

        text_meta_info = _get_text_info(text_id)

        return render(request, "work_area.html", context= {
            'founded':True,
            'ann_right':ann_right,
            'text_owner':text_owner,
            'user_id':request.user.id_user,
            'annotation_form':annotation_form, 
            'text_id':text_id,
            'lang_name':text_language_name,
            'text_info':text_meta_info
            })
    else:
        return render(request, 'work_area.html', context={'founded':False})
