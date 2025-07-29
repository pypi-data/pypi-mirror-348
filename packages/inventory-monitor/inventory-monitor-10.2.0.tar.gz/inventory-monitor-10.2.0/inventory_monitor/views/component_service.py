from netbox.views import generic

from inventory_monitor import filtersets, forms, models, tables


class ComponentServiceView(generic.ObjectView):
    queryset = models.ComponentService.objects.all()


class ComponentServiceListView(generic.ObjectListView):
    queryset = models.ComponentService.objects.all()
    filterset = filtersets.ComponentServiceFilterSet
    filterset_form = forms.ComponentServiceFilterForm
    table = tables.ComponentServiceTable


class ComponentServiceEditView(generic.ObjectEditView):
    queryset = models.ComponentService.objects.all()
    form = forms.ComponentServiceForm


class ComponentServiceDeleteView(generic.ObjectDeleteView):
    queryset = models.ComponentService.objects.all()
