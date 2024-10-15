from rest_framework import serializers
from .models import User, Store, Product, Variant, Music, Video


## A. Serializers for taking data from the user and converting it into storable db format
# 1. USER - can be used for both storing and retrieving user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
# 2. STORE - can be used for both storing and retrieving store data
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

# 3. VARIANT - helper function, can be used for both storing and retrieving variant data directly also
class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

# 4. PRODUCT - usable only for storing data as we need to show the response instead of primary key while viewing the product
class ProductSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    variants = VariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        # Extract the nested variants data from the validated_data
        variants_data = validated_data.pop('variants', [])

        # Create the product
        product = Product.objects.create(**validated_data)

        # Handle variants if provided
        for variant_data in variants_data:
            variant, created = Variant.objects.get_or_create(**variant_data)  # Create or get the variant
            product.variants.add(variant)  # Add variant to product's ManyToMany relationship

        return product

# 5. MUSIC - can be used for both storing and retrieving music data
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

# 6. VIDEO - usable only for storing data as we need to show the response instead of primary key while viewing the video
class VideoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, required=False)
    music = serializers.PrimaryKeyRelatedField(queryset=Music.objects.all(), required=False)

    class Meta:
        model = Video
        fields = '__all__'


## B. Serializers for viewing angle
# 1. VIEW PRODUCT - for viewing the product data in a more readable format
class ViewProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

# 2. VIEW VIDEO - for viewing the video data in a more readable format
class ViewVideoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = ViewProductSerializer(many=True)
    music = MusicSerializer()

    class Meta:
        model = Video
        fields = '__all__'