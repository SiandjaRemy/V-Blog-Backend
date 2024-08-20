from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Comment, Post, Reaction, Subscriber, Category

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["ip_address", "type", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(many=False)
    class Meta:
        model = Comment
        fields = ["author", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(many=False)
    class Meta:
        model = Post
        fields = ["id", "title", "content", "category", "image", "created_at"]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "category", "image", "created_at"]

    def create(self, validated_data):
        user = self.context["user"]

        validated_data["author"] = user

        return super().create(validated_data)


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"