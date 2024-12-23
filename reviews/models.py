from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Product"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Review Title"))
    body = models.TextField(verbose_name=_("Review Body"))
    rating = models.PositiveSmallIntegerField(
        verbose_name=_("Rating"), help_text=_("Rating from 1 to 5")
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_("Approved"),
        help_text=_("Whether this review is approved by an admin"),
    )
    show_name = models.BooleanField(
        default=True,
        verbose_name=_("Show Name"),
        help_text=_("Whether to display the user's name with the review"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        unique_together = (
            "user",
            "product",
        )  # Each user can review a product only once

    def __str__(self):
        return f"{self.title} by {self.user.username if self.show_name else 'Anonymous'} for {self.product.name}"
