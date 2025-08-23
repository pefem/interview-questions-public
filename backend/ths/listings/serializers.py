from datetime import date

from rest_framework import serializers

from .models import Assignment, Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["first_name", "last_name", "pets", "assignments"]


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["id", "start_date", "end_date", "listing"]

    def validate_start_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("Start date must be tomorrow or later.")
        return value

    def validate_assignment(self, data):
        listing = data.get("listing")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if listing and start_date and end_date:
            overlapping = Assignment.objects.filter(
                listing=listing,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if overlapping.exists():
                raise serializers.ValidationError(
                    "This assignment overlaps with an existing assignment."
                )
        return data
