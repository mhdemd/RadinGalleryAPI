from django.urls import path

from .views import (
    AdminReviewApprovalView,
    AdminReviewListView,
    CommentCreateView,
    CommentListView,
    ReviewCreateView,
    ReviewListView,
    ReviewUpdateDeleteView,
    ReviewVoteView,
    reviews_schema_view,
)

urlpatterns = [
    # ----------------------
    # Regular User Routes
    # ----------------------
    path(
        "products/<int:product_id>/reviews/",
        ReviewListView.as_view(),
        name="review-list",
    ),
    path(
        "products/<int:product_id>/reviews/create/",
        ReviewCreateView.as_view(),
        name="review-create",
    ),
    path(
        "reviews/<int:pk>/",
        ReviewUpdateDeleteView.as_view(),
        name="review-detail",
    ),
    path(
        "reviews/<int:review_id>/vote/",
        ReviewVoteView.as_view(),
        name="review-vote",
    ),
    path(
        "reviews/<int:review_id>/comments/",
        CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "reviews/<int:review_id>/comments/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    # ----------------------
    # Admin Routes
    # ----------------------
    path(
        "admin/reviews/",
        AdminReviewListView.as_view(),
        name="admin-review-list",
    ),
    path(
        "admin/reviews/<int:review_id>/approve/",
        AdminReviewApprovalView.as_view(),
        name="admin-review-approve",
    ),
    # ----------------------
    # Create schema for swagger
    # ----------------------
    path("schema/", reviews_schema_view, name="reviews-schema"),
]
