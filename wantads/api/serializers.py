from rest_framework import serializers

from categories.api.serializers import CategorySerializer

from ..models import Bookmark, Image, Note, WantAd


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class WandAdSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField("want_ad:detail", lookup_field="pk")
    categories = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = WantAd
        fields = (
            "url",
            "id",
            "user",
            "title",
            "description",
            "active_chat",
            "categories",
            "city",
            "zone",
            "confirmed",
            "lat",
            "long",
            "show_phone",
            "data",
            "special",
            "images",
        )
        read_only_fields = ("id", "user", "images")
        # depth = 1
        # depth=1  show all info for relational fields

        #

    def get_categories(self, obj):
        return CategorySerializer(obj.category).data

    def get_images(self, obj):
        return ImageSerializer(obj.images.all(), many=True).data


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("user", "text", "want")
        read_only_fields = ("user",)


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("user", "want")
        read_only_fields = ("user",)

        
        
        
        
class WandAdCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = WantAd
        fields = (
            'id',
            'title',
            'description',
            'active_chat',
            'category',
            'city',
            'zone',
            'lat',
            'long',
            'show_phone',
            'data',
        )
        read_only_fields = ('id',)        
