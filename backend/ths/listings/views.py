from rest_framework import generics

from .models import Assignment, Listing
from .serializers import AssignmentSerializer, ListingSerializer


class ListingList(generics.ListAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()


class AssignmentCreate(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
