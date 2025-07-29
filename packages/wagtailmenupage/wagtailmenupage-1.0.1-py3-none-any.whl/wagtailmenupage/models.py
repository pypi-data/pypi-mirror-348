from django.db import models
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.models import Page


class CustomMenuUrl(Page):
    """A page mode that contains a custom URL.
    This page has no frontend and won't display in the sitemap.
    """

    subpage_types = []
    preview_modes = []
    search_fields = []

    custom_url = models.CharField(max_length=255)

    open_in_new_tab = models.BooleanField(
        default=False,
    )

    content_panels = [
        FieldPanel(
            "title",
            heading=_("Label"),
            help_text=_("Label for the menu item."),
        ),
        FieldPanel(
            "custom_url",
            heading=_("URL"),
            help_text=_("The URL to use for the menu item."),
        ),
        FieldPanel(
            "open_in_new_tab",
            heading=_(
                "Open in new tab",
            ),
            help_text=_("Open the URL in a new tab."),
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
        ]
    )

    @property
    def url(self):
        """Return the custom URL."""
        return self.custom_url

    def get_url(self, *args, **kwargs):
        """Return the custom URL."""
        return self.url

    def clean(self):
        """Sets the slug automatically, based on the ID of the page so as to avoid conflicts."""
        self.slug = f"custom_menu_url_{self.id}"
        self.show_in_menus = True
        super().clean()

    def serve(self, *args, **kwargs):
        """Raise a 404 error when the page is accessed directly."""
        raise Http404("This page does not exist.")

    def get_sitemap_urls(self, *args, **kwargs):
        """Override the default sitemap URL generation to return an empty list.
        This prevents the page from appearing in the sitemap.
        """
        return []

    def __str__(self):
        return self.url

    class Meta:
        db_table = "wagtailmenupage_custom_menu_url"
        verbose_name = "Custom Menu URL"
        verbose_name_plural = "Custom Menu URLs"
