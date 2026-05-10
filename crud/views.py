from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.paginator import Paginator



# Gender List
def gender_list(request):
    try:
        genders = Genders.objects.all()

        data = {
            'genders': genders
        }

        return render(request, 'layout/gender/GendersList.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')


# Add Gender
def add_gender(request):
    try:
        if request.method == 'POST':

            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender)

            messages.success(request, 'Gender added successfully!')

            return redirect('/gender/list')

        else:
            return render(request, 'layout/gender/AddGender.html')

    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')


# Edit Gender
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':

            genderObj = Genders.objects.get(pk=genderId)

            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')

            return redirect('/gender/list')

        else:

            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj
            }

            return render(request, 'layout/gender/EditGender.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')


# Delete Gender
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':

            genderObj = Genders.objects.get(pk=genderId)

            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')

            return redirect('/gender/list')

        else:

            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj
            }

            return render(request, 'layout/gender/DeleteGender.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')
    
def user_list(request):
    try:

        search = request.GET.get('search')

        userObj = Users.objects.select_related('gender')

        if search:
            userObj = userObj.filter(
                Q(full_name__icontains=search) |
                Q(email=search) |
                Q(address=search)
            )

             # PAGINATION
        paginator = Paginator(userObj, 15)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {
            'users': page_obj,
            'page_obj': page_obj,
            'search': search
        }

        return render(request, 'layout/user/UserList.html', context)

       

        
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')        
    
def add_user(request):
    try:
        if request.method == 'POST':

            fullname = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactnumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            profile = request.FILES.get('profile', None)
            
            # REQUIRED VALIDATION
            if not fullname or not gender or not birthdate or not username or not password:
                messages.error(request, 'Please fill all required fields.')
                return redirect('/user/add')

        # USERNAME UNIQUE
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('/user/add')

            if password != confirmPassword:
                messages.error(request, 'Password does not match')
                return redirect('/user/add')

            Users.objects.create(
                full_name=fullname,
                profile=profile,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthdate,
                address=address,
                contact_number=contactnumber,
                email=email,
                username=username,
                password=make_password(password)
            )

            messages.success(request, 'User added successfully')

            return redirect('/user/list')

        else:

            genderObj = Genders.objects.all()

            data = {
                'genders': genderObj
            }

            return render(request, 'layout/user/AddUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during add user: {e}')
    
def edit_user(request, userId):
    userObj = Users.objects.get(pk=userId)

    if request.method == 'POST':
        userObj.full_name = request.POST.get('full_name')
        userObj.birth_date = request.POST.get('birth_date')
        userObj.address = request.POST.get('address')
        userObj.contact_number = request.POST.get('contact_number')
        userObj.email = request.POST.get('email')

        profile = request.FILES.get('profile')
        if profile:
            userObj.profile = profile

        userObj.save()
        return redirect('/user/list')

    data = {'user': userObj}
    return render(request, 'layout/user/EditUser.html', data)

def delete_user(request, userId):
    userObj = Users.objects.get(pk=userId)

    if request.method == 'POST':
        userObj.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('/user/list')

    data = {
        'user': userObj
    }

    return render(request, 'layout/user/DeleteUser.html', data)