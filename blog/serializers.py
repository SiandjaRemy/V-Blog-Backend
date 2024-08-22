from email.policy import default
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

    
    # def create(self, validated_data):
    #     post_id = self.context["post_id"]
    #     post = MoviePost.objects.only("id").filter(id=post_id).first()
    #     validated_data["post"] = post
    #     return super().create(validated_data)
    

class CreateReactionSerializer(serializers.Serializer):
    ip_address = serializers.CharField(max_length=20)
    type = serializers.ChoiceField(choices=Reaction.Type.choices, default=Reaction.Type.NICE)

    def save(self, **kwargs):
        ip_address = self.validated_data["ip_address"]
        type = self.validated_data["type"]
        post_id = self.context["post_id"]
        post = MoviePost.objects.only("id").filter(id=post_id).first()
        try:
            existing_reaction = Reaction.objects.get(
                post=post,
                ip_address=ip_address,
                type=type, # Include 'type' in the check
            )
            # Delete existing reaction
            existing_reaction.delete()
            return None # Indicate reaction was deleted

        except Reaction.DoesNotExist:
            # Create a new reaction
            reaction = Reaction.objects.create(
                post=post, type=type, ip_address=ip_address
            )
            return reaction


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(many=False)
    class Meta:
        model = Comment
        fields = ["author", "content", "created_at"]


class MoviePostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(many=False)
    reactions = ReactionSerializer(many=True)
    comments = CommentSerializer(many=True)
    class Meta:
        model = MoviePost
        fields = ["id", "author", "movie_name", "synopsis", "category", "my_review", "image", "gif", "reactions", "comments", "created_at"]


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

    


