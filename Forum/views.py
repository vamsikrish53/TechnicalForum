from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import F
from django.db.utils import IntegrityError
from .models import *


# Create your views here.

def index_page(request):
    return render(request, template_name="Forum/index.html")


def signup(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, email, password)
            context_message = {"default_message": "Account succussfully created. You can Login now."}
            user.save()
        except IntegrityError:
            context_message = {"default_message": username + " is already used. Please try with other."}
    else:
        context_message = {"default_message": "Invalid request. Try again."}
    return render(request, template_name="Forum/index.html", context=context_message)


def login_validation(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/home_page')
    else:
        context_message = {"default_message": "Invalid login. Username and password are not matched."}
        return render(request, template_name="Forum/index.html", context=context_message)


def logout_validation(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home_page(request):
    questions_list_objects = Question.objects.filter().order_by('-active')
    if questions_list_objects:
        context_message = {"questions_list": questions_list_objects}
    else:
        context_message = {}
    return render(request, template_name="Forum/home_page.html", context=context_message)


@login_required
def ask_question_page(request):
    return render(request, template_name="Forum/ask_question.html")


@login_required
def add_new_question(request):
    # save new question
    new_question_title = request.GET.get('question_title')
    new_question_description = request.GET.get('question_description')
    new_questioned_by = request.user
    new_question = Question(question_title=new_question_title, question_description=new_question_description,
                            questioned_by=new_questioned_by)
    new_question.save()

    # link tags to question
    question_tags = request.GET.get('question_tags')
    tag_list = list(set(question_tags.split(' ')))
    for new_tag_name in tag_list:
        # add tag to Tag Table if it is new one
        new_tag = Tag(tag_name=new_tag_name)
        new_tag.save()

        # save tag and question link
        new_tag_question_link = Tag_Question_Link(question_link=new_question, tag_link=new_tag)
        new_tag_question_link.save()

    # return redirct link to homepage
    return HttpResponseRedirect('/home_page')


def search(request):
    search_tag = request.GET.get('search')
    tag_ids = Tag.objects.filter(tag_name=search_tag)
    questions_list_objects = []
    for tag_id in tag_ids:
        link_details = Tag_Question_Link.objects.get(tag_link_id=tag_id)
        questions_list_objects.append(Question.objects.get(id=link_details.question_link_id))

    if questions_list_objects:
        context_message = {"questions_list": questions_list_objects}
    else:
        context_message = {}
    return render(request, template_name="Forum/home_page.html", context=context_message)


def view_question(request, pk):
    # fetch question details
    question_details = Question.objects.get(id=pk)
    question_details = model_to_dict(question_details)
    # fetch comments of question
    comments = Comment.objects.filter(commented_to_question_id=question_details["id"]).values()
    if len(comments) != 0:
        for comment in comments:
            comment.update({"commented_by": User.objects.get(id=comment["commented_by_id"])})
        question_details.update({"comments": comments})

    # fetch user details
    user_details = User.objects.get(id=question_details["questioned_by"])

    # fetch tag details
    tag_details = []
    tag_ids_related_to_question = Tag_Question_Link.objects.filter(question_link=pk).values('tag_link')
    for tag in tag_ids_related_to_question:
        tag_details += Tag.objects.filter(id=tag["tag_link"])

    # fetch answer details
    answers_list = Answer.objects.filter(answered_to=pk).values()
    for answer in answers_list:
        answer.update({"answered_by": User.objects.get(id=answer["answered_by_id"])})
        # fetch comments of answers
        comments = Comment.objects.filter(commented_to_answer_id=answer["id"]).values()
        if len(comments) != 0:
            for comment in comments:
                comment.update({"commented_by": User.objects.get(id=comment["commented_by_id"])})
            answer.update({"comments": comments})

    # get login user details
    current_user_id = request.user.id

    # return responce
    context_message = {"question_details": question_details, "answers_list": answers_list, "user_details": user_details,
                       "tag_details": tag_details, "current_user_id": current_user_id}
    return render(request, template_name="Forum/view_question.html", context=context_message)


def add_answer(request, pk):
    # save new answer
    question_details = Question.objects.get(id=pk)
    new_answer_description = request.GET.get('answer_description')
    new_answered_by = request.user
    new_answer = Answer(answer_description=new_answer_description, answered_by=new_answered_by,
                        answered_to=question_details)
    new_answer.save()

    # update question details
    question_details = Question.objects.get(id=pk)
    answer_count = question_details.answer_count
    question_details = Question.objects.filter(id=pk)
    question_details.update(answer_count=answer_count + 1)
    question_details = Question.objects.get(id=new_answer.answered_to_id)
    question_details.save()

    # return question_page
    return HttpResponseRedirect('/home_page/view_question/' + pk)


def post_comment_to_answer(request, pk):
    # save new comment
    new_comment_to = Answer.objects.get(id=pk)
    new_comment_description = request.GET.get('comment')
    new_comment_by = request.user
    new_comment = Comment(comment_description=new_comment_description, commented_by=new_comment_by,
                          commented_to_answer=new_comment_to)
    new_comment.save()

    # update question details
    question_details = Question.objects.get(id=new_comment_to.answered_to_id)
    question_details.save()

    # return question page
    return HttpResponseRedirect('/home_page/view_question/' + str(new_comment_to.answered_to.id))


def post_comment_to_question(request, pk):
    # save new comment
    new_comment_to = Question.objects.get(id=pk)
    new_comment_description = request.GET.get('comment')
    new_comment_by = request.user
    new_comment = Comment(comment_description=new_comment_description, commented_by=new_comment_by,
                          commented_to_question=new_comment_to)
    new_comment.save()

    # update question details
    question_details = Question.objects.get(id=new_comment_to.id)
    question_details.save()

    # return question page
    return HttpResponseRedirect('/home_page/view_question/' + str(new_comment_to.id))


def tag_questions(request, pk):
    tag_details = Tag.objects.get(id=pk)
    tag_ids = Tag.objects.filter(tag_name=tag_details.tag_name)
    questions_list_objects = []
    for tag_id in tag_ids:
        link_details = Tag_Question_Link.objects.get(tag_link_id=tag_id)
        questions_list_objects.append(Question.objects.get(id=link_details.question_link_id))

    if questions_list_objects:
        context_message = {"questions_list": questions_list_objects}
    else:
        context_message = {}
    return render(request, template_name="Forum/home_page.html", context=context_message)


def view_tags(request):
    tag_details = Tag.objects.all()
    if tag_details:
        context_message = {"tag_details": tag_details}
    else:
        context_message = {}
    return render(request, template_name="Forum/view_tags.html", context=context_message)


def delete_question(request, pk):
    question_details = Question.objects.get(id=pk)
    related_answers = Answer.objects.filter(answered_to_id=question_details.id)

    # delete related comments
    for answer in related_answers:
        Comment.objects.filter(commented_to_answer_id=answer.id).delete()

    # delete related answers
    related_answers.delete()

    # delete related tags
    link_details = Tag_Question_Link.objects.filter(question_link_id=question_details.id)
    for link in link_details:
        Tag.objects.get(id=link.tag_link_id).delete()
    link_details.delete()

    # delete question
    Question.objects.get(id=pk).delete()

    return HttpResponseRedirect("/home_page")


def delete_answer(request, pk):
    # get answer details
    answer_details = Answer.objects.get(id=pk)

    # update question details
    question_details = Question.objects.get(id=answer_details.answered_to_id)
    answer_count = question_details.answer_count
    question_details = Question.objects.filter(id=answer_details.answered_to_id)
    question_details.update(answer_count=answer_count - 1)
    question_details = Question.objects.get(id=answer_details.answered_to_id)
    question_details.save()

    # delete comments
    Comment.objects.filter(commented_to_answer_id=answer_details.id).delete()

    # delete answer
    answer_details.delete()

    return HttpResponseRedirect("/home_page/view_question/" + str(question_details.id))


def update_question(request, pk):
    question_details = Question.objects.get(id=pk)
    question_details = model_to_dict(question_details)

    # fetch tag details
    tag_details = []
    tag_ids_related_to_question = Tag_Question_Link.objects.filter(question_link=pk).values('tag_link')
    for tag in tag_ids_related_to_question:
        tag_details += Tag.objects.filter(id=tag["tag_link"])
    question_tags = " ".join([tag.tag_name for tag in tag_details])

    question_details.update({"question_tags": question_tags})
    context_message = {"question_details": question_details}
    return render(request, template_name="Forum/update_question.html", context=context_message)


def update_answer(request, pk):
    answer_details = Answer.objects.get(id=pk)
    context_message = {"answer_details": answer_details}
    return render(request, template_name="Forum/update_answer.html", context=context_message)


def update_question_in_database(request, pk):
    # save update question
    question_title = request.GET.get('question_title')
    new_question_description = request.GET.get('question_description')
    question_data = Question.objects.get(id=pk)

    question_data.question_title = question_title
    question_data.question_description = new_question_description
    question_data.save()

    # remove old links
    link_details = Tag_Question_Link.objects.filter(question_link_id=question_data.id)
    for link in link_details:
        Tag.objects.get(id=link.tag_link_id).delete()
    link_details.delete()

    # link tags to question
    question_tags = request.GET.get('question_tags')
    tag_list = list(set(question_tags.split(' ')))
    for new_tag_name in tag_list:
        # add tag to Tag Table if it is new one
        new_tag = Tag(tag_name=new_tag_name)
        new_tag.save()

        # save tag and question link
        new_tag_question_link = Tag_Question_Link(question_link=question_data, tag_link=new_tag)
        new_tag_question_link.save()

    # return redirct link to homepage
    return HttpResponseRedirect('/home_page/view_question/' + pk)


def update_answer_in_database(request, pk):
    # update answer data
    new_answer_description = request.GET.get('answer_description')
    answer_data = Answer.objects.get(id=pk)
    answer_data.answer_description = new_answer_description
    answer_data.save()

    # refresh questions
    question_details = Question.objects.get(id=answer_data.answered_to_id)
    question_details.save()

    # redirct link
    return HttpResponseRedirect('/home_page/view_question/' + str(answer_data.answered_to_id))


def sort_by_active(request):
    questions_list_objects = Question.objects.filter().order_by('-active')
    if questions_list_objects:
        context_message = {"questions_list": questions_list_objects}
    else:
        context_message = {}
    return render(request, template_name="Forum/home_page.html", context=context_message)


def sort_by_voice(request):
    questions_list_objects = Question.objects.filter().order_by('-answer_count')
    if questions_list_objects:
        context_message = {"questions_list": questions_list_objects}
    else:
        context_message = {}
    return render(request, template_name="Forum/home_page.html", context=context_message)