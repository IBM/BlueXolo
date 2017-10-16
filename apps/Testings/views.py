from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView

from apps.Testings.models import Keyword, Collection
from apps.Testings.forms import CollectionForm


class KeyWordsView(LoginRequiredMixin, TemplateView):
    template_name = "keywords.html"


class NewKeywordView(LoginRequiredMixin, TemplateView):
    template_name = "create-keyword.html"


class DeleteKeywordView(LoginRequiredMixin, DeleteView):
    template_name = "delete-keyword.html"
    model = Keyword
    success_url = reverse_lazy('keywords')


class CollectionsView(LoginRequiredMixin, TemplateView):
    template_name = "collections.html"


class NewCollectionsView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = "create-edit-collection.html"

    def get_success_url(self):
        messages.success(self.request, "Collection Created")
        return reverse_lazy('collections')

    def get_context_data(self, **kwargs):
        context = super(NewCollectionsView, self).get_context_data(**kwargs)
        context['title'] = "New Collection"
        return context


class EditCollectionsView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = "create-edit-collection.html"

    def get_success_url(self):
        messages.success(self.request, "Collection Edited")
        return reverse_lazy('collections')

    def get_context_data(self, **kwargs):
        context = super(EditCollectionsView, self).get_context_data(**kwargs)
        context['title'] = "Edit Collections"
        return context


class DeleteCollectionsView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = "delete-collections.html"

    def get_success_url(self):
        messages.success(self.request, "Colletions Deleted")
        return reverse_lazy('collections')
