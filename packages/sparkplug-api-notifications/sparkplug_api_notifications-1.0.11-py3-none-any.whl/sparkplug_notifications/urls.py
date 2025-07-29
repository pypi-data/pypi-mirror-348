from django.urls import path

from . import views

urlpatterns = [
    path(
        "mark-read/",
        views.MarkReadView.as_view(),
        name="notifications-mark-read",
    ),
    path(
        "<str:uuid>/set-star/",
        views.SetStarView.as_view(),
        name="notifications-set-star",
    ),
    path(
        "unread-count/",
        views.UnreadCountView.as_view(),
        name="notifications-unread-count",
    ),
    path(
        "",
        views.ListView.as_view(),
        name="notifications-list",
    ),
]
