from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict
from .models import Product


class ResultPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        task_id = self.request.GET.get("task_id")
        task_data = Product.objects.filter(task_id=task_id).first()
        if len(data) == 0:
            if task_data.comment == "":
                task_data.comment = "Data is None"
            return Response(
                OrderedDict(
                    [
                        ("task_id", task_data.task_id),
                        ("Error", task_data.comment),
                        ("Comment", task_data.comment),
                    ]
                )
            )
        else:
            result = [
                ("task_id", task_data.task_id),
                ("count", self.page.paginator.count),
                ("status", task_data.status),
                ("total_calls", task_data.calls),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
            if task_data.type == "realtime":
                result.insert(2, ("cursor", task_data.cursor))
            return Response(OrderedDict(result))
