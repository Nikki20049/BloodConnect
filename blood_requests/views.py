from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import BloodRequest, Comment
from .forms import BloodRequestForm, CommentForm, RequestStatusForm
from accounts.models import BloodGroup, User
from notifications.utils import create_notification, notify_donors

@login_required
def create_blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            
            # Notify nearby donors with matching blood group
            notify_donors(blood_request)
            
            messages.success(request, 'Blood request created successfully!')
            return redirect('view_request', request_id=blood_request.id)
    else:
        form = BloodRequestForm()
    
    return render(request, 'requests/create_request.html', {'form': form})

def view_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    donations = blood_request.donations.all()
    comments = Comment.objects.filter(blood_request=blood_request).order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blood_request = blood_request
            comment.save()
            
            # Notify the requester about the new comment
            if comment.user != blood_request.requester:
                create_notification(
                    recipient=blood_request.requester,
                    notification_type='comment',
                    title='New comment on your request',
                    message=f'{comment.user.username} commented on your blood request.',
                    related_request=blood_request
                )
            
            return redirect('view_request', request_id=request_id)
    else:
        comment_form = CommentForm()
    
    # Check if the request is expired
    if blood_request.status == 'pending' and blood_request.is_expired():
        blood_request.status = 'expired'
        blood_request.save()
    
    # Status update form for admins/NGOs
    status_form = None
    if request.user.is_authenticated and request.user.user_type in ['admin', 'ngo']:
        status_form = RequestStatusForm(instance=blood_request)
    
    context = {
        'blood_request': blood_request,
        'donations': donations,
        'comments': comments,
        'comment_form': comment_form,
        'status_form': status_form,
    }
    return render(request, 'requests/request_detail.html', context)

def update_request_status(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    # Allow only admins, NGO users, or the original requester
    if request.user.user_type not in ['admin', 'ngo'] and request.user != blood_request.requester:
        messages.error(request, 'You do not have permission to update request status.')
        return redirect('view_request', request_id=request_id)

    if request.method == 'POST':
        form = RequestStatusForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            
            # Notify the requester about the status change
            create_notification(
                recipient=blood_request.requester,
                notification_type='request',
                title='Blood Request Status Updated',
                message=f'Your blood request status has been updated to {blood_request.get_status_display()}.',
                related_request=blood_request
            )
            
            messages.success(request, 'Request status updated successfully.')

    return redirect('view_request', request_id=request_id)


@login_required
def my_requests(request):
    requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'requests/my_requests.html', {'requests': requests})

def search_requests(request):
    query = request.GET.get('q', '')
    blood_group = request.GET.get('blood_group', '')
    urgency = request.GET.get('urgency', '')
    status = request.GET.get('status', 'pending')
    
    requests = BloodRequest.objects.all()
    
    if query:
        requests = requests.filter(
            Q(hospital_name__icontains=query) |
            Q(hospital_address__icontains=query) |
            Q(patient_name__icontains=query) |
            Q(reason__icontains=query)
        )
    
    if blood_group:
        requests = requests.filter(blood_group__name=blood_group)
    
    if urgency:
        requests = requests.filter(urgency=urgency)
    
    if status:
        requests = requests.filter(status=status)
    
    # Update expired requests
    now = timezone.now()
    expired_requests = requests.filter(status='pending', needed_by__lt=now)
    for req in expired_requests:
        req.status = 'expired'
        req.save()
    
    context = {
        'requests': requests.order_by('-created_at'),
        'blood_groups': BloodGroup.objects.all(),
        'query': query,
        'selected_blood_group': blood_group,
        'selected_urgency': urgency,
        'selected_status': status,
    }
    return render(request, 'requests/search_requests.html', context)