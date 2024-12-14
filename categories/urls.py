from django.urls import path

from .views import (  # User Endpoints; Admin Endpoints
    AdminCategoryDetailView,
    AdminCategoryListCreateView,
    CategoryDetailView,
    CategoryListView,
)

urlpatterns = [
    # User Endpoints (Categories)
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    # Admin Endpoints (Categories)
    path(
        "admin/categories/",
        AdminCategoryListCreateView.as_view(),
        name="admin-category-list-create",
    ),
    path(
        "admin/categories/<int:pk>/",
        AdminCategoryDetailView.as_view(),
        name="admin-category-detail",
    ),
]