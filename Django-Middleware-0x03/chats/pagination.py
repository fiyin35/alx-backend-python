from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination as DRFLimitOffsetPagination


class StandardResultsPagination(PageNumberPagination):
    """
    Standard pagination class using page number style.
    """
    page_size = 20  
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        """
        Optionally use page.paginator.count in response
        """
        return super().get_paginated_response(data)  # or override and use page.paginator.count if needed


class CustomLimitOffsetPagination(DRFLimitOffsetPagination):
    """
    Custom limit-offset pagination class.
    """
    default_limit = 10
    max_limit = 50
