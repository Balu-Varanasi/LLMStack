from allauth.socialaccount.providers.saml.views import ACSView as AllauthACSView
from allauth.socialaccount.providers.saml.views import (
    FinishACSView as AllauthFinishACSView,
)
from allauth.socialaccount.providers.saml.views import LoginView as AllauthLoginView
from allauth.socialaccount.providers.saml.views import (
    MetadataView as AllauthMetadataView,
)
from allauth.socialaccount.providers.saml.views import (
    SAMLViewMixin as AllauthSAMLViewMixin,
)
from allauth.socialaccount.providers.saml.views import SLSView as AllauthSLSView


class SAMLViewMixin(AllauthSAMLViewMixin):
    pass


class ACSView(SAMLViewMixin, AllauthACSView):
    pass


acs = ACSView.as_view()


class FinishACSView(SAMLViewMixin, AllauthFinishACSView):
    pass


finish_acs = FinishACSView.as_view()


class SLSView(SAMLViewMixin, AllauthSLSView):
    pass


sls = SLSView.as_view()


class MetadataView(SAMLViewMixin, AllauthMetadataView):
    pass


metadata = MetadataView.as_view()


class LoginView(SAMLViewMixin, AllauthLoginView):
    pass


login = LoginView.as_view()
