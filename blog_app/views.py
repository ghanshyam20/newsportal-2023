from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    DetailView,
    CreateView,
    UpdateView,
    View,
)


from newspaper.models import Post
from blog_app.forms import PostForm


# CRUD
# c->create
# R->Read/retrieve
# U->update
# D->delete


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("news-admin:draft-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# def post_create(request):
#     form = PostForm()
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()

#             return redirect("draft-list")

#     return render(request, "post_create.html", {"form": form})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")

   


class PostDetailView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    def get_queryset(self):
        queryset = Post.objects.filter(
            pk=self.kwargs.get["pk"], published_at__isnull=False
            
        )
        return queryset


class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = "blog/draft_detail.html"
    context_object_name = "drafts"
    queryset=Post.objects.filter(published_at__isnull=True).order_by("-published_at")


    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=True).order_by(
            "-published_at"
        )


class DraftDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = "blog/draft_detail.html"
    context_object_name = "draft"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"

    def get_success_url(self):
        post = self.get_object()  # jun post update gardai xam tei post leko ho

        if post.published_at:
            return reverse_lazy("news-admin:post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("news-admin:draft-detail", kwargs={"pk": post.pk})


# class PostUpdate(LoginRequiredMixin,View):
#     def get(self, request, pk, *args, **kwargs):
#         post = Post.objects.get(pk=pk)
#         form = PostForm(instance=post)
#         return render(
#             request,
#             "post_create.html",
#             {"form": form},
#         )
#     def post(self,request,pk,*args,**kwargs):
#         post=Post.objects.get(pk=pk)
#         form=PostForm(
#             request.POST,instance=post

#         )#frontend bata ako data haleko form ma
#         if form.is_valid():
#             post.save()
#             if post.published_at:
#                 return redirect{"post-detail",post.pk}
#             else:
#                 return redirect("draft-detail",post.pk)
#         else:
#             return render{
#                 request,"post_create.html",
#             }


class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk, published_at__isnull=False)
        post.delete()
        return redirect("news-admin:post-list")


class DraftDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        draft = Post.objects.get(pk=pk, published_at__isnull=True)
        draft.delete()
        return redirect("news-admin:draft-list")


# def post_update(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostForm(instance=post)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             if post.published_at:
#                 return redirect("post-detail", post.pk)

#             else:
#                 return redirect("draft-detail", post.pk)
#             return redirect("post-detail", post.pk)
#     return render(request, "post_create.html", {"form": form})


class DraftPublishView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        draft = Post.objects.get(pk=pk, published_at__isnull=True)
        draft.published_at = timezone.now()
        draft.save()
        return redirect("post-detail", draft.pk)




