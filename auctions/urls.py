from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_items, name="category_items"),
    path("listings/<int:listing_id>", views.listing_page, name="listing_page"),
    path("user-watchlist-add", views.user_watchlist_add, name="user-watchlist-add"),
    path("user-watchlist-rm", views.user_watchlist_rm, name="user-watchlist-rm"),
    path("new_bid", views.new_bid, name="new_bid"),
]
