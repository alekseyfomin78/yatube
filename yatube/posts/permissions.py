from rest_framework.permissions import BasePermission


# проверка, что ресурс (пост, коммент) принадлежит текущему пользователю
# проверка осуществляется на методы PUT, PATCH, DELETE
class OwnResourcePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user == obj.author
        return True
