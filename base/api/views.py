from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import *
from .serializers import *
@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms/',
        'GET /api/rooms/:id/',
    ]
    #safe is set to false to allow for any data to be sent
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    #objects can't be converted tojson, so we need to convert them to dicts many is set to true to allow for multiple objects
    rooms_serializer = RoomSerializer(rooms, many=True)
    return Response(status=status.HTTP_200_OK, data=rooms_serializer.data)


@api_view(['GET'])
def getRoom(request, id):
    room = Room.objects.get(id=id)
    #objects can't be converted tojson, so we need to convert them to dicts many is set to true to allow for multiple objects
    room_serializer = RoomSerializer(room, many=False)
    return Response(status=status.HTTP_200_OK, data=room_serializer.data)