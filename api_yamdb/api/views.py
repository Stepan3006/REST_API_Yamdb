from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from .permissions import AdminOrReadOnly
from .permissions import (IsAdmin,
                          IsOwner,
                          IsReviewPerm,
                          IsAuthorModeratorOrReadOnly)
from .serializers import (ConfirmSerializer,
                          EmailSerializer,
                          UserSerializer,
                          UserSerializerSimpleUser,
                          TitlesSerializer,
                          GenresSerializer,
                          CategoriesSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          TitlesSerializer,
                          TitlesCreateSerializer,)
from reviews.models import Review, Title, Genres, User, Categories
from django.db.models import Avg
from .filter import TitleFilter

RESTRICTED_USERNAMES = [
    'me',
]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]
    lookup_field = "username"

    @action(detail=False, methods=['get', 'patch'], permission_classes=[
        IsAuthenticated, IsOwner, ])
    def me(self, request):
        self.kwargs['username'] = request.user.username

        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)
        else:
            raise Exception('Not implemented')

    def get_serializer_class(self):
        if self.request.user.role == User.USER:
            return UserSerializerSimpleUser
        return UserSerializer


def send_msg(email, confirmation_code):
    subject = "Confirmation code"
    body = f"Ваш код подтверждения: {confirmation_code}"
    send_mail(
        subject, body, None, [email, ],
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def email(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    eml = serializer.data.get('email')
    username = serializer.data.get('username')
    if username in RESTRICTED_USERNAMES:
        return Response(
            {
                'username':
                f'Wrong username. Username - {username} is restricted'},
            status=status.HTTP_400_BAD_REQUEST)

    confirm = get_random_secret_key()

    if User.objects.filter(username=username).exists():
        return Response(
            {
                'username':
                f'Wrong username. Such user - {username}  - is already used'
            },
            status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=eml).exists():
        return Response(
            {
                'email':
                f'Wrong email. Such email - {eml}  - is already used'
            },
            status=status.HTTP_400_BAD_REQUEST)

    User.objects.create(
        email=eml,
        username=username,
        confirm=confirm
    )
    send_msg(eml, confirm)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    user = get_object_or_404(User, username=username)
    if user.confirm == serializer.data.get('confirmation_code'):
        token = str(RefreshToken.for_user(user).access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Wrong confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST)


class GetMixins(mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenresViewSet(GetMixins):
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()


class CategoriesViewSet(GetMixins):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    serializer_class = TitlesSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSerializer
        return TitlesCreateSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsReviewPerm, )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorModeratorOrReadOnly,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
