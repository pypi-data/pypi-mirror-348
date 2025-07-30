import base64
import json
from rest_framework import status
from rest_framework.views import APIView

from ardhi_framework.request import ArdhiRequest
from ardhi_framework.response import ArdhiResponse
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.conf import settings
from django.views.generic import View
import jwt
from ardhi_framework.exceptions import get_exception_response
from ardhi_framework.models import ArdhiBaseModel, ArdhiModel


class ViewMixinWrapper:
    ...


class ArdhiGenericView(View):
    pass


class ArdhiViewMixin:
    request: ArdhiRequest = None
    request_id = None
    application_instance = None
    delete_serializer = None
    logged_in_user = None
    context = {}
    headers = {}
    active_role = 'UNKNOWN_ROLE'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = self.return_headers()
        self.logged_in_user = self.get_logged_in_user()
        self.request_id = self.get_request_id()
        self.active_role = self.get_active_role()
        self.context = self.get_serializer_context()

        # set some factors
        self.request.is_authenticated = bool(self.logged_in_user)

    def get_serializer_context(self):
        context = {
            'headers': self.headers,
            'user': self.logged_in_user,
            'request_id': self.request_id,
            'request': self.application_instance,
            'method': self.request.method,
            'active_role': self.active_role,
        }
        return context

    def get_active_role(self):
        if self.headers.get('CPARAMS', None) is not None:
            return json.loads((base64.b64decode(self.headers.get('CPARAMS').encode()).decode('utf-8')))['active_role']
        return 'UNKNOWN_ROLE'

    def get_request_id(self, req_id=None):
        if not req_id:
            return self.request.query_params.get('request_id', self.request.data.get('request_id', None))
        return req_id

    def decode_jwt(self):
        return jwt.decode(self.headers.get('JWTAUTH').split(' ')[1], settings.SECRET_KEY, algorithms='RS256',
                          options={"verify_signature": True})

    def get_logged_in_user(self):
        return self.decode_jwt().get('user')

    def return_headers(self):
        headers = {
            'Authorization': self.request.headers.get('Authorization'),
            'JWTAUTH': self.request.headers.get('JWTAUTH'),
            'CPARAMS': self.request.headers.get('CPARAMS')
        }
        return headers


class ArdhiBaseView(ArdhiViewMixin, ViewMixinWrapper, ArdhiGenericView):
    # requires that each function to have serializer_class and return success message
    serializer_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        assert isinstance(self.request, View), (
            "Ardhi Base View requires that the view be a Valid Django View."
        )

    @staticmethod
    def return_invalid_serializer(serializer):
        return get_exception_response(serializer.errors)

    @staticmethod
    def return_failed(created_response):
        return ArdhiResponse({'details': created_response}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def return_success(data):
        return ArdhiResponse(data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        raise NotImplementedError('View must define a serializer_class attribute.')

    def run_serializer_validator(self, success_msg=None):
        """Processes the serializer through validation to save"""
        context = self.get_serializer_context()
        if context['method'] == 'PATCH':
            self.serializer_class = self.delete_serializer
        serializer = self.get_serializer_class()(
            data=self.request.data,
            context=context
        )
        if not serializer.is_valid():
            return self.return_invalid_serializer(serializer)

        created, created_response = serializer.save()
        if not created:
            return self.return_failed(created_response)
        if created_response is not None:
            if isinstance(created_response, dict):
                created_response['details'] = success_msg
                return self.return_success(created_response)
            elif isinstance(created_response, str):
                return self.return_success({"details": created_response})
        return self.return_success({"details": success_msg})


class ArdhiGenericViewSet(ArdhiBaseView, GenericViewSet): ...


class ArdhiAPIView(ArdhiBaseView, APIView): ...


class ArdhiModelViewSet(ArdhiBaseView, ModelViewSet):
    model: ArdhiBaseModel = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        assert isinstance(self.model, (ArdhiBaseModel, ArdhiModel)), "This view must be used with an Ardhi Custom Model."

    def perform_destroy(self, request, *args, **kwargs):
        # ensure no delete occurs by overriding destroy method
        return


