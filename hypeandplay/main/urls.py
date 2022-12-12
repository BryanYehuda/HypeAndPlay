from . import views

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


from django.urls import path
urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name='token_obtain_pain'),
    path("token/refresh/", TokenRefreshView.as_view(), name = 'token_refresh'),
    
]

router = DefaultRouter()
router.register("category", views.CategoryViewset, basename = "category")
router.register("promo", views.PromoViewset, basename="promo")
router.register("product", views.ProductViewset, basename="product")
router.register("adbanner", views.AdBannerViewset, basename = "banner")
router.register("event", views.EventViewset, basename = "event")
router.register("register", views.RegisterView, basename = "register")
router.register('cart', views.CartViewset, basename="cart")
# router.register("login", views.LoginViewset, basename = "login")
# router.register("sign-up", views.SignUpViewset, basename = "signup")

urlpatterns += router.urls