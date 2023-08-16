from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from chat.models import ChatRoom, ChatMessage
from api.models import CustomUser


class ChatRoomView(APIView):
    def get(self, request, userId):
        if request.query_params.get("user", None) is not None:
            user = CustomUser.objects.get(id=request.query_params.get("user"))
            chatRooms = user.chatroom_set.all()
            serializer = ChatRoomSerializer(
                chatRooms, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        chatRooms = ChatRoom.objects.filter(member=userId)
        serializer = ChatRoomSerializer(
            chatRooms, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.query_params.get("id", None) is not None:
            chatroom = ChatRoom.objects.get(roomId=request.query_params.get("id"))
            chatroom.delete()
            return Response({"status": "success"}, status=status.HTTP_200_OK)


class MessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        roomId = self.kwargs["roomId"]
        return ChatMessage.objects.filter(chat__roomId=roomId).order_by("-timestamp")
