from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаление всех новостей в указанной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Название категории')

    def handle(self, *args, **options):
        category_name = options['category']
        answer = input(f'Вы правда хотите удалить все статьи в категории "{category_name}"? да/нет')

        if answer.lower() != 'да':
            self.stdout.write(self.style.ERROR('Операция отменена'))
            return

        try:
            category = Category.objects.get(name=category_name)
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Статьи в категории "{category.name}" успешно удалены!'))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория "{category_name}" не найдена'))
