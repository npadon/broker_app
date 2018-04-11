from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render
from .models import Survey
from django.views import generic


@login_required
def index(request):
    surveys = Survey.objects.order_by('building_name')[:5]
    template = loader.get_template('index.html')
    context = {'surveys': surveys, }
    return render(request, 'index.html', context)


class SurveyDetailView(generic.DetailView):
    model = Survey
    template_name = 'list_surveys.html'