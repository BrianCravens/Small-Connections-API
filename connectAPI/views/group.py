"""View module for handling requests about groups"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from connectAPI.models import Group
from django.contrib.auth.models import User
from connectAPI.views.member import MemberSerializer

class GroupSerializer(serializers.HyperlinkedModelSerializer):

    leader = MemberSerializer()
    class Meta:
        model = Group
        url = serializers.HyperlinkedIdentityField(
            view_name="group",
            lookup_field="id"
        )
        fields = (
            "id",
            "leader",
            "name",
            "address",
            "city",
            "state",
            "capacity",
            "schedule",
            "image",
            "kids"
        )

class Groups(ViewSet):
    '''Groups created in Small Connections'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for single Group
        
        Returns:
            Response -- JSON serialized group instance
        '''

        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        

        groups = Group.objects.all()
        
        serializer = GroupSerializer(
            groups, many=True, context={'request': request})
        
        return Response(serializer.data)