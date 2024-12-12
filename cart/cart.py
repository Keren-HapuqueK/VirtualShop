from decimal import Decimal
from django.conf import settings
from shop.models import Produto

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # salva um carrinho vazio na sessão do browser
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, produto, quantidade=1, override_quantity=False):
        produto_id = str(produto.id)
        if produto_id not in self.cart:
            self.cart[produto_id] = {
                'quantidade': 0,
                'preco': str(produto.preco),
            }
        if override_quantity:
            self.cart[produto_id]['quantidade'] = quantidade
        else:
            self.cart[produto_id]['quantidade'] += quantidade
        self.save()

    def save(self):
        # marca a sessão como "modificada"
        # para ter certeza que será salvo
        self.session.modified = True

    def __iter__(self):
        """
        Interage sobre os itens do carrinho e obtem os produtos
        da base de dados.
        """
        produto_ids = self.cart.keys()
        # get the product objects and add them to the cart
        produtos = Produto.objects.filter(id__in=produto_ids)
        cart = self.cart.copy()

        for produto in produtos:
            cart[str(produto.id)]['produto'] = produto

        for item in cart.values():
            item['preco'] = Decimal(item['preco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield item  # return a list of values from this function

    def __len__(self):
        return sum(item['quantidade'] for item in self.cart.values())

    def remove(self, produto):
        produto_id = str(produto.id)
        if produto_id in self.cart:
            del self.cart[produto_id]
            self.save()

    def clear(self):
        # remove o carrinho da sessão
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_preco_total(self):
        return sum(
            Decimal(item['preco']) * item['quantidade']
            for item in self.cart.values()
        )