from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "children",
        )

    def get_children(self, obj):
        return CategorySerializer(obj.get_children(),many=True).data

    # def get_children(self, obj):
    #     return CategorySerializer(obj.get_ancestors(ascending=False, include_self=False), many=True).data
    #
    # def get_children(self, obj):
    #     return CategorySerializer(obj.get_descendants(include_self=False), many=True).data
    # def get_children(self, obj):
    #     return CategorySerializer(obj.get_root(), many=True).data


class CategoryWantSerializer(CategorySerializer):
    wants = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        model = CategorySerializer.Meta.model
        fields = CategorySerializer.fields

    #
    # def get_wants(self, obj):
    #
