from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from equipment.models import Equipment, MovementHistory
from post_office.forms import AddEquipmentForm
from post_office.models import PostOffice


class HomePageView(LoginRequiredMixin, TemplateView):
    """Домашняя страница"""
    template_name = '_base.html'
    login_url = 'account_login'


class AddEquipment(LoginRequiredMixin, FormView):
    """Страница добавления оборудования"""
    template_name = 'post_office/add_equipment.html'
    form_class = AddEquipmentForm
    login_url = 'account_login'
    success_url = reverse_lazy('add_equipment')

    def does_equipment_exist(self, barcode):
        """Проверяем существует ли обькт в БД по штрихкоду"""
        try:
            equipment = Equipment.objects.get(bar_number=int(barcode))
            return equipment
        except Equipment.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, 'Оборудование с таким идентификатором не найдено')

    def move_equipment(self, equipment, new_department):
        """Перемещаем технику"""
        try:
            equipment.department = new_department
            equipment.save()  # Не забываем сохранить изменения
            messages.add_message(self.request, messages.SUCCESS, 'Оборудование успешно перемещено')
        except Exception as e:
            raise Exception(f"Оборудование не было перемещено из-за ошибки: {e}")

    def create_movement_history(self, equipment, old_department, new_department):
        """Создаем запись в истории перемещений"""
        try:
            MovementHistory.objects.create(
                equipment=equipment,
                from_where=old_department,
                where=new_department,
                who_moved=self.request.user
            )
        except Exception as e:
            raise Exception(f"При создании истории перемещения произошла ошибка: {e}")

    def form_valid(self, form):
        barcode = form.cleaned_data['barcode']
        equipment = self.does_equipment_exist(barcode)
        if equipment:
            old_department = equipment.department
            new_department = self.request.user.department
            if old_department != new_department:
                self.create_movement_history(equipment, old_department, new_department)
                self.move_equipment(equipment, new_department)
            else:
                messages.add_message(self.request, messages.WARNING, 'Оборудование уже находится на балансе отдела')

        return super().form_valid(form)


class PostOfficeDetailView(LoginRequiredMixin, DetailView):
    model = PostOffice
    context_object_name = 'post_office'
    template_name = 'post_office/post_office_detail.html'
    login_url = 'account_login'

    def __get_count_equipments(self):
        """Получаем количество оборудования"""
        post_office = self.get_object()  # получаем обькт класса
        count_equipments = len(post_office.equipments.all())
        return count_equipments

    def __get_sum_equipments(self):
        """Получаем стоимость всего оборудования"""
        post_office = self.get_object()  # получаем обькт класса
        sum_equipments = sum([m.price for m in post_office.equipments.all()])
        return sum_equipments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_equipments'] = self.__get_count_equipments()
        context['sum_equipments'] = self.__get_sum_equipments()
        return context
