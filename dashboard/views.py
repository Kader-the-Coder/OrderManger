from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from accounts.models import CustomUser, Company
from .models import CompanyInvitation


@login_required
def dashboard(request):
    user = request.user
    company = getattr(user, 'company', None)
    invitations = CompanyInvitation.objects.filter(invited_user=user, accepted=False)
    context = {
        'company': company,
        'invitations': invitations,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@require_POST
def create_company(request):
    name = request.POST.get('name')
    user = request.user
    if not name:
        messages.error(request, "Company name cannot be empty.")
        return redirect('dashboard:dashboard')

    company = Company.objects.create(name=name, owner=user)
    company.members.add(user)
    user.company = company
    user.save()
    messages.success(request, f"Company '{name}' created.")
    return redirect('dashboard:dashboard')


@login_required
@require_POST
def leave_company(request):
    user = request.user
    company = getattr(user, 'company', None)

    if not company:
        messages.error(request, "You are not in a company.")
        return redirect('dashboard:dashboard')

    if company.members.count() == 1:
        company.delete()
        messages.success(request, "You left and the company was deleted as you were the last member.")
    else:
        company.members.remove(user)
        if company.owner == user:
            new_owner = company.members.first()
            company.owner = new_owner
            company.save()
        messages.success(request, "You left the company.")

    user.company = None
    user.save()
    return redirect('dashboard:dashboard')


@login_required
@require_POST
def delete_company(request):
    user = request.user
    company = getattr(user, 'company', None)

    if not company or company.owner != user:
        messages.error(request, "You are not authorized to delete this company.")
        return redirect('dashboard:dashboard')

    company.delete()
    user.company = None
    user.save()
    messages.success(request, "Company deleted.")
    return redirect('dashboard:dashboard')


@login_required
@require_POST
def invite_user(request):
    email = request.POST.get('email')
    user = request.user
    company = getattr(user, 'company', None)

    if not company:
        messages.error(request, "You are not in a company.")
        return redirect('dashboard:dashboard')

    try:
        invited_user = CustomUser.objects.get(email=email)
        if invited_user.company == company:
            messages.warning(request, "User is already in your company.")
        else:
            CompanyInvitation.objects.create(company=company, invited_user=invited_user, invited_by=user)
            messages.success(request, f"Invitation sent to {email}.")
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")

    return redirect('dashboard:dashboard')


@login_required
@require_POST
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(CompanyInvitation, id=invitation_id, invited_user=request.user)
    company = invitation.company
    invitation.accepted = True
    invitation.save()
    company.members.add(request.user)
    request.user.company = company
    request.user.save()
    messages.success(request, f"You joined '{company.name}'.")
    return redirect('dashboard:dashboard')
