from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import stores, products
from .forms import newstoreform, newproductform, newcontactform
from email.message import EmailMessage
import smtplib
from django.views.generic import ListView


def home(request):
    return render(request, 'home.html')


# función info
def info(request):
    nombre = ['DevLupita']
    return render(request, 'info.html', {
        'name': nombre
    })


def stores_view(request):
    s = stores.objects.all()
    return render(request, 'stores.html', {
        'stores': s
    })


def products_view(request):
    p = products.objects.all()
    return render(request, 'products.html', {
        'products': p
    })


def create_store(request):
    if request.method == 'GET':
        return render(request, 'create_store.html', {
            'forms': newstoreform()
        })
    else:
        stores.objects.create(
            name=request.POST['name'],
            description=request.POST['description']
        )
        return redirect('stores')


def create_product(request):
    if request.method == 'GET':
        return render(request, 'create_product.html', {
            'forms': newproductform(),
            'stores': stores.objects.all()
        })
    else:
        store_id = request.POST['store']
        store_obj = stores.objects.get(id=store_id)

        products.objects.create(
            title=request.POST['title'],
            price=request.POST['price'],
            store=store_obj
        )
        return redirect('products')


def details(request, id):
    s = stores.objects.get(id=id)
    p = products.objects.filter(store_id=id)
    return render(request, 'details.html', {
        'store': s,
        'products': p
    })


def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': newcontactform()})
    else:
        try:
            remitente = "programadores303@gmail.com"
            destinatario = request.POST['email']
            password_app = "vmtujjfepajxyrem"

            mensaje = "Saludos, gracias por contactarnos.\nNuestros productos son:\n\n"

            for i in products.objects.all():
                mensaje += f"{i} - ${i.price}\n"

            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = "Contacto tienda - Nuestros Productos DevLiz"
            email.set_content(mensaje)

            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login(remitente, password_app)
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()

            return redirect('home')

        except Exception as e:
            return render(request, 'contact.html', {
                'form': newcontactform(),
                'error': f'Error: {str(e)}'
            })


def despedirse(request):
    return HttpResponse('<h1>¡Adiós!</h1>')


# BUSCADOR DE PRODUCTOS
class ProductosListView(ListView):
    context_object_name = 'productos'
    template_name = "filtro.html"

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", "")
        return products.objects.filter(title__icontains=palabra_clave)


#  BUSCADOR DE STORES 
class StoresListView(ListView):
    context_object_name = 'stores'
    template_name = "filtro.html"

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", "")
        return stores.objects.filter(name__icontains=palabra_clave)


#  ACTUALIZAR PRODUCTO
def update_product(request):
    if request.method == "GET":

        if "kword" not in request.GET:
            return render(request, "update_product.html")

        nombre = request.GET.get("kword", "")

        try:
            product = products.objects.get(title=nombre)
        except products.DoesNotExist:
            return render(request, "update_product.html", {
                "error": "No existe un producto con ese nombre."
            })

        form = newproductform(initial={
            "title": product.title,
            "price": product.price,
            "store": product.store.id
        })

        return render(request, "update_product.html", {
            "forms": form,
            "product": product
        })

    else:
        nombre_original = request.POST.get("title_original")
        product = products.objects.get(title=nombre_original)

        form = newproductform(request.POST)
        if form.is_valid():
            product.title = form.cleaned_data["title"]
            product.price = form.cleaned_data["price"]
            product.store = form.cleaned_data["store"]
            product.save()
            return redirect("products")

        return render(request, "update_product.html", {
            "forms": form,
            "error": "Datos inválidos"
        })


#  ELIMINAR PRODUCTO 
def delete_product(request):
    context = {}

    if request.method == 'POST':
        kword = request.POST.get('kword', '').strip()

        if kword:
            try:
                obj = products.objects.get(title__iexact=kword)
                obj.delete()
                context['mensaje'] = f"Producto '{kword}' eliminado correctamente."
            except products.DoesNotExist:
                context['error'] = f"No se encontró el producto '{kword}'."

    return render(request, 'delete_product.html', context)


#  ACTUALIZAR STORE 
def update_Stores(request):
    if request.method == "GET":

        if "kword" not in request.GET:
            return render(request, "update_stores.html")

        nombre = request.GET.get("kword", "")

        try:
            store = stores.objects.get(name=nombre)
        except stores.DoesNotExist:
            return render(request, "update_stores.html", {
                "error": "No existe un store con ese nombre."
            })

        form = newstoreform(initial={
            "name": store.name,
            "description": store.description
        })

        return render(request, "update_stores.html", {
            "forms": form,
            "store": store
        })

    else:
        nombre_original = request.POST.get("name_original")

        try:
            store = stores.objects.get(name=nombre_original)
        except stores.DoesNotExist:
            return render(request, "update_stores.html", {
                "error": "La tienda ya no existe."
            })

        form = newstoreform(request.POST)
        if form.is_valid():
            store.name = form.cleaned_data["name"]
            store.description = form.cleaned_data["description"]
            store.save()
            return redirect("stores")

        return render(request, "update_stores.html", {
            "forms": form,
            "error": "Datos inválidos"
        })


#  ELIMINAR STORE 
def delete_Stores(request):
    context = {}

    if request.method == 'POST':
        kword = request.POST.get('kword', '').strip()

        if kword:
            try:
                obj = stores.objects.get(name__iexact=kword)
                obj.delete()
                context['mensaje'] = f"Store '{kword}' eliminado correctamente."
            except stores.DoesNotExist:
                context['error'] = f"No se encontró el Store '{kword}'."

    return render(request, 'delete_stores.html', context)
