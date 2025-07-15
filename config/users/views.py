from django.contrib import messages, auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from .models import User
from .forms import (
    UserLoginForm,
    UserRegForm,
    UserUpdateForm,
    AvatarChange,
)

from config.group_channels.forms import CreateGroupForm, UpdateGroupForm


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        return redirect(reverse('main_index'))

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Вы разлогинены')
        auth.logout(request)
        return redirect(reverse('main_index'))
    
    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(
            request,
            'login.html',
            {'form': form}
        )
        
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Вы залогинены')
                return redirect(reverse('main_index'))
        return render(request, 'login.html', {'form': form})
   

class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        create_form = CreateGroupForm()
        update_form = UpdateGroupForm()
        avatar_form = AvatarChange()
        user = request.user
        groups = user.user_group.all()
        return render(
            request,
            'users/profile.html',
            {'user': user,
             'create_form': create_form,
             'update_form': update_form,
             'avatar_form': avatar_form,
             'groups': groups}
        )
        

class UserRegister(View):
    def post(self, request, *args, **kwargs):
        form = UserRegForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.avatar_image:
                user.avatar_image = 'data:image/png;base64,iVBORw0KGg\
                    oAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAMFBMVEX\
                    Q3uP////1+PnX4+ft8vT7/P3U4eXM2+Hk7O/d5+vu8/XW4ub\
                        c5ur4+vvl7e/p7/KylbazAAAIGUlEQVR4nO2d2bqrIAyF2U\
                        6IQ33/tz11arVFBbISldN1tS92W/4PSBiSoP5ilzq7Ae\
                            z6Ed5fUoR50pVNWqinirQxjyoR+mERwjwzhdJqJa1VXVa5wK+\
                            zE7aPWn/QLTDTjh2SlzDvii26F2WasTaBlTBpjvBGRl\
                                W2jK3gI6xqJ74RsuEzPFyEiQffyMjVjzyEufHjGxhLl\
                                    qbwEHbeeKNYbA4DYes5QBfdmDL4DjxhFso3M\
                                        Hbw9sAJA2bgCrFBNwhMmBckvl4FeKRi\
                                            CVsyXy+sb4QSJrQROktDbSqSEAQ\
                                                ItjdAQhggthdxhJg5OCNWsH\
                                                    bBCHMk4BMRZm5ghFjAp\
                                                        1BOA0XYwAkLUMtA\
                                                            hA+clXnJY\
                                                                JqGIQS\
a0bdAUxFDyMDXC9M2xJeUTISQcYogZBmjvSBeEUFYMwEqyDgFfAdpy3sgwNkNgJCPTyH8P\
    p2Qy8yMohsbOiHjGH1Kk49RyYS8XQjoRDIhMyC9E6mEHe8gVXRzSiWkn60dSZ9LyLa\
        cWRASTzSIhIYdUKn0VEIBQKVpXp9GWPEP0qdoZ4s0QolBSh2mNEIRQKI1JREKW\
            NKBkHScQSJ8iAASnT6JMBUiJN0pkgiFAGlbfcqHW5lpSPSIFEIZb6iIpoZ\
                CGBpU4i/K0pRCKOPvez1OIpQypbSNPoWQf284i+IuKIRigKqOnpByl\
                    3gPQlIrwz8Kvrn/Ef4If4RBn/0R/ggvTyi3ajtrTSO38j5rXSq\
                        3ezprb8F9OfoW5bCNQpiJEZ61xxc6ED7xnCaP/qwt/vNSM\
                            XdBunwiEUoZ0/PuLYSOhGk3+SRCIVNDC6m5ww0psY2\
                                kT8us22gJezRCztDSt2gBNTRCkYlIjGwjxtNIe\
                                    ERiagmRUOImnxi6RyQUuAamJpZcPzaR2kJ\
                                        yfCk74NnxpezDlJz9RI6C5ram5CQ9M\
iG30ycnPdOzEXgBicGlEML4M0pYV26ALEtA3hPnBoMY4w0iZHQYiARERIYfPo97FuVGZtY\
    vh9RJXJ2I6EIMIdNMxKSrYzLCecwpwJD+oQhZwjLoyZWDQFUjOJL0QBXqUJU/GHbCo\
        JahvgfuMWA1eGD1adALcIyZ+UNWUQKPU1jVNhwhdJxesU4UtgoPqPpOL2S9Nty\
            RDaqCUi9ozT0YIbJ04iWrCuIm4R+6MiTk4E1TMmS+Ba7uWdIRNdDK9EJXa\
                KUjwlz9pKvVoIUDMtQRpm34Idv6lRhqQVMQ8YAs9bzDByoDIE/F8kB\
                    zg68D3Yun6nzQlh/tJiYxvRyQBAAyvXPB9TZC7l16/l5vI/Tym\
                        oxMI7QXhrAylt1A4rHrt6y1W4NZgCPunsr+ISDbhsexG60\
                            d2A7PswBOven3+POEszWmTY8ZdWr75GSqdEF+TIhGm\
                                Jj3O072XV118FiQLqwfW9hi6mNCBMJxdC6aYp8\
                                    31U4/6nTjM+sv1oYwWoMJLQ3fKoffloXlU\
                                        Su9/QrS90b6OVpDGxpG+Nl9czs2rxr\
                                            yqjR10WP1UkVtymrTAdoNlDZhH\
                                                jOEcHvcQR6K2fn2EP/hT9h\
Zu+8lqn3fXe/pgBApT8L28C6U+GzT0Zpdq4fnMPEidHpITRfhK8zcwX8q5TchPQidH1IL7\
    kbXTZfXM23OhMfv/C0VYhISj1/wYHQkPDAv3y2ofS2OywJv9QvWxV4ooS+fVwtGPre\
        nEkN+wYEwC+DzY3R8CjLsFw4Jq0C+oQUuay2HlzxJjAeEvg81fjfBZHv+K888p\
            9/3Dxw9DblLmFB/fmiCLsossWDmSbn9zKzPD9gOGNwIqVcQi0b0z/82pnx\
                0gx6laWqFoJu+fs8BbxPK1QxEaHvCbxGSJ6CwdLFlcjYIATed0tKNf\
                    TpaCX3OAa8k64GOjfCGHTjKugH/Jmxv2oGjvmfjF6FYYVkefTu\
                        OT8LbjtBZX5eQH4SBS+BLKd0jlKttxal6m5Av+UVWzRYhb\
                            h16slZxYwvCm1vRpZa5KAvCs5uFVGEj5H/XSFCLsAc\
                                VZReqRbbG66+IZmGv92XmizAWTzEr/SQUqy4np\
                                    Vde2Ex4rzMLF5UfhIxviZ6lNWF0g/Tt9VW\
                                        sg/Q1TCfCODYVaxVLwggH6cuaqhjd/\
                                            aRuQShX81hS6YLw7LbwaKxtMxC\
                                                KFQSW1bg2HQilXoiTlnkRR\
                                                    rigGTUTRukreg3+QkX\
rK3p1E6Fc9XhpNRPhra9i9jUSSr4XI6zeI6povWGv3iMqqWLA56gbCOM1NMMeUcW67B5lB\
    sLYzhGXav6TPox/HsbvLSLd/w6Kfl1qJkKx16el9do9RWtN33v8WNfesZ+XThcX06l\
        +hONUr+8t4ru4eCWIv265I0N8Z8C/YxaiOlJcpPgvIoZiiEuctIwyXca13T62d\
            NYqb34Vm1id3TSMilW09zq+1C1L9dr6jIP+jIK++4X+d2bJVyR7fusoU0t\
                ZB0u+xd0Sgt6yZrFZc2YyQs7jedrIRNzIe7of42am5WZ2nnP2/SW0U\
                    xZkJ8MyNP9YXFqVO1mku1my+YOQ5iyloxpER7ncVYNLZmXQdhU\
                        fZ8KnsqtCauVS8MyppkKeNZcbrlo1bsU3nCt/VOZCkG695\
0n4VFLWF6Ds8/t9Sm541hjKK2vdLjk8tV+jgU44qHqkJ/Tls+9MFlC+KLReW9IZSMkHRzi\
    VllVgGTFSVcEkK1Ng8Qc7XNEEw9EJB+VJN3CCQfsvbOwlQ6QJR+XP/jRpQScdi4SU3\
        XZJPk+ha9DmSdWVpinGtrrSTv+amjKDkc3iq7Kbt0mV9YVaTJOmdfEdPFcUdZo\
            2xpRdViVJi3zTYik+wqvoR3h/xU/4DwzAeQMogZYGAAAAAElFTkSuQmCC'

            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Пользователь успешно зарегистрирован')
            return redirect(reverse('users:login'))
        return render(request, 'users/register.html', {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = UserRegForm()
        return render(
            request,
            'users/register.html',
            {'form': form}
        )
        

class UserUpdate(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if request.user.username == kwargs.get('username'):
            form = UserUpdateForm(initial={
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'avatar_image': request.user.avatar_image,
                'email': request.user.email,
                'bio': request.user.bio,
            })
            return render(
                request,
                'users/update.html',
                {'form': form,
                 'username': request.user.username,
                 'user': request.user,
                }
            )
        messages.add_message(request,
                             messages.ERROR,
                        'У вас нет прав для изменения другого пользователя.')
        return redirect(reverse('users:profile'))
    
    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        form = UserUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Профиль успешно изменен')
            return redirect(reverse('users:profile'))
        return render(
            request,
            'users/update.html',
            {'form': form}
        )


class AvatarChangeView(View):
    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        avatar_form = AvatarChange(data=request.POST, instance=user)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Аватар успешно изменен')
            return redirect(reverse('users:profile'))
        if avatar_form.errors.get('avatar_url'):
            avatar_url = avatar_form.errors.get('avatar_url').as_text()
            messages.add_message(request,
                                 messages.ERROR,
                                 avatar_url[1:])
        return redirect(reverse('users:profile'))