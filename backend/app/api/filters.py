from fastapi_filters import FilterField, FilterSet


class ProductFilters(FilterSet):
    name: FilterField[str]