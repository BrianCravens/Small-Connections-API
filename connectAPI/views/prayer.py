"""View module for handling requests about Messages"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from connectAPI.models import MemberGroup, Group, Member, Prayer
from django.contrib.auth.models import User
from connectAPI.views.member import MemberSerializer
from connectAPI.views.group import GroupSerializer

class PrayerSerializer(serializers.HyperlinkedModelSerializer):

    member = MemberSerializer()
    group = GroupSerializer()

    class Meta:
        model = Prayer
        url = serializers.HyperlinkedIdentityField(
            view_name="prayer",
            lookup_field="id"
        )
        fields = (
            "id",
            "member",
            "group",
            "date",
            "description"
        )

class Prayers(ViewSet):
    '''Prayers created in Small Connections'''

    def create(self, request):
        '''Handle POST request for Prayers
        Returns:
            Response -- JSON serialized prayer instance'''
        
        try:
            prayer = Prayer()
            member = Member.objects.get(user=request.auth.user)
            membergroup = MemberGroup.objects.filter(is_approved=True).filter(member_id=member)
            print(membergroup)
            group = Group.objects.get(pk=membergroup[0].group_id)
            prayer.member = member
            prayer.group = group
            prayer.description = request.data['description']

            prayer.save()

            serializer = PrayerSerializer(prayer, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        '''Handle GET requests for single Prayers
        
        Returns:
            Response -- JSON serialized prayer instance
        '''

        try:
            prayer = Prayer.objects.get(pk=pk)
            serializer = PrayerSerializer(prayer, context={'request': request})
            print(serializer.data)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual Prayer

        Returns:
            Response -- Empty body with 204 status code
        """
        prayer = Prayer.objects.get(pk=pk)
        prayer.id = request.data['id']
        prayer.description = request.data['description']
        prayer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single Prayer(Request)
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            prayer = Prayer.objects.get(pk=pk)
            prayer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Prayer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        '''Handle List of Prayers for each group'''
        try:
            currentUser = Member.objects.get(user=request.auth.user)
            membergroup = MemberGroup.objects.filter(is_approved=True).filter(member_id=currentUser)
            prayers = Prayer.objects.filter(group_id=membergroup[0].group_id)
            
            serializer = PrayerSerializer(
                prayers, many=True, context={'request': request})
        
            return Response(serializer.data)
            
        except Exception as ex:
            return HttpResponseServerError(ex)