from django.shortcuts import render
from django.views.generic.base import View
from apps.group_channels.models import Group
from django.db.models import Count
from apps.parser.models import TelegramChannel
from math import ceil

class IndexView(View):
    CATS_COLUMNS = 4 
    ROWS_PER_COL = 8


    def get(self, request, *args, **kwargs):
        editorial = (
            Group.objects
                 .filter(is_editorial=True)
                 .annotate(ch_count=Count('channels'))
        )

        auto_qs = (
            Group.objects
                 .filter(auto_rule__isnull=False)
                 .select_related('auto_rule')
                 .order_by('order', 'name')
        )
        auto_groups = list(auto_qs)

        page_size = self.CATS_COLUMNS * self.ROWS_PER_COL
        total = len(auto_groups)
        total_pages = max(1, ceil(total / page_size))

        try:
            page = int(request.GET.get('cats_page', '1'))
        except ValueError:
            page = 1
        page = max(1, min(page, total_pages))

        start = (page - 1) * page_size
        end = start + page_size
        page_groups = auto_groups[start:end]

        categories = [g.auto_rule.category for g in page_groups]
        if categories:
            counts_qs = (
                TelegramChannel.objects
                    .filter(category__in=categories)
                    .values('category')
                    .annotate(cnt=Count('id'))
            )
            counts_map = {row['category']: row['cnt'] for row in counts_qs}
        else:
            counts_map = {}

        for g in page_groups:
            g.cat_count = counts_map.get(g.auto_rule.category, 0)

        cols = []
        for i in range(self.CATS_COLUMNS):
            start_i = i * self.ROWS_PER_COL
            end_i = start_i + self.ROWS_PER_COL
            cols.append(page_groups[start_i:end_i])
        
        role = request.role
        
        context = {
            'editorial_groups': editorial,
            'categories_cols': cols,
            'cats_page': page,
            'cats_total_pages': total_pages,
            'cats_has_prev': page > 1,
            'cats_has_next': page < total_pages,
            'cats_prev_page': page - 1,
            'cats_next_page': page + 1,
            'user_role': role
        }
        print(role)
        return render(request, 'index.html', context)
