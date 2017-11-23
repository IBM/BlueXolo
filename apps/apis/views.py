import json
import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Count
from django.http import JsonResponse
from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from string import digits, ascii_lowercase
from random import choice

from apps.Products.models import Command, Source, Argument
from apps.Servers.models import TemplateServer, ServerProfile, Parameters
from apps.Servers.views import run_keyword

from apps.Testings.models import Keyword, Collection, TestCase, Phase, TestSuite
from apps.Testings.views import apply_highlight
from apps.Users.models import Task
from extracts import run_extract
from .serializers import TemplateServerSerializer, KeywordsSerializer, \
    BasicCommandsSerializer, ServerProfileSerializer, CommandsSerializer, SourceSerialzer, CollectionSerializer, \
    TaskSerializer, ArgumentsSerializer, ParametersSerializer, TestCaseSerializer, PhaseSerializer, TestSuiteSerializer
from .api_pagination import CommandsPagination, KeywordPagination, TestCasePagination
from .api_filters import SourceFilter, CollectionFilter, TaskFilter, ArgumentFilter, ParametersFilter, TestCaseFilter, \
    PhaseFilter, TestSuiteFilter


class KeywordAPIView(LoginRequiredMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordsSerializer
    pagination_class = KeywordPagination

    def get_queryset(self):
        script_type = self.request.query_params.get('script_type')
        if script_type:
            qs = Keyword.objects.filter(script_type=int(script_type))
        else:
            qs = Keyword.objects.all()
        return qs

    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name')
        collection = self.request.query_params.get('collection')
        if collection:
            queryset = queryset.filter(collection=collection)
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class KeywordDetailApiView(LoginRequiredMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordsSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ServerTemplateApiView(LoginRequiredMixin,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = TemplateServer.objects.all()
    serializer_class = TemplateServerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Template Created")
        return self.create(request, *args, **kwargs)


class ServerTemplateDetailApiView(LoginRequiredMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView):
    queryset = TemplateServer.objects.all()
    serializer_class = TemplateServerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        messages.success(self.request, "Template Updated")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ServerProfileApiView(LoginRequiredMixin,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    queryset = ServerProfile.objects.all()
    serializer_class = ServerProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Profile Created")
        return self.create(request, *args, **kwargs)


class ServerProfileDetailApiView(LoginRequiredMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 generics.GenericAPIView):
    queryset = ServerProfile.objects.all()
    serializer_class = ServerProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        messages.success(self.request, "Profile Updated")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommandsApiView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = Command.objects.all()
    pagination_class = CommandsPagination

    def filter_queryset(self, queryset):
        queryset = Command.objects.all()
        name = self.request.query_params.get('name')
        id_command = self.request.query_params.get('id')
        category = self.request.query_params.get('category')
        source = self.request.query_params.get('source')
        exact = self.request.query_params.get('exact')
        full_search = self.request.query_params.get('full_search')
        if full_search == '1':
            queryset = queryset.filter(
                Q(source__name__icontains=name) |
                Q(name__icontains=name)
            )
            if category:
                queryset = queryset.filter(source__category=category)
            return queryset.annotate(Count('id'))
        if category:
            if category in ['2', '3', '4', '5'] and name:
                # check the category and search by his name
                if category == '4':
                    queryset = queryset.filter(
                        Q(source__category=5) |
                        Q(source__depends__category=4)
                    )
                else:
                    queryset = queryset.filter(source__category=category)
                if exact:
                    queryset = queryset.filter(
                        Q(source__name=name) |
                        Q(name=name)
                    )
                else:
                    queryset = queryset.filter(
                        Q(source__name__istartswith=name) |
                        Q(name__istartswith=name)
                    )
            else:
                queryset = queryset.filter(source__category=category)
            return queryset.annotate(Count('id'))
        if name:
            if exact:
                queryset = queryset.filter(name=name)
            else:
                queryset = queryset.filter(name__istartswith=name)
        if id_command:
            queryset = queryset.filter(id=id_command)
        if source:
            queryset = queryset.filter(source__id=source)
        return queryset

    def get_serializer_class(self):
        serializer = BasicCommandsSerializer
        if self.request.query_params.get('extra') == '1' or self.request.data.get('extra') == '1':
            serializer = CommandsSerializer
        return serializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(request, "Command Created")
        return self.create(request, *args, **kwargs)


class CommandsDetailApiView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = Command.objects.all()

    def get_serializer_class(self):
        serializer = BasicCommandsSerializer
        if self.request.query_params.get('extra') == '1' or self.request.data.get('extra') == '1':
            serializer = CommandsSerializer
        return serializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        messages.success(request, "Command Updated")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RunExtract(LoginRequiredMixin, APIView):
    """Call Extract Class for get commands form different sources"""

    def post(self, request):
        _status = status.HTTP_200_OK
        _config = request.data
        data = {}
        try:
            file = request.FILES.get('zip')
            if file:
                fs = FileSystemStorage(location='{0}/zip/'.format(settings.MEDIA_ROOT))
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url('zip/{}'.format(filename))
                _config.update({"zip": uploaded_file_url})
            origin = 'Local Server'
            if _config.get('host'):
                origin = _config.get('host')
            extract = run_extract.delay(_config)
            task = Task.objects.create(
                name="Extract commands from {0}".format(origin),
                category=1,
                task_info="Started",
                task_id=extract.task_id,
                state=extract.state
            )
            request.user.tasks.add(task)
            request.user.save()
            messages.success(request, "Running the extract in background")
            data = {"text": "success"}
        except Exception as error:
            data = None
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(status=_status, data=data)


class SourceApiView(LoginRequiredMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView
                    ):
    queryset = Source.objects.all()
    serializer_class = SourceSerialzer
    filter_class = SourceFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CollectionApiView(LoginRequiredMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView
                        ):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_class = CollectionFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RunOnServerApiView(LoginRequiredMixin, APIView):
    """Call "functions for run scripts on servers"""

    def post(self, request):
        _status = status.HTTP_200_OK
        _config = request.data
        _data = {}
        try:
            kwd = Keyword.objects.get(pk=_config.get('keyword'))
            _host = ""
            _username = ""
            _passwd = ""
            _path = ""
            _profile_name = ""
            _values = []
            _values_name = []
            _perfiles = json.loads(_config.get('profile'))
            for perfil in _perfiles:
                _server_profile = ServerProfile.objects.get(pk=perfil)
                if _server_profile.category == 2:
                    _parametros = json.loads(_server_profile.config)
                    for p in _parametros:
                        _parametro = Parameters.objects.get(pk=p.get('id'))
                        if _parametro.name == 'host':
                            _host = p.get('value')
                        if _parametro.name == 'user':
                            _username = p.get('value')
                        if _parametro.name == 'passwd':
                            _passwd = p.get('value')
                        if _parametro.name == 'path':
                            _path = p.get('value')
                elif _server_profile.category == 1:
                    _global_variables = json.loads(_server_profile.config)
                    _profile_name = _server_profile.name
                    for variable in _global_variables:
                        _values.append(variable.get('value'))
                        _param_name = Parameters.objects.get(pk=variable.get('id'))
                        _arreglo = []
                        _arreglo.append(_param_name.name)
                        _arreglo.append(variable.get('value'))
                        _values_name.append(_arreglo)
            try:
                random_string = ''.join(choice(ascii_lowercase + digits) for i in range(12))
                today = time.strftime("%y_%m_%d")
                name = kwd.name.replace(" ", "")
                name_file = "{0}_{1}_{2}".format(name, random_string, today)
                filename = run_keyword.delay(_host, _username, _passwd, kwd.name, kwd.script, _values, _path, name_file,
                                             _profile_name, _values_name)
                task = Task.objects.create(
                    name="Run Keyword -  {0}".format(kwd.name),
                    task_id=filename.task_id,
                    state="run",
                    task_result="{0}/{1}test_result/{2}_report.html".format(settings.SITE_DNS, settings.MEDIA_URL,
                                                                            name_file)
                )
                request.user.tasks.add(task)
                request.user.save()
                _data = {
                    'report': "{0}test_result/{1}_report.html".format(settings.MEDIA_URL, name_file)
                }
            except Exception as errorConnection:
                _status = 500
                _data = {
                    'text': "{0}".format(errorConnection)
                }
        except Exception as Error:
            _status = 500
            _data = {
                'text': "{0}".format(Error)
            }
        return Response(status=_status, data=_data)


class TasksApiView(LoginRequiredMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView
                   ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArgumentsApiView(LoginRequiredMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView
                       ):
    serializer_class = ArgumentsSerializer
    filter_class = ArgumentFilter

    def get_queryset(self):
        qs = Argument.objects.exclude(id__in=[1, 2, 3, 4, 5, 6])
        return qs.annotate(Count('id'))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArgumentsDetailApiView(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             generics.GenericAPIView):
    queryset = Argument.objects.all()
    serializer_class = ArgumentsSerializer
    filter_class = ArgumentFilter

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ParametersApiView(LoginRequiredMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView
                        ):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer
    filter_class = ParametersFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ParametersDetailApiView(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer
    filter_class = ParametersFilter

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TestCaseApiView(LoginRequiredMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView
                      ):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    pagination_class = TestCasePagination

    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name')
        collection = self.request.query_params.get('collection')
        if collection:
            queryset = queryset.filter(collection=collection)
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestCaseDetailApiView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    filter_class = TestCaseFilter

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PhaseApiView(LoginRequiredMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView
                   ):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer
    filter_class = PhaseFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PhaseDetailApiView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer
    filter_class = PhaseFilter

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TestSuiteApiView(LoginRequiredMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView
                       ):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    filter_class = TestSuiteFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestSuiteDetailApiView(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             generics.GenericAPIView):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    filter_class = TestSuiteFilter

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET'])
def get_highlight_version(request):
    if request.is_ajax:
        script = request.query_params.get('script')
        data = {}
        if script:
            try:
                data = {"script_result": apply_highlight(script)}
            except Exception as error:
                data = {'text': '{0}'.format(error)}
            return JsonResponse(data)
