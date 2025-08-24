from rest_framework import generics

from .models import Listing
from .serializers import ListingSerializer


class ListingList(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return Listing.objects.all().prefetch_related("pets", "assignments")
