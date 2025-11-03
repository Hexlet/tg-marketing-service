from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.base import View

from apps.parser.models import TelegramChannel

from apps.group_channels.forms import AddChannelForm, CreateGroupForm, UpdateGroupForm
from apps.group_channels.models import Group


class CreateGroupView(View):
    def post(self, request, *args, **kwargs):
        up_form = UpdateGroupForm()
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            if not group.image_url:
                group.image_url = 'data:image/jpeg;base64,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'
            group.owner = request.user
            form.save()
            messages.success(request, 'Группа успешно создана')
            return redirect(reverse('users:profile'))
        return render(request, 'users/profile.html', {
            'create_form': form,
            'update_form': up_form
        })


class UpdateGroupView(View):
    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        group = get_object_or_404(Group, slug=slug)
        form = UpdateGroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()
            messages.success(request, 'Группа успешно изменена')
        else:
            if form.errors.get('name'):
                messages.error(request, form.errors['name'].as_text()[1:])
            if form.errors.get('description'):
                messages.error(request, 'Слишком длинное описание (макс. 200 симв.).')

        return redirect(reverse('users:profile'))


class DeleteGroupView(View):
    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        group = get_object_or_404(Group, slug=slug)
        group.delete()
        messages.success(request, 'Группа успешно удалена')
        return redirect(reverse('users:profile'))


class GroupDetailView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        group = get_object_or_404(Group, slug=slug)

        channels = group.channels.all()

        auto_category = None
        if hasattr(group, 'auto_rule'):
            auto_category = group.auto_rule.category
            channels = TelegramChannel.objects.filter(category=auto_category)

        is_owner = request.user.is_authenticated and (group.owner == request.user)
        add_form = None
        if is_owner and not hasattr(group, 'auto_rule'):
            free_qs = TelegramChannel.objects.exclude(groups=group)
            add_form = AddChannelForm(channel_qs=free_qs)

        return render(request, 'group_channels/detail.html', {
            'group': group,
            'channels': channels,
            'auto_category': auto_category,
            'add_form': add_form,
            'is_owner': is_owner,
        })


class AddChannelsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return self.group.owner == self.request.user

    def post(self, request, slug):
        free_qs = TelegramChannel.objects.exclude(groups=self.group)
        form = AddChannelForm(request.POST, instance=self.group, channel_qs=free_qs)

        if form.is_valid():
            self.group.channels.add(*form.cleaned_data['channels'])
            messages.success(request, 'Каналы добавлены')
        else:
            for msg in form.errors.values():
                messages.error(request, msg)

        return redirect('group_channels:group_detail', slug=slug)
