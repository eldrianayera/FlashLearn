from rest_framework import serializers
from .models import Course , User , Document , Flashcard

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        
class DocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Document
        fields = '__all__'


class FlashcardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flashcard
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

