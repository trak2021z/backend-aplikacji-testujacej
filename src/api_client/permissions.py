from rest_framework.permissions import BasePermission


class APIPermission(BasePermission):
    def has_permission(self, request, view):
        return 'FRONT' in request.headers and request.headers['FRONT'] == 'CvjbjbqnCbyvohqnFrxfzhmlxnCbyvgrpuavxn'