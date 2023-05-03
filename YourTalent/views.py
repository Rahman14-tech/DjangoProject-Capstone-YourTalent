from enum import unique
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random
import json
import os

from mysqlx import Auth

from .models import *
choice = [
    "contentcreator",
    "recruiter"
]
genre = [
    'Dance',
    'Music',
    'Illustration',
    'Programming'
]
# Create your views here.
def index(request):
    return render(request,"YourTalent/index.html")
def login_place(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                current_auth = Authentication.objects.get(user_authentication = user,boolean_authenticate = True)
            except Authentication.DoesNotExist:
                return HttpResponseRedirect(reverse("authenticate",kwargs={'username':username}))
            login(request, user)
            return HttpResponseRedirect(reverse("home",kwargs={'username':username}))
        else:
            return render(request, "YourTalent/login.html", {
                "error": "Invalid username and/or password."
            })
    else:
        return render(request,"YourTalent/login.html")
def logout_place(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        if len(username) < 5:
            return render(request,"YourTalent/register.html",{
                            "error":"Username must have at least 5 characters."
                        }) 
        email = request.POST['email']
        try:
            database_email = User.objects.get(email = email)
        except User.DoesNotExist:
            valid_email = False
            if len(email) < 3:
                return render(request,"YourTalent/register.html",{
                        "error":"Email must be a valid email."
                    }) 
            for char_email in email:
                if char_email == '@':
                    valid_email = True
                    break
            if valid_email != True:
                return render(request,"YourTalent/register.html",{
                    "error":"Email must be a valid email."
                }) 
            password = request.POST['password']
            if len(password) < 8:
                return render(request,"YourTalent/register.html",{
                    "error":"Password must have at least 8 characters"
                })
            confirmation = request.POST['confirmation']
            if password != confirmation:
                return render(request,"YourTalent/register.html",{
                    "error":"Password and confirmation not match."
                })
            option = request.POST['optradio']
            if option not in choice:
                    return render(request,"YourTalent/register.html",{
                    "error":"There is no such option of role."
                })
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
            except IntegrityError:
                return render(request,"YourTalent/register.html",{
                "error":"Username has already been taken."
                })
            authentication_code = random.randint(100000, 999999)
            user_authentication = Authentication(user_authentication = user, boolean_authenticate = False, authentication_code = authentication_code,role = option)
            user_authentication.save()
            send_mail(
                    'Authentication code for YourTalent account',
                    f'Your authentication code is {authentication_code}',
                    'yourtalent765@gmail.com',
                    [email],
                    fail_silently=False,
                )
            return HttpResponseRedirect(reverse("authenticate",kwargs={'username':username}))
        return render(request,"YourTalent/register.html",{
                "error":"Email has already been taken."
            })
    else:
        return render(request,"YourTalent/register.html")
def authentication(request,username):
    if request.method == 'POST':
        try:
            current_user = User.objects.get(username = username)
        except User.DoesNotExist:
            return render(request,"YourTalent/error.html",{
                "error":"User not found."
            })
        try:
            current_auth = Authentication.objects.get(user_authentication = current_user,boolean_authenticate = False)
        except Authentication.DoesNotExist:
              return render(request,"YourTalent/error.html",{
                "error":"User not found or already authenticated."
            })
        authenticationcode = request.POST['authenticationcode']
        if int(authenticationcode) != int(current_auth.authentication_code):
            return render(request,"YourTalent/authenticate.html",{
                "username":username,
                "error":"Authentcation code not match."
            })
        current_auth.boolean_authenticate = True
        current_auth.save()
        login(request, current_user)
        return HttpResponseRedirect(reverse("home",kwargs={'username':username}))
    else:
        try:
            current_user = User.objects.get(username = username)
        except User.DoesNotExist:
            return render(request,"YourTalent/error.html",{
                "error":"User not found."
            })
        try:
            current_auth = Authentication.objects.get(user_authentication = current_user,boolean_authenticate = False)
        except Authentication.DoesNotExist:
              return render(request,"YourTalent/error.html",{
                "error":"User not found or already authenticated."
            })
        return render(request,"YourTalent/authenticate.html",{
            "username":username,
        })

@csrf_exempt
def authenticateapi(request,username):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            current_user = User.objects.get(username = data['username'])
        except User.DoesNotExist:
            return JsonResponse({'error':'There is no such user.'})
        try:
            current_auth = Authentication.objects.get(user_authentication = current_user,boolean_authenticate = False)
        except Authentication.DoesNotExist:
            return JsonResponse({'error':'There is no such user or user has already been verified.'})
        new_code = random.randint(100000, 999999)
        current_auth.authentication_code = new_code
        current_auth.save()
        send_mail(
                    'Authentication code for YourTalent account',
                    f'Your authentication code is {new_code}',
                    'yourtalent765@gmail.com',
                    [current_user.email],
                    fail_silently=False,
                )
        return HttpResponse(status=204)
    return JsonResponse({"username":f"{username}"})
@login_required(login_url='login')   
def home(request,username):
    if request.method == 'POST':
        if 'content_creator_part' in request.POST:
            Title = request.POST['title']
            Description = request.POST['description']
            Category = request.POST['optioncate']
            if Category not in genre:
                return render (request,'YourTalent/home.html',{
                        'username':username,
                        'genres':genre,
                        'error':"Category doesn't exist"
                })
            try:
                creation = request.FILES["filecreation"]
            except AttributeError:
                return render (request,'YourTalent/home.html',{
                        'username':username,
                        'genres':genre,
                        'error':"Inputed the wrong form."
                })
            if Category == 'Illustration' or Category == 'Music':
                Data = Novidpart(creator = request.user,title = Title, description = Description, category = Category,file = creation )
                file_path = os.path.splitext(f'{Data.file}')
                file_extension = file_path[1]
                if Category == 'Illustration':
                    if file_extension == '.png' or file_extension == '.jpg':
                        Data.save()
                    else:
                        return render (request,'YourTalent/home.html',{
                            'username':username,
                            'genres':genre,
                            'error':"The supported file for illustration are (png,jpg)."
                        })
                elif Category == 'Music':
                    if file_extension == '.mp3':
                        Data.save()
                    else:
                        return render (request,'YourTalent/home.html',{
                            'username':username,
                            'genres':genre,
                            'error':"The supported file for music is mp3."
                        })
            elif Category == 'Dance' or Category == 'Programming':
                url = request.POST['thumbnail']
                result = url.split('?v=')
                in_error = False
                try:
                    videoid = result[1].split('&ab')
                except IndexError:
                    videoid = url.split('/')
                    in_error = True
                if in_error:
                    Data = Vidpart(creator = request.user, title = Title, description = Description, category = Category,thumbnail = creation,videoid = videoid[3])
                else:
                    Data = Vidpart(creator = request.user, title = Title, description = Description, category = Category,thumbnail = creation,videoid = videoid[0])
                file_path = os.path.splitext(f'{Data.thumbnail}')
                file_extension = file_path[1]
                if Category == 'Dance' or Category == 'Programming':
                    if file_extension == '.png' or file_extension == '.jpg':
                        Data.save()
                    else:
                        return render (request,'YourTalent/home.html',{
                            'username':username,
                            'genres':genre,
                            'error':"The supported file thumbnail for Dance or Programming are (png,jpg)."
                        })
        if 'recruit_now' in request.POST:
            the_creator = request.POST['the_creator']
            try:
                the_creatorfinal = User.objects.get(username = the_creator)
            except User.DoesNotExist:
                return render (request,'YourTalent/error.html',{
                        'error':"User not found."
                })
            the_category = request.POST['the_category']
            if the_category not in genre:
                return render (request,'YourTalent/error.html',{
                        'error':"Category not exist."
                })
            the_content = request.POST['the_content']
            if the_category == 'Illustration' or the_category == 'Music':
                try:
                    the_content_final = Novidpart.objects.get(title = the_content,creator = the_creatorfinal)
                except Novidpart.DoesNotExist:
                    return render (request,'YourTalent/error.html',{
                        'error':"Content not exist."
                    })
            elif the_category == 'Dance' or the_category == 'Programming':
                try:
                    the_content_final = Vidpart.objects.get(title = the_content,creator = the_creatorfinal)
                except Vidpart.DoesNotExist:
                    return render (request,'YourTalent/error.html',{
                        'error':"Content not exist."
                    })
            new_notif = Notifications(notif_recruiter = request.user,  notif_contencreator = the_creatorfinal, notif_thecontent_title = the_content, category = the_category, content_id = the_content_final.id, seen = False)
            new_notif.save()
            recruitment_code = random.randint(100000, 999999999)
            recruitment_code_str = str(recruitment_code)
            recruitment_code_final = the_creatorfinal.username + recruitment_code_str
            send_mail(
                    f'Congratulation!,{request.user.username} has just recruited you.',
                    f'Congratulation! You just got recruited from the content of \'{the_content_final.title}\' to contact the recruiter you can contact the following gmail {request.user.email} and don\'t forget to screenshot this email to have a proof that you have been recruited. And here is your recruitement code {recruitment_code_final} make sure to send it to the recruitement as well to identify you are the real one.',
                    'yourtalent765@gmail.com',
                    [the_creatorfinal.email],
                    fail_silently=False,
                )
            send_mail(
                    f'Congratulation!,you just recruited {the_creatorfinal.username}.',
                    f'Congratulation! You just recruited from the content of \'{the_content_final.title}\' the contentcreator will contact you from gmail he/she/they will give you the screenshot of the gmail and the recruitement code of {recruitment_code_final}.',
                    'yourtalent765@gmail.com',
                    [request.user.email],
                    fail_silently=False,
                )
            return render(request,'YourTalent/success.html',{
                'success':f"Successfully to recruit {the_creatorfinal.username} from the {the_content} content"
            })
        return render(request,'YourTalent/success.html',{
            'success':"Successfully upload yourtalent. the content can only be seen by the recruiter."
        })
    else:
        try:
            current_user = User.objects.get(username = username)
        except User.DoesNotExist:
            return render(request,'YourTalent/error.html',{
                'error':'User Does Not Exist.'
            })
        if current_user != request.user:
            return render(request,'YourTalent/error.html',{
                'error':'You don\'t have access to the following page.'
            })
        try:
            user_role = Authentication.objects.get(user_authentication = current_user,boolean_authenticate = True)
        except Authentication.DoesNotExist:
            return render(request,'YourTalent/error.html',{
                'error':'User Does Not Exist or Not Authenticated Yet.'
            })
        Contents = None
        Contents_cat = None
        if 'category' in request.GET:
            Contents_cat = request.GET['category']
            if Contents_cat == 'Illustration' or Contents_cat == 'Music':
                try:
                    Contents = Novidpart.objects.filter(category = Contents_cat).order_by("-id")
                except Novidpart.DoesNotExist:
                    return render (request,'YourTalent/home.html',{
                            'role':user_role.role,
                            'genres':genre,
                            "no_content":"There is content yet."
                    })
            elif Contents_cat == 'Dance' or Contents_cat == 'Programming':
                try:
                    Contents = Vidpart.objects.filter(category = Contents_cat).order_by("-id")
                except Vidpart.DoesNotExist:
                    return render (request,'YourTalent/home.html',{
                            'role':user_role.role,
                            'genres':genre,
                            "no_content":"There is content yet."
                    })
        if user_role.role == 'recruiter':
            return render (request,'YourTalent/home.html',{
                    'role':user_role.role,
                    'genres':genre,
                    'Contents':Contents,
                    'username':request.user.username,
                    'Contents_cat':Contents_cat
            })
        zero_new_notification = False
        try:
            notifications = Notifications.objects.filter(notif_contencreator = request.user,seen = False).order_by("-id")
        except Notifications.DoesNotExist:
            zero_new_notification = True
        if len(notifications) == 0:
            zero_new_notification = True
        return render (request,'YourTalent/home.html',{
                    'role':user_role.role,
                    'genres':genre,
                    'username':username,
                    'notifications':notifications,
                    'zero_new_notification':zero_new_notification
            })
@login_required(login_url='login')  
def viewcontent(request,category,id):
    if request.method == 'POST':
        the_creator = request.POST['the_creator']
        try:
            the_creatorfinal = User.objects.get(username = the_creator)
        except User.DoesNotExist:
            return render (request,'YourTalent/error.html',{
                    'error':"User not found."
            })
        the_category = request.POST['the_category']
        if the_category not in genre:
            return render (request,'YourTalent/error.html',{
                    'error':"Category not exist."
            })
        the_content = request.POST['the_content']
        if the_category == 'Illustration' or the_category == 'Music':
            try:
                the_content_final = Novidpart.objects.get(title = the_content,creator = the_creatorfinal)
            except Novidpart.DoesNotExist:
                return render (request,'YourTalent/error.html',{
                    'error':"Content not exist."
                })
        elif the_category == 'Dance' or the_category == 'Programming':
            try:
                the_content_final = Vidpart.objects.get(title = the_content,creator = the_creatorfinal)
            except Vidpart.DoesNotExist:
                return render (request,'YourTalent/error.html',{
                    'error':"Content not exist."
                })
        new_notif = Notifications(notif_recruiter = request.user,  notif_contencreator = the_creatorfinal, notif_thecontent_title = the_content, category = the_category, content_id = the_content_final.id, seen = False)
        new_notif.save()
        recruitment_code = random.randint(100000, 999999999)
        recruitment_code_str = str(recruitment_code)
        recruitment_code_final = the_creatorfinal.username + recruitment_code_str
        send_mail(
                f'Congratulation!,{request.user.username} has just recruited you.',
                f'Congratulation! You just got recruited from the content of \'{the_content_final.title}\' to contact the recruiter you can contact the following gmail {request.user.email} and don\'t forget to screenshot this email to have a proof that you have been recruited. And here is your recruitement code {recruitment_code_final} make sure to send it to the recruitement as well to identify you are the real one.',
                'yourtalent765@gmail.com',
                [the_creatorfinal.email],
                fail_silently=False,
            )
        send_mail(
                f'Congratulation!,you just recruited {the_creatorfinal.username}.',
                f'Congratulation! You just recruited from the content of \'{the_content_final.title}\' the contentcreator will contact you from gmail he/she/they will give you the screenshot of the gmail and the recruitement code of {recruitment_code_final}.',
                'yourtalent765@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
        return render(request,'YourTalent/success.html',{
            'success':f"Successfully to recruit {the_creatorfinal.username} from the {the_content} content"
        })
    else:
        try:
            user_role = Authentication.objects.get(user_authentication = request.user,boolean_authenticate = True)
        except Authentication.DoesNotExist:
            return render(request,'YourTalent/error.html',{
                'error':'User Does Not Exist or Not Authenticated Yet.'
            })
        if category == 'Dance' or category == 'Programming':
            try:
                Content = Vidpart.objects.get(id = id)
            except Vidpart.DoesNotExist:
                return render(request,'YourTalent/error.html',{
                'error':'Content doesn\'t exist.'
                })
            try:
                interest = Interestvidpart.objects.get(interest_vid = Content, interest_recruiter = request.user,category = category)
            except Interestvidpart.DoesNotExist:
                interest = None
        elif category == 'Illustration':
            try:
                Content = Novidpart.objects.get(id = id,category = category)
            except Novidpart.DoesNotExist:
                return render(request,'YourTalent/error.html',{
                'error':'Content doesn\'t exist.'
                }) 
            try:
                interest = Interestnovidpart.objects.get(interest_file = Content, interest_recruiter = request.user,category = category)
            except Interestnovidpart.DoesNotExist:
                interest = None
        return render(request,'YourTalent/view.html',{
            'role':user_role.role,
            'Content':Content,
            'category':category,
            'interest':interest
        })
@login_required(login_url='login')
def mycontents(request,username):
    try:
        current_user = User.objects.get(username = username)
    except User.DoesNotExist:
        return render(request,'YourTalent/error.html',{
            'error':'User Does Not Exist.'
        })
    if current_user != request.user:
        return render(request,'YourTalent/error.html',{
            'error':'You don\'t have access to the following page.'
        })
    try:
        user_role = Authentication.objects.get(user_authentication = current_user,boolean_authenticate = True)
    except Authentication.DoesNotExist:
        return render(request,'YourTalent/error.html',{
            'error':'User Does Not Exist or Not Authenticated Yet.'
        })
    Contents = None
    Contents_cat = None
    if 'category' in request.GET:
        Contents_cat = request.GET['category']
        if Contents_cat == 'Illustration' or Contents_cat == 'Music':
            try:
                Contents = Novidpart.objects.filter(creator = request.user,category = Contents_cat).order_by("-id")
            except Novidpart.DoesNotExist:
                return render (request,'YourTalent/mycontents.html',{
                        'role':user_role.role,
                        'genres':genre,
                        "no_content":"There is content yet."
                })
        elif Contents_cat == 'Dance' or Contents_cat == 'Programming':
            try:
                Contents = Vidpart.objects.filter(creator = request.user,category = Contents_cat).order_by("-id")
            except Vidpart.DoesNotExist:
                return render (request,'YourTalent/mycontents.html',{
                        'role':user_role.role,
                        'genres':genre,
                        "no_content":"There is content yet."
                })
    zero_new_notification = False
    try:
        notifications = Notifications.objects.filter(notif_contencreator = request.user,seen = False).order_by("-id")
    except Notifications.DoesNotExist:
        zero_new_notification = True
    if len(notifications) == 0:
        zero_new_notification = True
    if user_role.role == 'contentcreator':
        return render (request,'YourTalent/mycontents.html',{
                'role':user_role.role,
                'genres':genre,
                'Contents':Contents,
                'username':request.user.username,
                'Contents_cat':Contents_cat,
                'notifications':notifications,
                'zero_new_notification':zero_new_notification
        })
    return render(request,'YourTalent/error.html',{
        'error':'You are not allowed to this page.'
    })
@login_required(login_url='login')
@csrf_exempt
def interest_content(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Content_id = data.get("Content_id","")
        Category = data.get("Category","")
        if Category not in genre:
            return JsonResponse({"error":"The category is undefined."})
        if Category == 'Dance' or Category == 'Programming':
            try:
                Data_vid = Vidpart.objects.get(id = Content_id)
            except Vidpart.DoesNotExist:
                return JsonResponse({"error":"The content is undefined."})
            try:
                uniqueness = Interestvidpart.objects.get(interest_recruiter = request.user,interest_vid = Data_vid,category = Category)
            except Interestvidpart.DoesNotExist:
                new_interest = Interestvidpart(interest_recruiter = request.user,interest_vid = Data_vid, category = Category)
                new_interest.save()
                return JsonResponse({"success":"Interest has been added."})
            pass
        elif Category == 'Illustration' or Category == 'Music':
            try:
                Data_file = Novidpart.objects.get(id = Content_id,category = Category)
            except Novidpart.DoesNotExist:
                return JsonResponse({"error":"The content is undefined."})
            try:
                uniqueness = Interestnovidpart.objects.get(interest_recruiter = request.user,interest_file = Data_file,category = Category)
            except Interestnovidpart.DoesNotExist:
                new_interest = Interestnovidpart(interest_recruiter = request.user,interest_file = Data_file,category = Category)
                new_interest.save()
                return JsonResponse({"success":"Interest has been added."})
            pass
        return JsonResponse({"error":"Interest failed to be added."})
    elif request.method == 'GET':
        try:
            interest = Interestnovidpart.objects.filter(interest_recruiter = request.user).order_by("-id")
        except Interestnovidpart.DoesNotExist:
            return JsonResponse({"content_id":"error_no_content!@#$%."})
        return JsonResponse([inter.serialize()  for inter in interest],safe = False)
@login_required(login_url='login')
@csrf_exempt
def uninterest_content(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    Content_id = data.get("Content_id","")
    Category = data.get("Category","")
    if Category not in genre:
        return JsonResponse({"error":"The category is undefined."})
    if Category == 'Dance' or Category == 'Programming':
        try:
            Data_vid = Vidpart.objects.get(id = Content_id, category = Category)
        except Vidpart.DoesNotExist:
            return JsonResponse({"error":"The content is undefined."})
        try:
            interest = Interestvidpart.objects.get(interest_recruiter = request.user, interest_vid = Data_vid,category = Category)
        except Interestvidpart.DoesNotExist:
            return JsonResponse({"error":"The content is already uninterested."})
        interest.delete()
        return JsonResponse({"success":"Interest has been removed."})
    elif Category == 'Illustration' or Category == 'Music':
        try:
            Data_file = Novidpart.objects.get(id = Content_id,category = Category)
        except Novidpart.DoesNotExist:
            return JsonResponse({"error":"The content is undefined."})
        try:
            interest = Interestnovidpart.objects.get(interest_recruiter = request.user, interest_file = Data_file,category = Category)
        except Novidpart.DoesNotExist:
            return JsonResponse({"error":"The content is already uninterested."})
        interest.delete()
        return JsonResponse({"success":"Interest has been removed."})        
    return JsonResponse({"error":"Interest failed to be added."})
@login_required(login_url='login')
def interest(request,username):
    if request.method == 'POST':
        the_creator = request.POST['the_creator']
        try:
            the_creatorfinal = User.objects.get(username = the_creator)
        except User.DoesNotExist:
            return render (request,'YourTalent/error.html',{
                    'error':"User not found."
            })
        the_category = request.POST['the_category']
        if the_category not in genre:
            return render (request,'YourTalent/error.html',{
                    'error':"Category not exist."
            })
        the_content = request.POST['the_content']
        if the_category == 'Illustration' or the_category == 'Music':
            try:
                the_content_final = Novidpart.objects.get(title = the_content,creator = the_creatorfinal)
            except Novidpart.DoesNotExist:
                return render (request,'YourTalent/error.html',{
                    'error':"Content not exist."
                })
        elif the_category == 'Dance' or the_category == 'Programming':
            try:
                the_content_final = Vidpart.objects.get(title = the_content,creator = the_creatorfinal)
            except Vidpart.DoesNotExist:
                return render (request,'YourTalent/error.html',{
                    'error':"Content not exist."
                })
        new_notif = Notifications(notif_recruiter = request.user,  notif_contencreator = the_creatorfinal, notif_thecontent_title = the_content, category = the_category, content_id = the_content_final.id, seen = False)
        new_notif.save()
        recruitment_code = random.randint(100000, 999999999)
        recruitment_code_str = str(recruitment_code)
        recruitment_code_final = the_creatorfinal.username + recruitment_code_str
        send_mail(
                f'Congratulation!,{request.user.username} has just recruited you.',
                f'Congratulation! You just got recruited from the content of \'{the_content_final.title}\' to contact the recruiter you can contact the following gmail {request.user.email} and don\'t forget to screenshot this email to have a proof that you have been recruited. And here is your recruitement code {recruitment_code_final} make sure to send it to the recruitement as well to identify you are the real one.',
                'yourtalent765@gmail.com',
                [the_creatorfinal.email],
                fail_silently=False,
            )
        send_mail(
                f'Congratulation!,you just recruited {the_creatorfinal.username}.',
                f'Congratulation! You just recruited from the content of \'{the_content_final.title}\' the contentcreator will contact you from gmail he/she/they will give you the screenshot of the gmail and the recruitement code of {recruitment_code_final}.',
                'yourtalent765@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
        return render(request,'YourTalent/success.html',{
            'success':f"Successfully to recruit {the_creatorfinal.username} from the {the_content} content"
        })
    else:
        try:
            current_user = User.objects.get(username = username)
        except User.DoesNotExist:
            return render(request,'YourTalent/error.html',{
                'error':'User Does Not Exist.'
            })
        if current_user != request.user:
            return render(request,'YourTalent/error.html',{
                'error':'You don\'t have access to the following page.'
            })
        try:
            user_role = Authentication.objects.get(user_authentication = current_user,boolean_authenticate = True)
        except Authentication.DoesNotExist:
            return render(request,'YourTalent/error.html',{
                'error':'User Does Not Exist or Not Authenticated Yet.'
            })
        Contents = None
        Contents_cat = None
        if 'category' in request.GET:
            Contents_cat = request.GET['category']
            if Contents_cat == 'Illustration' or Contents_cat == 'Music':
                try:
                    Contents = Interestnovidpart.objects.filter(interest_recruiter = request.user,category = Contents_cat).order_by("-id")
                except Interestnovidpart.DoesNotExist:
                    return render (request,'YourTalent/interest.html',{
                            'role':user_role.role,
                            'genres':genre,
                            "no_content":"There is content yet."
                    })
            elif Contents_cat == 'Dance' or Contents_cat == 'Programming':
                try:
                    Contents = Interestvidpart.objects.filter(interest_recruiter = request.user,category = Contents_cat).order_by("-id")
                except Interestvidpart.DoesNotExist:
                    return render (request,'YourTalent/interest.html',{
                            'role':user_role.role,
                            'genres':genre,
                            "no_content":"There is content yet."
                    })
        return render (request,'YourTalent/interest.html',{
                'role':user_role.role,
                'genres':genre,
                'Contents':Contents,
                'username':request.user.username,
                'Contents_cat':Contents_cat,
        })
@login_required(login_url='login')
@csrf_exempt
def notifapi(request,id):
    try:
        role = Authentication.objects.get(user_authentication = request.user,boolean_authenticate = True)
    except Authentication.DoesNotExist:
        return JsonResponse({'error':'User doesn\'t exist or not authenticated'})
    if role.role == 'recruiter':
        return JsonResponse({'error':'You\'re not authenticated to receive data'})
    try:
        notifications = Notifications.objects.get(notif_contencreator = request.user,seen = False,id = id)
    except Notifications.DoesNotExist:
        return JsonResponse({'error':'No new'})
    if request.method == "PUT":
        new_data = json.loads(request.body)
        notifications.seen = new_data["seen"]
        notifications.save()
    return HttpResponse(status=204)
@login_required(login_url='login')
@csrf_exempt
def delete_content(request,id,category):
    try:
        role = Authentication.objects.get(user_authentication = request.user,boolean_authenticate = True)
    except Authentication.DoesNotExist:
        return JsonResponse({'error':'User doesn\'t exist or not authenticated'}) 
    if role.role == 'recruiter':
        return JsonResponse({'error':'You\'re not authenticated to receive data'})
    data = json.loads(request.body)
    if data['category'] == 'Music' or data['category'] == 'Illustration':
        try:
            content = Novidpart.objects.get(creator = request.user, category = category,id = id)
        except Novidpart.DoesNotExist:
            return JsonResponse({'error':'You\'re not authenticated to receive data'})
    elif data['category'] == 'Dance' or data['category'] == 'Programming':
        try:
            content = Vidpart.objects.get(creator = request.user, category = category,id = id)
        except Vidpart.DoesNotExist:
            return JsonResponse({'error':'You\'re not authenticated to receive data'})
    content.delete()
    return HttpResponse(status=204)
     