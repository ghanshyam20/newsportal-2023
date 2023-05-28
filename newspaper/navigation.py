from newspaper.models import Post,Category,Tag
def navigation(request):
    categories = Category.objects.all()[0:5]
    tags = Tag.objects.all()[0:10]
    trending_posts = Post.objects.filter(
            status="active", published_at__isnull=False
        ).order_by("-views_count")[:4]
    return {
            "categories":categories,
            "tags":tags,
            "trending_posts":trending_posts,
        }