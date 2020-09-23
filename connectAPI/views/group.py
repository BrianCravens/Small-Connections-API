"""View module for handling requests about groups"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from connectAPI.models import Group, Member, MemberGroup
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

    def create(self, request):
        '''Handle POST request for Groups
        Returns:
            Response -- JSON serialized group instance'''
        
        group = Group()
        member = Member.objects.get(user=request.auth.user)
        group.leader = member
        group.name = request.data['name']
        group.address = request.data['address']
        group.city = request.data['city']
        group.state = request.data['state']
        group.image = request.data['image']
        group.kids = request.data['kids']
        group.schedule = request.data['schedule']
        group.capacity = request.data['capacity']

        group.save()

        serializer = GroupSerializer(group, context={'request': request})

        return Response(serializer.data)

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

    def update(self, request, pk=None):
        """Handle PUT requests for an individual Members

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            currentUser = Member.objects.get(user=request.auth.user)
            group = Group.objects.get(pk=pk)
            member = Member.objects.get(pk = request.data['leader_id'])
            group.id = request.data['id']
            group.leader = member
            group.save()



        except:    
            currentUser = Member.objects.get(user=request.auth.user)
            group = Group.objects.get(pk=pk)
            group.id = request.data['id']
            group.address = request.data['address']
            group.city = request.data['city']
            group.state = request.data['state']
            group.schedule = request.data['schedule']
            group.image = request.data['image']
            group.kids = request.data['kids']
            group.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        

        groups = Group.objects.all()
        
        serializer = GroupSerializer(
            groups, many=True, context={'request': request})
        
        return Response(serializer.data)