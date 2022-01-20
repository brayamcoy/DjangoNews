from newsletters.serializers import NewsletterSerializer
from newsletters.models import Newsletter
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from tags.serializers import TagSerializer
from tags.models import Tag
from users.models import User
from votes.serializers import VoteSerializer
from votes.models import Vote
from users.serializers import UserSerializer
from newsletters.pagination import StandardResultsSetPagination
from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated
 )

#2. Poder ver la listas de boletines creados y ver su categoria#

class NewsViewSet(viewsets.ModelViewSet):

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = ( IsAuthenticated,)
    
    #Paginación y busqueda
    def get_queryset(self):
        query = {}
        for item in self.request.query_params:
            if item not in ['page_size']:
                continue
                if item in ['users', 'tags']:
                    query[item + '__id'] = self.request.query_params[item]
                    continue
                query[item + '__icontains'] = self.request.query_params[item]
        self.queryset = self.queryset.filter(**query)
        return super().get_queryset()

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)

    def tags(self, request, pk=None):
        newsletter = self.get_object()
        if request.method== 'GET':
            serialized = TagSerializer(newsletter.tags, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)

        if request.method== 'POST':
            newsletter_id = request.data['tags']
            for tag_id in newsletter_id:
                tag = Tag.objects.get(id=int(tag_id))
                newsletter.tags.add(tag)
            return Response(status = status.HTTP_201_CREATED)

        if request.method== 'DELETE':
            newsletter_id = request.data['tags']
            for tag_id in newsletter_id:
                tag = Tag.objects.get(id=int(tag_id))
                newsletter.tags.remove(tag)
            return Response(status = status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True)

    def users(self, request, pk=None):
    #3. Como administrador quiero poder invitar a nuevos administradores para editar los boletines
        newsletter = self.get_object()
        users_id = request.data['id']
        
        for user_id in users_id:
            user = User.objects.get(id=int(user_id))
            newsletter.users.add(user_id)
        return Response(status = status.HTTP_201_CREATED)
    
    #Visualizar los votos de cada boletin
    @action(methods=['GET'], detail=True)
    def votes(self, request, pk=None):
        newsletter = self.get_object()
        votes = Vote.objects.filter(newsletter=int(newsletter.id))
        serialized = VoteSerializer(votes, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized.data)