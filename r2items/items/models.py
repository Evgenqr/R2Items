from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

DEFAULT_IMG = 'media/img_default.jpg'


def monster_directory_path(instance, filename):
    return 'media/monsters/img_{0}'.format(filename)


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    url = models.SlugField("Ссылка", max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория предмета"
        verbose_name_plural = "Категории предметов"


class Location(models.Model):
    title = models.CharField(verbose_name="Название", max_length=150)
    local_img = models.ImageField("Изображение",
                                  upload_to="media/locations",
                                  default=DEFAULT_IMG)
    url = models.SlugField("Ссылка", max_length=250, unique=True)

    def __str__(self):
        return self.title
     
    def get_absolute_url(self):
        return reverse("location_list", kwargs={"slug": self.url})
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Monster(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    monster_img = models.FileField("Изображение",
                                   upload_to="media/monsters",
                                   default=DEFAULT_IMG)
    url = models.SlugField("Ссылка", max_length=250, unique=True)
    locations = models.ManyToManyField(Location,
                                       verbose_name="Локация",
                                       related_name="monsters_in_location")

    # slug = models.SlugField("Слаг", max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("monster_list", kwargs={"slug": self.url})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super(Monster, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Монстр"
        verbose_name_plural = "Монстры"

    # def get_absolute_url(self):
    #     return reverse('items:monster_list_by_location',
    # args=[self.id, self.slug])


class Item(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Автор",
                               blank=True,
                               null=True)
    name = models.CharField(verbose_name="Предмет: ", max_length=150)
    description = models.TextField(verbose_name="Описание",
                                   null=True,
                                   blank=True)
    weight = models.IntegerField("Вес:", default=0)
    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 on_delete=models.CASCADE)
    monster = models.ManyToManyField(Monster,
                                     verbose_name="Выпадает с: ",
                                     related_name="monster_item")
    url = models.SlugField("Ссылка", max_length=250, unique=True)
    item_img = models.ImageField("Изображение",
                                 upload_to='media/items/',
                                 default=DEFAULT_IMG)

    # slug = models.SlugField("Слаг", max_length=130, unique=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super(Item, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("item_list", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self',
                               verbose_name="Родитель",
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)
    monster = models.ForeignKey(Monster,
                                verbose_name="Монстр",
                                on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.monster}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


# class Comments(models.Model):
#     monster = models.ForeignKey(Monster,
#                                 on_delete=models.CASCADE,
#                                 verbose_name="Монстр",
#                                 blank=True,
#                                 null=True,
#                                 related_name="comments_monsters")
#     author = models.ForeignKey(User,
#                                on_delete=models.CASCADE,
#                                verbose_name="Автор",
#                                blank=True,
#                                null=True)
#     create_date = models.DateTimeField(auto_now=True)
#     text = models.TextField(verbose_name="текст комментария", max_length=3000)

#     def __str__(self):
#         return f"{self.author} - {self.monster} - {self.text}"

#     class Meta:
#         verbose_name = "Комментарий"
#         verbose_name_plural = "Комментарии"
