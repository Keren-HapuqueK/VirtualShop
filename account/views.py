from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse

# Create your views here.
def signUp(request):
    User = get_user_model()
    
    if request.user.is_authenticated:
        return render(request=request, template_name='account/home.html')
    
    if request.method == 'POST':
        #intercepta os dados do formulario/ as variaveis transacionadas no POST
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        genero = request.POST.get('genero','')
        nasimento = request.POST.get('nasimento','')
        redesocial = request.POST.get('redesocial','')
        
        #criando o objeto do usuario com as variaveis de instancia
        user = User.objects.create_user(username=username, 
                                        email=email, 
                                        password=password, 
                                        genero=genero, 
                                        nasimento=nasimento, 
                                        redesocial=redesocial)
        
        #redirecinando o usuario para a pagina home
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
        return redirect('/')
        
    return render(request=request, template_name='account/signup.html', context={})

def signIn(request):
    if request.method == 'POST':
        #intercepta os dados do formulario/ as variaveis transacionadas no POST
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session.save()
            return redirect('/')
        else:
            return HttpResponse('Autenticação falhou!')
          
    return render(request=request, template_name='account/signin.html', context={})

def home(request):
    return render(request=request, template_name='account/home.html', context={})

def signOut(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')