from django.contrib.auth import get_user_model
from django_filters import CharFilter
from django_filters.filterset import STRICTNESS
from rest_framework.filters import DjangoFilterBackend, FilterSet
from rest_framework.generics import ListAPIView

from data_import.models import DataFile
from public_data.serializers import PublicDataFileSerializer
from studies.views import RetrieveStudyDetailView

from .filters import StartEndDateFromToRangeFilter
from .serializers import MemberSerializer

UserModel = get_user_model()


class MemberDetailAPIView(RetrieveStudyDetailView):
    """
    Return information about the member.
    """

    def get_queryset(self):
        return UserModel.objects.filter(pk=self.request.user.pk)

    lookup_field = None
    serializer_class = MemberSerializer


class PublicDataFileFilter(FilterSet):
    """
    A FilterSet that maps member_id and username to less verbose names.
    """

    created = StartEndDateFromToRangeFilter()
    member_id = CharFilter(name='user__member__member_id')
    username = CharFilter(name='user__username')
    strict = STRICTNESS.RAISE_VALIDATION_ERROR

    class Meta:
        model = DataFile
        fields = ('created', 'source', 'username', 'member_id')


class PublicDataListAPIView(ListAPIView):
    """
    Return the list of public data files.
    """

    queryset = DataFile.objects.public()
    serializer_class = PublicDataFileSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = PublicDataFileFilter
