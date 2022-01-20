from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from users.serializers import UserSerializer
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from newsletters.models import Newsletter
from newsletters.serializers import NewsletterSerializer
from votes.models import Vote
from users.pagination import StandardResultsSetPagination
from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated
 )


class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
    def newsletters(self, request, pk=None):
        user = self.get_object()
    # 6. Como usuario quiero iniciar sesión para poder ver los boletines a los que estoy suscrito.
        if request.method== 'GET':
            id = Newsletter.objects.filter(users=int(user.id))
            serialized = NewsletterSerializer(id, many=True)
            return Response(status=status.HTTP_200_OK, data=serialized.data)
    # 4. Como usuario quiero poder suscribirme a un boletín para recibir noticias relacionadas en mi correo.
        if request.method=='POST':
            id_user = user.id 
            newsletters_id = request.data['id']
            for newsletter_id in newsletters_id:
                newsletter = Newsletter.objects.get(id=int(newsletter_id))
                newsletter.users.add(id_user)
            return Response(status = status.HTTP_201_CREATED)
    # 7. Como usuario quiero poder darme de baja de los boletines para dejar de recibir noticias.
        if request.method=='DELETE':
            id_user = user.id 
            newsletters_id = request.data['id']
            for newsletter_id in newsletters_id:
                newsletter = Newsletter.objects.get(id=int(newsletter_id))
                newsletter.users.remove(id_user)
            return Response(status = status.HTTP_204_NO_CONTENT)