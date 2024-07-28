from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from equipment.models import Equipment
from equipment.qr import PDFGenerator


class EquipmentListView(LoginRequiredMixin, ListView):
    """Список всего обрудования"""
    model = Equipment
    context_object_name = 'equipments_list'
    template_name = 'equipment/equipment_list.html'
    login_url = 'account_login'


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    """Детальное расмотрение оборудования"""
    model = Equipment
    context_object_name = 'equipment'
    template_name = 'equipment/equipment_detail.html'
    login_url = 'account_login'

    @staticmethod
    def __get_inform_for_qrcode(pk):
        """Получаем обьект модель класса Equipment и возвращаем данные об обьекте"""
        equipment = Equipment.objects.get(pk=pk)
        inform_for_qrcode = {
            'id': equipment.id,
            'inventory_number': equipment.inventory_number,
            'serial_number': equipment.serial_number,
            'department': equipment.department,
            'bar_number': equipment.bar_number,
        }
        return inform_for_qrcode

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('button_pressed', False)
        if pk:
            data = self.__get_inform_for_qrcode(pk)
            text = f"Отдел: {data['department']} ИНН: {data['inventory_number']} Серийный: {data['serial_number']}"
            pdf = PDFGenerator(data['bar_number'], data['bar_number'], text)
            response = HttpResponse(pdf.generate_pdf_bytes(), content_type='application/pdf')
            pdf.close_buffers()  # Освобождаем ресурсы оперетивной паммяти
            return response

        return super().get(request, *args, **kwargs)


class EquipmentResultsView(LoginRequiredMixin, ListView):
    """Результат поиска"""
    model = Equipment
    context_object_name = "equipment_list"
    template_name = 'equipment/search_results.html'
    login_url = 'account_login'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Equipment.objects.filter(
            Q(inventory_number__icontains=query) | Q(serial_number__icontains=query)
        )
