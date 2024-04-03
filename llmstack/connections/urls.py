import logging

from django.urls import include, path, re_path

from .apis import ConnectionsViewSet
from .handlers.google import GoogleAdapter
from .handlers.hubspot import HubspotAdapter
from .views import oauth2 as oauth2_views
from .views import saml as saml_views

logger = logging.getLogger(__name__)


saml_urlpatterns = [
    re_path(
        r"^connections/saml/(?P<organization_slug>[^/]+)/",
        include(
            [
                path(
                    "acs/",
                    saml_views.acs,
                    name="saml_acs",
                ),
                path(
                    "acs/finish/",
                    saml_views.finish_acs,
                    name="saml_finish_acs",
                ),
                path(
                    "sls/",
                    saml_views.sls,
                    name="saml_sls",
                ),
                path(
                    "metadata/",
                    saml_views.metadata,
                    name="saml_metadata",
                ),
                path(
                    "login/",
                    saml_views.login,
                    name="saml_login",
                ),
            ]
        ),
    )
]

oauth2_urlpatterns = [
    path(
        "connections/hubspot/login/",
        oauth2_views.CustomOAuth2LoginView.adapter_view(HubspotAdapter),
        name="hubspot_connection_login",
    ),
    path(
        "connections/hubspot/login/callback/",
        oauth2_views.CustomOAuth2CallbackView.adapter_view(HubspotAdapter),
        name="hubspot_connection_callback",
    ),
    path(
        "connections/google/login/",
        oauth2_views.CustomOAuth2LoginView.adapter_view(GoogleAdapter),
        name="google_connection_login",
    ),
    path(
        "connections/google/login/callback/",
        oauth2_views.CustomOAuth2CallbackView.adapter_view(GoogleAdapter),
        name="google_connection_callback",
    ),
]


urlpatterns = [
    path(
        "api/connection_types",
        ConnectionsViewSet.as_view({"get": "get_connection_types"}),
    ),
    path(
        "api/connections",
        ConnectionsViewSet.as_view({"get": "list"}),
    ),
    path(
        "api/connections/<str:uid>/access_token",
        ConnectionsViewSet.as_view({"get": "get_access_token"}),
    ),
    path(
        "api/connections/<str:uid>",
        ConnectionsViewSet.as_view(
            {
                "get": "get",
                "post": "post",
                "patch": "patch",
                "delete": "delete",
            },
        ),
    ),
]

urlpatterns += oauth2_urlpatterns
urlpatterns += saml_urlpatterns
