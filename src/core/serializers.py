from rest_framework import serializers
from .models import Course , User , Document , Flashcard

class FlashcardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flashcard
        fields = '__all__'
        
class DocumentSerializer(serializers.ModelSerializer):
    flashcards = FlashcardSerializer(many=True)
    
    class Meta:
        model = Document
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        
class CourseSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True , read_only= True)

    class Meta:
        model = Course
        fields = '__all__'

