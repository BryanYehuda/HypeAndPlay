from . import views

from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register("category", views.CategoryViewset, basename = "category")
router.register("promo", views.PromoViewset, basename="promo")
router.register("product", views.ProductViewset, basename="product")
router.register("adbanner", views.AdBannerViewset, basename = "banner")

urlpatterns += router.urls