from newsletters import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#Declaro o defino la ruta que quiero para mis newsletters
#Y Ademas cargo la clase del viewset
router.register(r'api/v1/newsletters', views.NewsViewSet)
urlpatterns = router.urls