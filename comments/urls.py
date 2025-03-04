from django.urls import path
from .views import CommentCreateView, CommentUpdateView,CommentDeleteView,CommentListView


urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='comment-create'),
    path('update/', CommentUpdateView.as_view(), name='comment-update'),
    path('delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('list/', CommentListView.as_view(), name='comment-list'),
]

