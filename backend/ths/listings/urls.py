from django.urls import path

from .views import AssignmentCreate, ListingList

urlpatterns = [path("", ListingList.as_view()), path("", AssignmentCreate.as_view())]
