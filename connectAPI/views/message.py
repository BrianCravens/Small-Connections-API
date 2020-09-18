"""View module for handling requests about Messages"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from connectAPI.models import MemberGroup, Group, Member, Message
from django.contrib.auth.models import User
from connectAPI.views.member import MemberSerializer
from connectAPI.views.group import GroupSerializer

class MessageSerializer(serializers.HyperlinkedModelSerializer):

    member = MemberSerializer()
    group = GroupSerializer()

    class Meta:
        model = Message
        url = serializers.HyperlinkedIdentityField(
            view_name="message",
            lookup_field="id"
        )
        fields = (
            "id",
            "member",
            "group",
            "date",
            "description"
        )

class Messages(ViewSet):
    '''Messages created in Small Connections'''

    def create(self, request):
        '''Handle POST request for Messages
        Returns:
            Response -- JSON serialized message instance'''
        

        message = Message()
        member = Member.objects.get(user=request.auth.user)
        membergroup = MemberGroup.objects.filter(is_approved=True).filter(member_id=member)
        print(membergroup)
        group = Group.objects.get(pk=membergroup[0].group_id)
        message.member = member
        message.group = group
        message.description = request.data['description']

        message.save()

        serializer = MessageSerializer(message, context={'request': request})

        return Response(serializer.data)



    def retrieve(self, request, pk=None):
        '''Handle GET requests for single Messages
        
        Returns:
            Response -- JSON serialized message instance
        '''

        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual Message

        Returns:
            Response -- Empty body with 204 status code
        """
        message = Message.objects.get(pk=pk)
        message.id = request.data['id']
        message.description = request.data['description']
        message.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single Message(Request)
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            message = Message.objects.get(pk=pk)
            message.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Message.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''Handle List of Messages for each group'''
        try:
            currentUser = Member.objects.get(user=request.auth.user)
            membergroup = MemberGroup.objects.filter(is_approved=True).filter(member_id=currentUser)
            messages = Message.objects.filter(group_id=membergroup[0].group_id)
            
            serializer = MessageSerializer(
                messages, many=True, context={'request': request})
        
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)


