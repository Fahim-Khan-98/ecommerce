from django.shortcuts import render
from django.views.generic import ListView,DetailView

from store.models import Product,ProductImages
# Create your views here.





class HomeListView(ListView):
    model = Product
    template_name = "store/index.html"
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ProductImages.objects.filter(product=self.object.id)
        return context


# def product_details(request, pk):
#     item = Product.objects.get(id=pk)
#     context = {
#         'item' : item,
#     }

#     return render (request, 'store/product.html', context)