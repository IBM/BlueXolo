import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Count
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.Products.models import Command, Source, Argument
from apps.Servers.models import TemplateServer, ServerProfile, Parameters
from apps.Servers.views import run_keyword

from apps.Testings.models import Keyword, Collection
from apps.Users.models import Task
from extracts import run_extract
from .serializers import TemplateServerSerializer, KeywordsSerializer, \
    BasicCommandsSerializer, ServerProfileSerializer, CommandsSerializer, SourceSerialzer, CollectionSerializer, \
    TaskSerializer, ArgumentsSerializer, ParametersSerializer
from .api_pagination import CommandsPagination
from .api_filters import SourceFilter, CollectionFilter, TaskFilter, ArgumentFilter, ParametersFilter


class KeywordAPIView(LoginRequiredMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordsSerializer

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
        if category:
            if category in ['2', '3', '4', '5'] and name:
                # check the category and search by his name
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
        if self.request.query_params.get('extra') == '1':
            serializer = CommandsSerializer
        return serializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommandsDetailApiView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = Command.objects.all()

    def get_serializer_class(self):
        serializer = BasicCommandsSerializer
        if self.request.query_params.get('extra') == '1':
            serializer = CommandsSerializer
        return serializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
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
            profile = ServerProfile.objects.get(pk=_config.get('profile'))
            params = json.loads(profile.config)
            _values = []
            _host = ""
            _username = ""
            _passwd = ""
            _path = ""
            for p in params:
                if p.get('parameter') == 'host':
                    _host = p.get('value')
                if p.get('parameter') == 'user':
                    _username = p.get('value')
                if p.get('parameter') == 'passwd':
                    _passwd = p.get('value')
                if p.get('parameter') == 'path':
                    _path = p.get('value')
                if p.get('category') == 2:
                    _values.append(p.get('value'))
            try:
                result, filename = run_keyword(_host, _username, _passwd, kwd.name, kwd.script, _values, _path)
                # task = Task.objects.create(
                #     name="Run Keyword -  {0}".format(kwd.name),
                #     task_id=result.task_id,
                #     state=result.state
                # )
                # request.user.tasks.add(task)
                # request.user.save()
                # run_key(host, user, passwd, filename, script, values):
                _data = {
                    'report': "{0}/test_result/{1}_report.html".format(settings.MEDIA_URL, filename)
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
    queryset = Argument.objects.all()
    serializer_class = ArgumentsSerializer
    filter_class = ArgumentFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



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
