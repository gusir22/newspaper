# articles/views.py
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    UpdateView,
    DeleteView,
    CreateView,
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Article, Comment


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    context_object_name = 'article'

    def test_func(self):
        """Tests if object author is the same as the user requesting the data to authorize access to view"""
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    context_object_name = 'article'

    def test_func(self):
        """Tests if object author is the same as the user requesting the data to authorize access to view"""
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body', )
    context_object_name = 'articles'

    def form_valid(self, form):
        form.instance.author = self.request.user  # automatically sets the current user as the author of the article
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_new.html'
    fields = ('comment', )
    context_object_name = 'comment'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        article_id = self.kwargs['pk']
        article = get_object_or_404(Article, id=article_id)
        kwargs['initial'] = {'article': article}
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user  # automatically sets the current user as the author of the comment

        # Retrieve the article pk from URL and autoassign the article to the new comment
        article_id = self.kwargs['pk']  # 'pk' was assigned as variable name in the url routing
        article = get_object_or_404(Article, id=article_id)
        form.instance.article = article

        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('article_list')
    context_object_name = 'comment'

    def test_func(self):
        """Tests if object author is the same as the user requesting the data to authorize access to view"""
        obj = self.get_object()
        return obj.author == self.request.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('comment',)
    template_name = 'comment_edit.html'
    context_object_name = 'comment'

    def test_func(self):
        """Tests if object author is the same as the user requesting the data to authorize access to view"""
        obj = self.get_object()
        return obj.author == self.request.user
