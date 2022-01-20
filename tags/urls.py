from tags import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#Declaro o defino la ruta que quiero para mis tags
#Y Ademas cargo la clase del viewset
router.register(r'api/v1/tags', views.TagViewSet)
urlpatterns = router.urls