from django.contrib.auth.views import FormView
from django.core import serializers
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from news_app.decorators import superuser_required
from news_app.forms.PostCreationForm import PostCreationForm
from news_app.forms.PostEditForm import PostEditForm
from news_app.models import News


class PostListView(ListView):
    """
    Список всех APPROVED новостей
    """
    model = News
    # Под данным именем наш список статей будет доступен в шаблоне
    context_object_name = 'news'
    extra_context = {
        'title': 'Новости',
    }
    paginate_by = 3
    ordering = ['-created_at']

    # Название шаблона
    template_name = 'news_app/news_list.html'

    def get_queryset(self):
        search_news = self.request.GET.get('search')
        if search_news:
            return News.objects.filter(status='APPROVED').filter(
                Q(title__icontains=search_news) |
                Q(topic__icontains=search_news) |
                Q(text__icontains=search_news)
            ).order_by(*self.ordering)
        return News.objects.filter(status='APPROVED').order_by(*self.ordering)


class PostDetailView(DetailView):
    """
    Одна новость
    """

    model = News

    queryset = News.objects.all()
    # Под данным именем наш список статей будет доступен в шаблоне
    context_object_name = 'post'

    # Название шаблона
    template_name = 'news_app/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = self.get_object().title
        context['post_data'] = serializers.serialize("python",
                                                     [self.get_object()])
        return context


@method_decorator(superuser_required, name='get')
class PostCreationView(FormView):
    template_name = 'news_app/post_create_or_update.html'
    form_class = PostCreationForm
    extra_context = {
        'title': 'Создание новости',
    }

    def get(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        post = News(
            title=request.POST.get('title'),
            text=request.POST.get('text'),
            topic=request.POST.get('topic'),
            status=request.POST.get('status'),
            photo=request.POST.get('photo'),
        )
        if request.FILES:
            photo = request.FILES['photo']
            photo_path = f'news_image/{request.POST.get("title")}.png'
            with default_storage.open(photo_path, 'wb+') as f:
                for chunk in photo.chunks():
                    f.write(chunk)
            post.photo = photo_path

        post.save()
        return HttpResponseRedirect(reverse('news_app:news'))


@method_decorator(superuser_required, name='get')
class PostEditView(UpdateView):
    template_name = 'news_app/post_create_or_update.html'
    queryset = News.objects.all()
    model = News
    form_class = PostEditForm
    success_url = reverse_lazy('news_app:news')
    extra_context = {
        'title': 'редактирование новости'
    }


@method_decorator(superuser_required, name='get')
class PostDeleteView(DeleteView):
    model = News
    template_name = 'news_app/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('news_app:news')
    extra_context = {
        'title': 'удаление новости'
    }
