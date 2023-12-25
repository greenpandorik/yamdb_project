from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer
from django.shortcuts import get_object_or_404

from api.pagination import LimitPageNumberPagination
from .serializers import (CustomUserSerializer, CustomUserCreateSerializer,
                          SubscriptionSerializer
                          )
from .models import User, Subscription


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response('Пароль изменён успешно!',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=["post", "delete"],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data=request.data,
                context={'request': request, 'author': author})
            if not serializer.is_valid():
                return Response({'errors': 'Автор не найден'},
                                status=status.HTTP_404_NOT_FOUND)
            serializer.save(author=author, user=user)
            return Response({'Подписка успешно создана': serializer.data},
                            status=status.HTTP_201_CREATED)
        if Subscription.objects.filter(author=author, user=user).exists():
            Subscription.objects.get(author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Автор не найден в подписках'},
                        status=status.HTTP_404_NOT_FOUND)

    @action(detail=False,
            methods=["get"],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = Subscription.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = SubscriptionSerializer(pages,
                                            many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)
