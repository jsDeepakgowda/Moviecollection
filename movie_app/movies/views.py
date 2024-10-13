import requests
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status, permissions
from .models import Collection, Movie
from .serializers import CollectionSerializer, MovieSerializer
from .middleware import RequestCounterMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication

MOVIE_API_URL = "https://demo.credy.in/api/v1/maya/movies/"
USERNAME = os.getenv('MOVIE_API_USERNAME')
PASSWORD = os.getenv('MOVIE_API_PASSWORD')

def fetch_movies_from_api():
    try:
        response = requests.get(MOVIE_API_URL, auth=(USERNAME, PASSWORD), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            print("Unauthorized: Check your username and password.")
        else:
            print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies: {e}")
    return None


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['GET'])
def get_movies(request):
    data = fetch_movies_from_api()
    if data is None:
        return Response({'error': 'Could not fetch movies at this time. Please try again later.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        movies_data = data.pop('movies', [])
        
        collection = Collection.objects.create(user=user, **data)
        
        for movie_data in movies_data:
            Movie.objects.create(collection=collection, **movie_data)
        
        serializer = self.get_serializer(collection)
        return Response({'collection_uuid': collection.pk}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        
        if 'title' in data:
            instance.title = data['title']
        if 'description' in data:
            instance.description = data['description']
        instance.save()

        if 'movies' in data:
            movies_data = data['movies']
            instance.movies.all().delete()
            for movie_data in movies_data:
                Movie.objects.create(collection=instance, **movie_data)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Collection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def request_count(request):
    with RequestCounterMiddleware.lock:
        count = RequestCounterMiddleware.count
    return Response({'requests': count})

@api_view(['POST'])
def reset_request_count(request):
    with RequestCounterMiddleware.lock:
        RequestCounterMiddleware.count = 0
    return Response({'message': 'Request count reset successfully'})
