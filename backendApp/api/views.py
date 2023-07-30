# views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializer import StockSerializer
from .models import Stock
from .scrapperService import startRendering
import threading

# GET API to retrieve all stocks data
@api_view(['GET'])
def get_stocks(request):
    if request.method == 'GET':
        stocks = Stock.objects.all().order_by('stock_id')
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_stocks_by_id(request, stock_id):
    if request.method == 'GET':
        try:
            stock = Stock.objects.get(stock_id=stock_id)
            data = {
                'stock_id': stock.stock_id,
                'name': stock.name
            }
            return JsonResponse(data)
        except Stock.DoesNotExist:
            return JsonResponse({'stock_id': '0'}, status=404)
        
    
@api_view(['GET'])
def update_stock_data(request, pageNumber=1):
    if request.method == 'GET':
        try: 
            startRenderThread = threading.Thread(target=startRendering, args=(pageNumber,))
            startRenderThread.start()
            return Response({'message': 'rendering started'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'failed to start rendering'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_stock(request):
    if request.method == 'POST':
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE API to update a specific stock's data
@api_view(['PUT'])
def update_stock(request, stock_id):
    try:
        stock = Stock.objects.get(stock_id=stock_id)
    except Stock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
