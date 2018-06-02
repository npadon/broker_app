from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import LandlordResponse, Requirement, TourBook, ExecutiveSummary, MediaUpload
from .tourbook_pdf import TourBookPDF
from .tourbook_ppt import TourBookPPT


@login_required
def index(request):
    landlord_responses = LandlordResponse.objects.order_by('building_name')[:5]
    requirements = Requirement.objects.order_by('name_of_tenant')[:5]
    tour_books = TourBook.objects.order_by('tour_title')[:5]
    executive_summaries = ExecutiveSummary.objects.order_by('title')[:5]

    context = {'landlord_responses': landlord_responses,
               'requirements': requirements,
               'tour_books': tour_books,
               'executive_summaries': executive_summaries}
    return render(request, 'broker_app/index.html', context)


def email_requirement(request, pk):
    requirement = get_object_or_404(TourBook, pk=pk)
    context = {'requirement': requirement}
    return render(request, 'broker_app/email_requirement.html', context)


landlord_response_fields = [
    'requirement',
    'building_name',
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

requirement_fields = ['name_of_tenant',
                      'type_of_tenant',
                      'commencement_date',
                      'term_length_YRS',
                      'submarket_A',
                      'submarket_B',
                      'submarket_C',
                      'submarket_D',
                      'building_class_A',
                      'building_class_B',
                      'building_class_C',
                      'minimum_rsf',
                      'maximum_rsf',
                      'lease_or_purchase',
                      'desired_percentage_offices_PCT',
                      'needs_furniture',
                      'notes',
                      ]


# Landlord Responses
class LandlordReponseCreate(CreateView):
    model = LandlordResponse
    fields = landlord_response_fields


class LandlordResponseUpdate(UpdateView):
    model = LandlordResponse
    fields = landlord_response_fields

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LandlordResponseDelete(DeleteView):
    model = LandlordResponse
    template_name = 'broker_app\generic_confirm_delete.html'

    success_url = reverse_lazy('index')


# Requirements
class RequirementsCreate(CreateView):
    model = Requirement
    fields = requirement_fields


class RequirementsUpdate(UpdateView):
    model = Requirement
    fields = requirement_fields

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RequirementsDelete(DeleteView):
    model = Requirement
    template_name = 'broker_app\generic_confirm_delete.html'

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
    template_name = 'broker_app\generic_confirm_delete.html'

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
    template_name = 'broker_app\generic_confirm_delete.html'

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


@login_required
def tourbook_ppt_view(request, pk):
    tour_book = get_object_or_404(TourBook, pk=pk)
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
    response['Content-Disposition'] = 'attachment; filename="tourbook_{}.pptx"'.format(pk)

    buffer = BytesIO()
    tour_book_ppt = TourBookPPT(buffer, tour_book)

    ppt_buffer = tour_book_ppt.generate_ppt()

    response.write(ppt_buffer)
    return response


class MediaFileCreateView(CreateView):
    model = MediaUpload
    fields = ['upload', 'upload_type']

    def form_valid(self, form):
        form.instance.survey = LandlordResponse.objects.get(pk=self.kwargs['survey_pk'])
        return super(MediaFileCreateView, self).form_valid(form)

    def get_success_url(self):
        # this currently returns the user to the page where they were modifying the survey media
        return self.request.POST['success_url']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey_pk'] = self.kwargs.get('survey_pk')

        # show only media objects related to this survey
        media_files = MediaUpload.objects.filter(survey=context['survey_pk'])
        context['media_files'] = media_files

        return context


class MediaFileDeleteView(DeleteView):
    model = MediaUpload

    success_url = reverse_lazy('index')

    # override delete method to additionally delete files from S3 after deleted from the Model
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        filename = self.object.upload.name
        self.object.delete()
        if default_storage.exists(filename):
            default_storage.delete(filename)
        return HttpResponseRedirect(success_url)

    template_name = 'broker_app\generic_confirm_delete.html'
