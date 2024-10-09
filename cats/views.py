from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # pagination_class = PageNumberPagination
    pagination_class = None
    filterset_fields = ('color', 'birth_year',)
    search_fields = ('$name', 'achievements__name',)
    ordering_fields = ('name', 'birth_year',)
    ordering = ('birth_year',)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    throttle_scope = 'low_request'

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer