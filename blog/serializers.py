from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Comment, MoviePost, Reaction, Subscriber, Category

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

    
    def create(self, validated_data):
        post_id = self.context["post_id"]
        post = MoviePost.objects.only("id").filter(id=post_id).first()
        validated_data["post"] = post
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(many=False)
    class Meta:
        model = Comment
        fields = ["author", "content", "created_at"]


class MoviePostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(many=False)
    class Meta:
        model = MoviePost
        fields = ["id", "author", "movie_name", "synopsis", "category", "my_review", "image", "gif", "image_url", "gif_url", "created_at"]


class CreateMoviePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviePost
        fields = ["id", "movie_name", "synopsis", "category", "my_review", "image", "gif", "created_at"]

    # Overwrite the create method to add the author to validated data for post
    def create(self, validated_data):
        user = self.context["user"]

        validated_data["author"] = user

        return super().create(validated_data)


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["id", "email", "ip_address"]

    


