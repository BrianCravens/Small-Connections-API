"""View module for handling requests about members"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from connectAPI.models import Member
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name="user",
            lookup_field="id"
        )
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_joined",
            "email"
        )

class MemberSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Member
        url = serializers.HyperlinkedIdentityField(
            view_name="member",
            lookup_field="id"
        )
        fields = (
            "id",
            "phone",
            "address",
            "birthday",
            "is_admin",
            "image",
            "user"
        )
        depth = 2

class Members(ViewSet):
    '''Members who join Small Connections'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for single Members
        
        Returns:
            Response -- JSON serialized customer instance
        '''

        try:
            member = Member.objects.get(pk=pk)
            serializer = MemberSerializer(member, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        

        members = Member.objects.all()
        
        serializer = MemberSerializer(
            members, many=True, context={'request': request})
        
        return Response(serializer.data)