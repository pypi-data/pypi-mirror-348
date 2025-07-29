from datetime import datetime, timedelta
from office365.sharepoint.client_context import ClientContext
from django.conf import settings


class SharePointContext:
    _instance = None
    _client_credentials = None
    _ctx = None
    _last_created = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharePointContext, cls).__new__(cls)
            cls._initialize(cls._instance)
        elif datetime.now() - cls._last_created > timedelta(minutes=45):
            cls._initialize(cls._instance)
        return cls._instance

    @classmethod
    def _initialize(cls, instance):
        client_id = getattr(settings, 'SHAREPOINT_APP_CLIENT_ID', 'client_id')
        sharepoint_url = getattr(settings, 'SHAREPOINT_URL', 'sharepoint_url')
        sharepoint_api_certificate_path = getattr(settings, 'SHAREPOINT_API_CERTIFICATE_PATH', 'sharepoint_api_certificate_path')
        sharepoint_api_certificate_thumbprint = getattr(settings, 'SHAREPOINT_API_CERTIFICATE_THUMBPRINT', 'sharepoint_api_certificate_thumbprint')
        sharepoint_api_tenant_name = getattr(settings, 'SHAREPOINT_API_TENANT_NAME', 'sharepoint_api_tenant_name')

        cert_settings = {
            'client_id': client_id,
            'thumbprint': sharepoint_api_certificate_thumbprint,
            'cert_path': sharepoint_api_certificate_path
        }
        instance._ctx = ClientContext(sharepoint_url).with_client_certificate(sharepoint_api_tenant_name, **cert_settings)
        cls._last_created = datetime.now()

    @property
    def client_credentials(self):
        return self._client_credentials

    @property
    def ctx(self):
        return self._ctx