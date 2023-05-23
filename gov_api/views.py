from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from .models import ProductModel
from .serializers import ProductSerializer
import math
from datetime import datetime
# Create your views here.


class Products(generics.GenericAPIView):
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        products = ProductModel.objects.all()
        total_products = products.count()
        if search_param:
            products = products.filter(title__icontains=search_param)
        serializer = self.serializer_class(
            products[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_products,
            "page": page_num,
            "last_page": math.ceil(total_products / limit_num),
            "notes": serializer.data
        })
