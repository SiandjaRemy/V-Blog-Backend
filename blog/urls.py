from django.urls import path, include

from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("posts", views.PostModelViewset, basename="posts")
router.register("category", views.CategoryGenericViewset, basename="category")
router.register("subscriber", views.SubscriberModelViewset, basename="subscriber")

post_router = routers.NestedDefaultRouter(router, "posts", lookup="posts")
post_router.register("comments", views.CommentModelViewset, basename="comments")
post_router.register("reactions", views.ReactionGenericViewset, basename="reactions")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(post_router.urls)),
]