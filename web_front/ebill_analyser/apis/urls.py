from django.conf.urls import url
from apis import views

urlpatterns = [
    url(r'^ebill$', views.ebills_list),
    url(r'^ebill/(?P<number>[0-9]+)$', views.mobile_records),
    url(r'^book$', views.books),
    url(r'^order$', views.order),
]
