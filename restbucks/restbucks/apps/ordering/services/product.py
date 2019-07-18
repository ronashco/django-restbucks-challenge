from ..models import Product, OptionSet, Option


class ProductService(object):
    @staticmethod
    def fetch_menu_list():
        return Product.objects.filter(soft_deleted=False)

    @staticmethod
    def get(**filters):
        return Product.objects.get(soft_deleted=False, **filters)

    @staticmethod
    def get_option_set(**filters):
        return OptionSet.objects.get(soft_deleted=False, **filters)

    @staticmethod
    def get_option(**filters):
        return Option.objects.get(soft_deleted=False, **filters)
