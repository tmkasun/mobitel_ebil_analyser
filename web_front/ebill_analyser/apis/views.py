from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from home.models import Ebill
from apis.serializers import EbillSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def ebills_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        ebills = Ebill.objects.all()
        serializer = EbillSerializer(ebills, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def mobile_records(request, number):
    query = "this.number == {}".format(number)
    try:
        record = Ebill.objects.where(query)
    except Ebill.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EbillSerializer(list(record), many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def books(request):
    if request.method == 'POST':
        data = {
            'success': True
        }
        return JSONResponse(data)
    data = [
        {
            "id": "978-0641723445",
            "cat": ["book", "hardcover"],
            "name": "The Lightning Thief",
            "author": "Rick Riordan",
            "series_t": "Percy Jackson and the Olympians",
            "genre_s": "fantasy",
            "inStock": True,
            "price": 12.50,
            "pages": 384
        }
        ,
        {
            "id": "978-1423103349",
            "cat": ["book", "paperback"],
            "name": "The Sea of Monsters",
            "author": "Rick Riordan",
            "series_t": "Percy Jackson and the Olympians",
            "genre_s": "fantasy",
            "inStock": True,
            "price": 6.49,
            "pages": 304
        }
        ,
        {
            "id": "978-1857995879",
            "cat": ["book", "paperback"],
            "name": "Sophie's World : The Greek Philosophers",
            "author": "Jostein Gaarder",
            "genre_s": "fantasy",
            "inStock": True,
            "price": 3.07,
            "pages": 64
        }
        ,
        {
            "id": "978-1933988177",
            "cat": ["book", "paperback"],
            "name": "Lucene in Action, Second Edition",
            "author": "Michael McCandless",
            "genre_s": "IT",
            "inStock": True,
            "price": 30.50,
            "pages": 475
        }
    ]
    return JSONResponse(data)


@csrf_exempt
def order(request):
    data = [{
        "ID": "1234",
        "Buyer": "Kasun",
        "Price": "13.40$"
    }, {
        "ID": "1235",
        "Buyer": "Thennakoon",
        "Price": "26.75$"
    }]
    return JSONResponse(data)
