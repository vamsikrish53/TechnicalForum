from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index_page, name="index_page"),
    url(r'^signup/$', views.signup),
    url(r'^login_validation/$', views.login_validation),
    url(r'^home_page/$', views.home_page,name="home_page"),
    url(r'^home_page/ask_question/$', views.ask_question_page,name="ask_question_page"),
    url(r'^home_page/ask_question/add_question$', views.add_new_question),
    url(r'^home_page/search', views.search),
    url(r'^home_page/view_question/(?P<pk>[0-9]+)/$', views.view_question),
    url(r'^home_page/post_answer/(?P<pk>[0-9]+)/add_answer/$', views.add_answer),
    url(r'^home_page/post_comment_to_answer/(?P<pk>[0-9]+)/$', views.post_comment_to_answer),
    url(r'^home_page/post_comment_to_question/(?P<pk>[0-9]+)/$', views.post_comment_to_question),
    url(r'^home_page/tag/(?P<pk>[0-9]+)/$', views.tag_questions),
    url(r'^home_page/view_tags/$', views.view_tags),
    url(r'^home_page/delete_question/(?P<pk>[0-9]+)/$', views.delete_question),
    url(r'^home_page/delete_answer/(?P<pk>[0-9]+)/$', views.delete_answer),
    url(r'^home_page/update_question/(?P<pk>[0-9]+)/$', views.update_question),
    url(r'^home_page/update_answer/(?P<pk>[0-9]+)/$', views.update_answer),
    url(r'^home_page/update_question/(?P<pk>[0-9]+)/add_question/$', views.update_question_in_database),
    url(r'^home_page/update_answer/(?P<pk>[0-9]+)/add_answer/$', views.update_answer_in_database),
    url(r'^home_page/sortby/active/$', views.sort_by_active),
    url(r'^home_page/sortby/voice/$', views.sort_by_voice),
    url(r'^logout$', views.logout_validation)
]