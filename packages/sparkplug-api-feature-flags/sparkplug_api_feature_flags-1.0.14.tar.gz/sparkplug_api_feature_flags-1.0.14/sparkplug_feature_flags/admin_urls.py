from django.urls import include, path

from .views import admin as views

uuid_patterns = [
    path(
        "give-access/",
        views.GiveAccessView.as_view(),
        name="feature-flags-give-access",
    ),
    path(
        "remove-access/",
        views.RemoveAccessView.as_view(),
        name="feature-flags-remove-access",
    ),
    path(
        "set-enabled/",
        views.SetEnabledView.as_view(),
        name="feature-flags-set-enabled",
    ),
    path(
        "",
        views.DetailView.as_view(),
        name="feature-flags-detail",
    ),
]

urlpatterns = [
    path(
        "autocomplete/",
        views.AutocompleteView.as_view(),
        name="feature-flags-autocomplete",
    ),
    path(
        "search/",
        views.SearchView.as_view(),
        name="feature-flags-search",
    ),
    path(
        "<str:uuid>/",
        include(uuid_patterns),
    ),
    path(
        "",
        views.ListView.as_view(),
        name="feature-flags-list",
    ),
]
