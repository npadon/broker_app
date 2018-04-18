from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Survey


@login_required
def index(request):
    surveys = Survey.objects.order_by('building_name')[:5]
    context = {'surveys': surveys, }
    return render(request, 'index.html', context)


@login_required
class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'list_surveys.html'


class SurveyCreate(CreateView):
    model = Survey
    fields = ['building_name', 'building_address', 'zipcode']


class SurveyUpdate(UpdateView):
    model = Survey
    fields = ['building_name', 'building_address', 'zipcode']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SurveyDelete(DeleteView):
    model = Survey
    success_url = reverse_lazy('index')
