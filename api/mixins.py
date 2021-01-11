from rest_framework import viewsets, permissions

from .permissions import IsAdminOrAuthor

class PermissionMixin(viewsets.ModelViewSet):
    action_permissions = {'list': [permissions.AllowAny],
                          'create': [permissions.IsAuthenticated],
                          'destroy': [IsAdminOrAuthor], 
                          'retrieve': [permissions.AllowAny],
                          'partial_update': [IsAdminOrAuthor]}
    
    def get_permissions(self):
        return [permission() for permission in self.action_permissions[self.action]]