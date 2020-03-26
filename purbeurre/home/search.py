from home.models import Product, Category

def search_product(text):
    queryset = Product.objects.filter(
        name__icontains=text, 
        ).order_by('name')
    
    return queryset

def search_substitute(id):
    product = Product.objects.get(pk=id)
    category = product.category_id
    queryset = Product.objects.filter(
        category_id_id=category.id 
        ).order_by('name').order_by('nutriscore')
    
    return queryset 