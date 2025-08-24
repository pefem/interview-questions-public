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
        """
        Method will validate the start_date to ensure its greater than the current date.
        """

        if value <= date.today():
            raise serializers.ValidationError(
                "Start date must be greater than today's date."
            )
        return value

    def validate(self, data):
        """
        Method will validate provided dates against exsiting dates to check for overlap.
        """
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
