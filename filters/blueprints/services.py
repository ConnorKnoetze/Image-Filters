import os

from filters.domainmodel.nav_item import NavItem

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
def get_nav_items(current_filter=None):
    filters = os.listdir(PROJECT_ROOT + "\\filter_types")[:-2:]
    nav_items = [NavItem("Home", "/")]
    nav_items += [NavItem(filter[0].upper() + filter[1:], f"filters/{filter}" if not current_filter else filter) for filter in filters]
    return nav_items