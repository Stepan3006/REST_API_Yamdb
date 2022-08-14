from rest_framework import serializers
from reviews.models import Categories, Genres, Title
from rest_framework import serializers
from reviews.models import User
from reviews.models import Comment, Review, Categories


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio',
                  'email', 'role',)

        model = User
        lookup_field = "username"
        lookup_value_regex = "[^/]+"


class UserSerializerSimpleUser(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio',
                  'email', 'role',)
        model = User
        lookup_field = "username"
        lookup_value_regex = "[^/]+"


class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField()


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

    def get_rating(self):
        return None


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context['request'].user
            if Review.objects.filter(title__id=title_id,
                                     author=author).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
