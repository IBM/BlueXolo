import json

from rest_framework import serializers

from apps.Products.models import Command, Argument, Source
from apps.Servers.models import TemplateServer, ServerProfile, Parameters
from apps.Testings.models import Keyword, Collection, TestCase, Phase, TestSuite
from apps.Users.models import Task


class ArgumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Argument
        fields = '__all__'


class SourceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class CommandsSerializer(serializers.ModelSerializer):
    arguments = ArgumentsSerializer(many=True)
    source = SourceSerialzer(many=True)

    class Meta:
        model = Command
        fields = '__all__'

    def create(self, validated_data):
        args = json.loads(self.initial_data['arguments'])
        sources = json.loads(self.initial_data['source'])
        command = Command.objects.create(
            name=validated_data['name'],
            description=validated_data['description']
        )
        for s in sources:
            command.source.add(s)
            command.save()
        for arg in args:
            command.arguments.add(arg)
            command.save()
        return command

    def update(self, instance, validated_data):
        try:
            args = json.loads(self.initial_data['arguments'])
            srcs = json.loads(self.initial_data['source'])
            instance.name = validated_data.get('name')
            instance.description = validated_data.get('description')
            instance.source = validated_data.get('source')

            for s in instance.source.all():
                instance.source.remove(s)
            for source in srcs:
                instance.source.add(source)
                instance.save()

            for arg in instance.arguments.all():
                instance.arguments.remove(arg)
            for a in args:
                instance.arguments.add(a)
                instance.save()
            return instance
        except Exception as error:
            raise RuntimeError('`update()` have error {0}.'.format(error))


class BasicCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = [
            'id',
            'name',
            'description'
        ]


class ParametersSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Parameters
        fields = '__all__'


class TemplateServerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    parameters = ParametersSerializer(many=True)

    class Meta:
        model = TemplateServer
        fields = '__all__'

    def create(self, validated_data):
        params = json.loads(self.initial_data['params'])
        template = TemplateServer.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            category=validated_data['category'],
            user=validated_data['user']
        )
        for param in params:
            template.parameters.add(param)
        template.save()
        return template

    def update(self, instance, validated_data):
        try:
            params = json.loads(self.initial_data['params'])
            instance.name = validated_data.get('name')
            instance.description = validated_data.get('description')
            instance.category = validated_data.get('category')
            for p in instance.parameters.all():
                instance.parameters.remove(p)
            for param in params:
                instance.parameters.add(param)
                instance.save()
            return instance
        except Exception as error:
            raise RuntimeError('`update()` have error {0}.'.format(error))


class KeywordsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Keyword
        fields = '__all__'


class ServerProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ServerProfile
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TestCaseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TestCase
        fields = '__all__'


class PhaseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Phase
        fields = '__all__'


class TestSuiteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TestSuite
        fields = '__all__'
