from rest_framework.response import Response
from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size' #used in get rquest filtering i.e ?page_size=2 
    # Set to an integer to limit the maximum page size the client may request.
    max_page_size = None
    
   
    def get_paginated_response(self, data):
        return Response({
            'pagination':{
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                    },
                'count': self.page.paginator.count,
                'num_pages': self.page.paginator.num_pages,
                'page_range': list(self.page.paginator.page_range),
                'start_index':self.page.start_index(),
                'end_index':self.page.end_index(),
            },
            'results': data
        })