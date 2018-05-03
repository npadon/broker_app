from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Survey, Requirement, TourBook, ExecutiveSummary, MediaUpload
from .tourbook_pdf import TourBookPDF


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


survey_fields = ['building_name',
                 'building_address',
                 'zipcode',
                 'building_size_RSF',
                 'building_number_of_floors',
                 'building_avg_floor_size',
                 'subject_space_floors',
                 'subject_space_size_RSF',
                 'quoted_net_rental_rate_USD_per_RSF',
                 'estimated_yearly_operating_expenses_USD',
                 'annual_increase_in_net_rental_rate_USD',
                 'quoted_improvement_allowance_USD',
                 'quoted_free_rent_months_CNT',
                 'quoted_free_rent_basis',
                 'building_reserved_parking_ratio',
                 'building_reserved_parking_rates_USD_per_DAY',
                 'building_unreserved_parking_ratio',
                 'building_unreserved_parking_rates_USD_per_DAY',
                 'supplemental_garage_reserved_parking_rates_USD_per_DAY',
                 'supplemental_garage_unreserved_parking_ratio',
                 'supplemental_garage_unreserved_parking_rates_USD_per_DAY',
                 'subject_space_former_use',
                 'subject_space_existing_condition',
                 'building_capital_improvements',
                 'other_notes']


# Surveys
class SurveyCreate(CreateView):
    model = Survey
    fields = survey_fields


class SurveyUpdate(UpdateView):
    model = Survey
    fields = survey_fields

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
    fields = ['tour_title', 'tour_date', 'surveys']


class TourBookUpdate(UpdateView):
    model = TourBook
    fields = ['tour_title', 'tour_date', 'surveys']

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


@login_required
def tourbook_pdf_view(request, pk):
    tour_book = get_object_or_404(TourBook, pk=pk)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tourbook{}.pdf"'.format(pk)
    buffer = BytesIO()
    # Create the PDF object, using the BytesIO object as its "file."
    pdf = TourBookPDF(buffer, 'Letter', tour_book).generate_pdf()
    response.write(pdf)
    return response


class MediaFileCreateView(CreateView):
    model = MediaUpload
    fields = ['upload', ]
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_files = MediaUpload.objects.all()
        context['media_files'] = media_files
        return context
