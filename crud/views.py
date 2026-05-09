from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password


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
     userObj = Users.objects.select_related('gender')

     data ={
         'users': userObj
     }

     return render(request, 'layout/user/UserList.html', data) 
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

      #if password != confirmPassword:

      Users.objects.create(
        full_name=fullname,
        gender=Genders.objects.get(pk=gender),
        birth_date=birthdate,
        address=address,
        contact_number=contactnumber,
        email=email,
        username=username,
        password=make_password(password)
      ).save()

      messages.success(request, 'User added successfully')
      return redirect('/user/add')
      
    else:
      genderObj = Genders.objects.all()

    data = {
        'genders': genderObj
    }

    return render(request, 'layout/user/AddUser.html', data)
  except Exception as e:
      return HttpResponse(f'Error occured during add user: {e}')
    