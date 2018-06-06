from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from .models import LandlordResponse, Requirement, TourBook, ExecutiveSummary, MediaUpload, Building
from .tourbook_ppt import TourBookPPT
from django.contrib.auth import login, authenticate


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'broker_app/signup.html', {'form': form})


@login_required
def index(request):
    landlord_responses = LandlordResponse.objects.all()
    requirements = Requirement.objects.order_by('name_of_tenant')[:5]
    tour_books = TourBook.objects.order_by('tour_title')[:5]
    executive_summaries = ExecutiveSummary.objects.order_by('title')[:5]
    buildings = Building.objects.all()

    context = {'landlord_responses': landlord_responses,
               'requirements': requirements,
               'tour_books': tour_books,
               'executive_summaries': executive_summaries,
               'buildings': buildings}

    return render(request, 'broker_app/index.html', context)


def email_requirement(request, pk):
    requirement = get_object_or_404(TourBook, pk=pk)
    context = {'requirement': requirement}
    return render(request, 'broker_app/email_requirement.html', context)


building_fields = [
    'building_name',
    'building_address',
    'zipcode',
    'building_size_RSF',
    'building_number_of_floors',
    'building_avg_floor_size',
    'building_reserved_parking_ratio',
    'building_reserved_parking_rates_USD_per_DAY',
    'building_unreserved_parking_ratio',
    'building_unreserved_parking_rates_USD_per_DAY',
    'supplemental_garage_reserved_parking_rates_USD_per_DAY',
    'supplemental_garage_unreserved_parking_ratio',
    'supplemental_garage_unreserved_parking_rates_USD_per_DAY',
    'building_capital_improvements'
]
landlord_response_fields = [
    'requirement',
    'building',
    'subject_space_floors',
    'subject_space_size_RSF',
    'quoted_net_rental_rate_USD_per_RSF',
    'estimated_yearly_operating_expenses_USD',
    'annual_increase_in_net_rental_rate_USD',
    'quoted_improvement_allowance_USD',
    'quoted_free_rent_months_CNT',
    'quoted_free_rent_basis',
    'subject_space_former_use',
    'subject_space_existing_condition',
    'other_notes']

requirement_fields = [
    'name_of_tenant',
    'type_of_tenant',
    'commencement_date',
    'term_length_YRS',
    'submarket_CBD',
    'submarket_Greenway',
    'submarket_Galleria',
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


# Building
class BuildingCreate(CreateView):
    model = Building
    fields = building_fields
    template_name = 'broker_app\generic_add_form.html'


class BuildingUpdate(UpdateView):
    model = Building
    fields = building_fields
    template_name = 'broker_app\generic_update_form.html'


class BuildingDelete(DeleteView):
    model = Building
    template_name = 'broker_app\generic_confirm_delete.html'
    success_url = reverse_lazy('index')


# Landlord Responses
class LandlordReponseCreate(CreateView):
    model = LandlordResponse
    fields = landlord_response_fields

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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
    fields = ['tour_title', 'tour_date', 'landlord_reponses']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TourBookUpdate(UpdateView):
    model = TourBook
    fields = ['tour_title', 'tour_date', 'landlord_reponses']

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

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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
        form.instance.landlordresponse = LandlordResponse.objects.get(pk=self.kwargs['landlordresponse_pk'])
        return super(MediaFileCreateView, self).form_valid(form)

    def get_success_url(self):
        # this currently returns the user to the page where they were modifying the survey media
        return self.request.POST['success_url']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['landlordresponse_pk'] = self.kwargs.get('landlordresponse_pk')

        # show only media objects related to this survey
        media_files = MediaUpload.objects.filter(landlord_response=context['landlordresponse_pk'])
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
