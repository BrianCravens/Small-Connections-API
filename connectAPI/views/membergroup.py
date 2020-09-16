"""View module for handling requests about Member Groups"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from connectAPI.models import MemberGroup, Group, Member
from django.contrib.auth.models import User
from connectAPI.views.member import MemberSerializer
from connectAPI.views.group import GroupSerializer

class MemberGroupSerializer(serializers.HyperlinkedModelSerializer):

    member = MemberSerializer()
    group = GroupSerializer()

    class Meta:
        model = MemberGroup
        url = serializers.HyperlinkedIdentityField(
            view_name="membergroup",
            lookup_field="id"
        )
        fields = (
            "id",
            "member",
            "group",
            "is_approved",
            "date"
        )

class MemberGroups(ViewSet):
    '''MemberGroups created in Small Connections'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for single MemberGroup
        
        Returns:
            Response -- JSON serialized membergroup instance
        '''

        try:
            membergroup = MemberGroup.objects.get(pk=pk)
            serializer = MemberGroupSerializer(membergroup, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual MemberGroup

        Returns:
            Response -- Empty body with 204 status code
        """
        membergroup = MemberGroup.objects.get(pk=pk)
        membergroup.id = request.data['id']
        membergroup.is_approved = request.data['is_approved']
        membergroup.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single MemberGroup(Request)
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            membergroup = MemberGroup.objects.get(pk=pk)
            membergroup.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except MemberGroup.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''Handle List of requests returning only requests of the group the leader is in'''
        try:
            currentUser = Member.objects.get(user=request.auth.user)
            group = Group.objects.filter(leader_id=currentUser)
            membergroups = MemberGroup.objects.filter(is_approved=False).filter(group_id=group[0].id)
            
            serializer = MemberGroupSerializer(
                membergroups, many=True, context={'request': request})
        
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)


