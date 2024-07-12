from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stocks.views import StockViewSet

app_name = 'stocks'

router = DefaultRouter()
router.register(r'stocks', StockViewSet)

urlpatterns = [
    # path('get_stocks/', ..., name='Получить имеющиеся запасы'),
    # path('get_stock/<int:pk>', ..., name='Получить конкретный товар'),
    # path('fill_stocks/', ..., name='Заполнение запасов'),
    # path('update_stocks/<int:pk>', ..., name='Обновление текущих запасов'),
    # path('delete_stocks/<int:pk>', ..., name='Удаление запасов')
    path('', include(router.urls)),
]
