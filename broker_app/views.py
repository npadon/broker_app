from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Survey, Requirement, TourBook, ExecutiveSummary


@login_required
def index(request):
    surveys = Survey.objects.order_by('building_name')[:5]
    requirements = Requirement.objects.order_by('name_of_tenant')[:5]
    tour_books = TourBook.objects.order_by('tour_title')[:5]
    executive_summaries = ExecutiveSummary.objects.order_by('title')[:5]

    context = {'surveys': surveys,
               'requirements': requirements,
               'tour_books': tour_books,
               'executive_summaries': executive_summaries}
    return render(request, 'broker_app/index.html', context)


# Surveys
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


# Requirements
class RequirementsCreate(CreateView):
    model = Requirement
    fields = ['name_of_tenant', 'type_of_tenant', 'building_class', 'minimum_rsf', 'maximum_rsf']


class RequirementsUpdate(UpdateView):
    model = Requirement
    fields = ['name_of_tenant', 'type_of_tenant', 'building_class', 'minimum_rsf', 'maximum_rsf']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RequirementsDelete(DeleteView):
    model = Requirement
    success_url = reverse_lazy('index')


# TourBooks
class TourBookCreate(CreateView):
    model = TourBook
    fields = ['tour_title', 'tour_date']


class TourBookUpdate(UpdateView):
    model = TourBook
    fields = ['tour_title', 'tour_date']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TourBookDelete(DeleteView):
    model = TourBook
    success_url = reverse_lazy('index')


# Executive Summary
class ExecutiveSummaryCreate(CreateView):
    model = ExecutiveSummary
    fields = ['title', 'notes']


class ExecutiveSummaryUpdate(UpdateView):
    model = ExecutiveSummary
    fields = ['title', 'notes']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ExecutiveSummaryDelete(DeleteView):
    model = ExecutiveSummary
    success_url = reverse_lazy('index')
