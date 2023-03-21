from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post, Comment, Group, Follow, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    permission_classes = [IsAuthenticated]
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    permission_classes = [IsAuthenticated]
    # comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Subscription to the author is already arranged.',
            ),
        )

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError("You can't subscribe to yourself.")
        return data
