from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserCreateForm, UserUpdateForm

# Create your views here.
def sign_up(request):
    if request.method=='POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else :
        form = UserCreateForm()
    context ={
        'form':form }
    return render(request,'users/sign_up.html',context)

@login_required
def profile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("chat")
    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context ={
        'u_form':u_form,
        'p_form': p_form}   
    return render(request,'users/profile.html',context)