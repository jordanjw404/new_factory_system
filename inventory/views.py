from decimal import Decimal
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404, render, redirect

from .models import Product, Balance, StockTransaction, TxnType
from .forms import ProductActionForm

def product_list(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.all().annotate(on_hand=Sum("balances__qty_on_hand")).order_by("sku")
    if q:
        qs = qs.filter(Q(sku__icontains=q) | Q(name__icontains=q))
    products = Paginator(qs, 25).get_page(request.GET.get("page"))
    return render(request, "inventory/stock_list.html", {"products": products, "q": q})

def _get_balance_for_update(product, location_code):
    bal = Balance.objects.select_for_update().filter(product=product, location_code=location_code).first()
    if not bal:
        bal = Balance(product=product, location_code=location_code, qty_on_hand=Decimal("0.000"))
    return bal

def product_action_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductActionForm(request.POST or None)

    # Allow ?op=IN/OUT/MOVE to preselect operation
    if not form.is_bound:
        form.initial.update({"operation": request.GET.get("op") or "IN"})

    if request.method == "POST":
        if form.is_valid():
            op  = form.cleaned_data["operation"]
            qty = form.cleaned_data["qty"]
            note = form.cleaned_data.get("note")
            fl = form.cleaned_data.get("from_location")
            tl = form.cleaned_data.get("to_location")

            with transaction.atomic():
                if op == "IN":
                    to = _get_balance_for_update(product, tl)
                    to.qty_on_hand += qty
                    to.save()
                    StockTransaction.objects.create(
                        product=product, txn_type=TxnType.IN, qty=qty,
                        from_location=tl, to_location=tl, note=note
                    )
                    messages.success(request, f"IN {qty} to {product.sku} @ {tl}")

                elif op == "OUT":
                    fr = _get_balance_for_update(product, fl)
                    if fr.qty_on_hand < qty:
                        messages.error(request, f"Insufficient stock in {fl}. On hand: {fr.qty_on_hand}")
                        per_loc = Balance.objects.filter(product=product).order_by("location_code")
                        return render(request, "inventory/product_action.html", {"product": product, "form": form, "per_loc": per_loc})
                    fr.qty_on_hand -= qty
                    fr.save()
                    StockTransaction.objects.create(
                        product=product, txn_type=TxnType.OUT, qty=qty,
                        from_location=fl, to_location=fl, note=note
                    )
                    messages.success(request, f"OUT {qty} from {product.sku} @ {fl}")

                else:  # MOVE
                    fr = _get_balance_for_update(product, fl)
                    if fr.qty_on_hand < qty:
                        messages.error(request, f"Insufficient stock to move. On hand at {fl}: {fr.qty_on_hand}")
                        per_loc = Balance.objects.filter(product=product).order_by("location_code")
                        return render(request, "inventory/product_action.html", {"product": product, "form": form, "per_loc": per_loc})
                    to = _get_balance_for_update(product, tl)
                    fr.qty_on_hand -= qty
                    to.qty_on_hand += qty
                    fr.save(); to.save()
                    StockTransaction.objects.create(
                        product=product, txn_type=TxnType.MOVE, qty=qty,
                        from_location=fl, to_location=tl, note=note
                    )
                    messages.success(request, f"MOVE {qty} {product.sku} from {fl} → {tl}")

            return redirect("inventory:product_action", product_id=product.id)
        else:
            messages.error(request, form.errors.as_text())

    per_loc = Balance.objects.filter(product=product).order_by("location_code")
    return render(request, "inventory/product_action.html", {"product": product, "form": form, "per_loc": per_loc})

def stock_txn_list(request):
    txns = Paginator(StockTransaction.objects.select_related("product").order_by("-created_at"), 50)\
        .get_page(request.GET.get("page"))
    return render(request, "inventory/stock_txn_list.html", {"txns": txns})
