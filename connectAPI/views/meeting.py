"""View module for handling requests about Meetings"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from connectAPI.models import MemberGroup, Group, Member, Meeting
from django.contrib.auth.models import User
from connectAPI.views.member import MemberSerializer
from connectAPI.views.group import GroupSerializer

class MeetingSerializer(serializers.HyperlinkedModelSerializer):

    member = MemberSerializer()
    group = GroupSerializer()

    class Meta:
        model = Meeting
        url = serializers.HyperlinkedIdentityField(
            view_name="meeting",
            lookup_field="id"
        )
        fields = (
            "id",
            "member",
            "group",
            "content",
            "date",
            "content",
            "title",
            "image",
            "url"
        )

class Meetings(ViewSet):
    '''Meetings created in Small Connections'''

    def create(self, request):
        '''Handle POST request for Meetings
        Returns:
            Response -- JSON serialized meeting instance'''
        
        meeting = Meeting()
        member = Member.objects.get(user=request.auth.user)
        membergroup = MemberGroup.objects.filter(is_approved=True).filter(member_id=member)
        print(membergroup)
        group = Group.objects.get(pk=membergroup[0].group_id)
        meeting.member = member
        meeting.group = group
        meeting.date = request.data['date']
        meeting.content = request.data['content']
        meeting.title = request.data['title']
        meeting.image = request.data['image']
        meeting.url = request.data['url']

        meeting.save()

        serializer = MeetingSerializer(meeting, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Handle GET requests for single Meeting
        
        Returns:
            Response -- JSON serialized meeting instance
        '''

        try:
            meeting = Meeting.objects.get(pk=pk)
            serializer = MeetingSerializer(meeting, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual Meeting

        Returns:
            Response -- Empty body with 204 status code
        """
        currentUser = Member.objects.get(user=request.auth.user)
        group = Group.objects.filter(leader_id=currentUser)
        meeting = Meeting.objects.get(pk=pk)
        meeting.id = request.data['id']
        meeting.member = currentUser
        meeting.date = request.data['date']
        meeting.content = request.data['content']
        meeting.title = request.data['title']
        meeting.image = request.data['image']
        meeting.url = request.data['url']
        meeting.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single Meeting(Request)
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            meeting = Meeting.objects.get(pk=pk)
            meeting.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Meeting.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''Handle List of requests returning only mettings of the group the leader is in'''
        try:
            currentUser = Member.objects.get(user=request.auth.user)
            group = MemberGroup.objects.filter(member_id=currentUser).filter(is_approved=True)
            meetings = Meeting.objects.filter(group_id=group[0].group_id)
            
            serializer = MeetingSerializer(
                meetings, many=True, context={'request': request})
        
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)


