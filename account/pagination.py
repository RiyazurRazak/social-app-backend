from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return ({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_count': self.page.paginator.count,
            'results': data
        })