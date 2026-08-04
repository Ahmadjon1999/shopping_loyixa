from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages



from app_one.models import Product,User, Cart, Transaction



def home_page(request):

    return render(request, template_name="home_page.html")



def products(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        data = {
            "products": products
        }
        return render(request, template_name="products.html", context=data)
    return redirect("login")


# DARSDAGI USLUB

# def user_login(request):
#    if request.user.is_authenticated:
#        return redirect("index")
#     if request.method == "POST":
#         phone_number = request.POST.get("phone_number")
#         password     = request.POST.get("password")
#
#         user = User.objects.filter(phone_number=phone_number).first()
#         if user:
#             password_exists = user.check_password(raw_password=password)
#             if password_exists:
#                 login(
#                     request=request,
#                     user=user
#                 )
#                 return redirect("index")
#
#         messages.error(request ,"Tel raqam yoki parol xato")
#         return redirect("login")
#
#     return render(request, template_name="login.html")



# PRO USLUB

def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if user:
            login(
                request=request,
                user=user,
            )
            return redirect("index")
        messages.error(request, "Tel raqam yoki Parol xato")
        return redirect("login")
    return render(request, template_name="login.html")



def user_logout(request):
    logout(request=request)
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")  # Yangi
        address = request.POST.get("address")  # Yangi
        profile_image = request.FILES.get("profile_image")  # Faylni olish uchun request.FILES ishlatiladi
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not first_name or not last_name or not phone_number or not password1 or not password2:
            messages.error(request, "Barcha majburiy soxalar to'ldirilishi shart")  # request qo'shildi
            return redirect("register")

        if password2 == password1:
            if len(password2) >= 8:
                user_exists = User.objects.filter(phone_number=phone_number).exists()

                if user_exists:
                    messages.error(request, "Bunday foydalanuvchi mavjud")
                    return redirect("register")

                # Yangi maydonlar bilan birga foydalanuvchi yaratish
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email if email else None,
                    address=address if address else None,
                    profile_image=profile_image if profile_image else None,
                )
                user.set_password(raw_password=password2)
                user.save()
                messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
                return redirect("login")

            else:
                messages.error(request, "Parol 8 ta belgidan kam")


        else:
            messages.error(request, "Parollar mos emas")
        return redirect("register")

    return render(request, template_name="register.html")




def prod_detail(request, product_id):
  product = get_object_or_404(Product, id=product_id)

  if request.method == "POST":
    try:
      quantity = int(request.POST.get("quantity", 1))
    except ValueError:
      quantity = 1

    if quantity > product.in_stock:
      messages.error(
          request, f"Kechirasiz, omborda faqat {product.in_stock} ta mavjud."
      )
      return render(request, "prod_detail.html", {"product": product})

    try:
      cart_obj = Cart.objects.get(user=request.user, product=product)
    except Cart.DoesNotExist:
      cart_obj = None

    if cart_obj is None:

      Cart.objects.create(
          user=request.user,
          product=product,
          count=quantity,
      )

      product.in_stock -= quantity
      product.save()

      messages.success(request, "Maxsulot savatchaga muvaffaqiyatli qoshildi")
    else:

      cart_obj.count += quantity
      cart_obj.save()


      product.in_stock -= quantity
      product.save()

      messages.success(request, "Savatchadagi maxsulot soni o'zgartirildi")

  data = {"product": product}
  return render(request, template_name="prod_detail.html", context=data)


def profile_info(request):

    if not request.user.is_authenticated:
        return redirect("login")


    context = {
        'user_info': request.user
    }
    return render(request, "profile.html", context)



def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Avval tizimga kirin")
        return redirect("login")
    products = request.user.cart_set.all()


    total_sum = 0
    for i in products:
        total_sum += i.count * i.product.price

    data = {
        "products": products,
        "total_sum": total_sum
    }
    return render(request, template_name="cart.html", context=data)





def delete_product(request, product_id):

  cart_item = Cart.objects.filter(id=product_id, user=request.user).first()

  if cart_item:
    product = cart_item.product
    product.in_stock += cart_item.count
    product.save()


    cart_item.delete()

  return redirect("cart")




def transaction(request):
    return render(request, template_name="transaction.html")




def buy(request):
    cart_objects = request.user.cart_set.all()

    if not cart_objects.exists():
        return redirect("cart")

    for cart_object in cart_objects:
        Transaction.objects.create(
            user=request.user,
            product_name=f"{cart_object.product.name} | Narxi: {cart_object.product.price}$ | Soni: {cart_object.count} ta",
            amount=cart_object.product.price * cart_object.count,
        )
    cart_objects.delete()
    return redirect("transactions")



def delete_transactions(request):
    transaction = request.user.transaction_set.all()
    transaction.delete()
    return redirect("transactions")



















