from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin

from django.shortcuts import render

from .models import Reaction, Category, MoviePost, Comment, Subscriber
from .serializers import CreateMoviePostSerializer, ReactionSerializer, MoviePostSerializer, CommentSerializer, CategorySerializer, SubscriberSerializer
# Create your views here.


class CategoryGenericViewset(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class MoviePostModelViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = MoviePost.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        user = self.request.user
        context = {
            "user": user,
        }
        return context
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMoviePostSerializer
        elif self.request.method == "PUT":
            return CreateMoviePostSerializer
        return MoviePostSerializer


class ReactionGenericViewset(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        user = self.request.user
        post_id = self.kwargs.get("post_pk")
        context = {
            "user": user,
            "post_id": post_id,
        }
        return context

class CommentModelViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        user = self.request.user
        context = {
            "user": user,
        }
        return context

class SubscriberModelViewset(viewsets.ModelViewSet):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]




