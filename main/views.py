from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from main.forms import RegisterForm
from main.models import medicament

@login_required(login_url='/pharmacy/login')
def home(request):
    return render(request, 'main/home.html')

def sign_up(request):
    if request.method == "POST":
        Vemail = request.POST.get('email')
        Vusername = request.POST.get('username').strip()
        Vpassword1 = request.POST.get('password1')
        Vpassword2 = request.POST.get('password2')
        
        if Vpassword1 != Vpassword2:
            return render(request, 'registration/sign_up.html', {'error':True, 'username':Vusername, 'email':Vemail})
        else:
            form = RegisterForm(request.POST)
            verify = User.objects.filter(username = Vusername, email__icontains = Vemail).first()
            if form.is_valid() and not verify:
                user = form.save()
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/sign_up.html', {'exist':True,'username':Vusername, 'email':Vemail})
    else:
        return render(request, 'registration/sign_up.html')

def login_views(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error':True})
    else:
        return render(request, 'registration/login.html')

def logout_views(request):
    logout(request)
    return redirect('/pharmacy/login')

def show(request):
    if(request.method == "POST"):
        element = request.POST.get('medicament').strip()
        verify = medicament.objects.filter(nom__icontains=element).first()
        if verify:
            return render(request, 'applications/afficher/show.html', {'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
        else:
            return render(request, 'applications/afficher/show.html', {'status':True})
    else:
        return redirect('/pharmacy/home/show')

def add(request):
    if request.method == "POST":
        vnom = request.POST.get('nom').strip()
        vcode = request.POST.get('code').strip()
        vprix = request.POST.get('prix').strip()
        vdescription = request.POST.get('description').strip()
        vdate_expiration = request.POST.get('dateExpiration').strip()
        vstock_disponible = request.POST.get('stockDisponible').strip()

        verify = medicament.objects.filter(nom__icontains = vnom).first()
        if not verify:
            new_medicament = medicament.objects.create(
                nom = vnom,
                code = vcode,
                prix = vprix,
                description = vdescription,
                dateExpiration = vdate_expiration,
                stockDisponible = vstock_disponible
            )
            if new_medicament:
                return render(request, 'applications/ajouter/add.html', {'ajout_success': True})
        elif verify:
            return render(request, 'applications/ajouter/add.html', {'exist': True})
        else:
            return render(request, 'applications/ajouter/add.html', {'fails': False})
    else:
        return render(request, 'applications/ajouter/add.html', {'new': True})
    
def delete(request):
    if request.method == "POST":
        element = request.POST.get('medicament').strip()
        confirmation = request.POST.get('ok')

        verify = medicament.objects.filter(nom__icontains=element).first()
        if confirmation is not None:
            result = medicament.objects.filter(nom__icontains=element).delete()
            if result:
                return render(request, 'applications/supprimer/delete.html', {'done':True})
        if verify and confirmation is None:
            return render(request, 'applications/supprimer/delete.html', {'status':True , 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
        else:
            return render(request, 'applications/supprimer/delete.html', {'not_status':True})
    else:
        return render(request, 'applications/supprimer/delete.html', {'new':True})

def change(request):
    if request.method == "POST":
        element = request.POST.get('medicament').strip()
        confirmation = request.POST.get('first')
        value = request.POST.get('value')

        verify = medicament.objects.filter(nom__icontains=element).first()
        if not verify:
            return render(request, 'applications/modifier/change.html', {'not_status':True})
        if (confirmation == '1' and value != '') or confirmation == '3':
            return render (request, 'applications/modifier/change.html', {'start':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
        if confirmation == '2' and value != '':
            if int(value) <= 0:
                return render(request, 'applications/modifier/change.html', {'value_error':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
            else:
                verify.stockDisponible = int (value)
                verify.save()
                return render(request, 'applications/modifier/change.html', {'done':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
        else:
            return render(request, 'applications/modifier/change.html', {'status':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
    else:
        return render(request, 'applications/modifier/change.html', {'new':True})
    
def sell(request):
    if request.method == "POST":
        element = request.POST.get('medicament').strip()
        confirmation = request.POST.get('first')
        value = request.POST.get('value')

        verify = medicament.objects.filter(nom__icontains=element).first()
        if not verify:
            return render(request, 'applications/vendre/sell.html', {'not_status':True})
        elif (confirmation == '1' and value !='') or confirmation == '3':
            return render (request, 'applications/vendre/sell.html', {'start':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
        elif confirmation == '2' and value !='':
            if int(value) <= 0:
                return render(request, 'applications/vendre/sell.html', {'value_error':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
            else:
                if verify.stockDisponible < int (value):
                    return render(request, 'applications/vendre/sell.html', {'stock_error':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
                else:
                    verify.stockDisponible = (verify.stockDisponible - int (value))
                    verify.save()
                    return render(request, 'applications/vendre/sell.html', {'done':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
        else:
            return render(request, 'applications/vendre/sell.html', {'status':True, 'nom':verify.nom,'code':verify.code,'prix':verify.prix, 'description':verify.description, 'dateExpiration':verify.dateExpiration, 'stockDisponible':verify.stockDisponible})
    else:
        return render(request, 'applications/vendre/sell.html', {'new':True})





