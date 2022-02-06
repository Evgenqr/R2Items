from django.db import models
from django.utils.text import slugify

from django.urls import reverse

DEFAULT_IMG = 'media/img_default.jpg'


def monster_directory_path(instance, filename):
    return 'media/monsters/img_{0}'.format(filename)


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    url = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория предмета"
        verbose_name_plural = "Категории предметов"


class Location(models.Model):
    title = models.CharField(verbose_name="Название", max_length=150)
    local_img = models.ImageField(upload_to="media/locations",
                                  default=DEFAULT_IMG)
    url = models.SlugField(max_length=250, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def get_absolute_url(self):
        return reverse('monsters', args=[self.slug])


class Monster(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    monster_img = models.FileField(upload_to=monster_directory_path,
                                   default=DEFAULT_IMG)
    # models.ImageField(upload_to=upload_function,
    #                                 null=True,
    #                                 blank=True)
    url = models.SlugField(max_length=250, unique=True)
    locations = models.ManyToManyField(Location)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Monster, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Монстр"
        verbose_name_plural = "Монстры"

    # def get_absolute_url(self):
    #     return reverse('items:monster_list_by_location',
    # args=[self.id, self.slug])


class Item(models.Model):
    name = models.CharField(verbose_name="Предмет", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 on_delete=models.CASCADE)
    monster = models.ManyToManyField(Monster,
                                     verbose_name="Монстр",
                                     related_name="monster_item")
    url = models.SlugField(max_length=250, unique=True)
    item_img = models.ImageField(upload_to='media/items/', default=DEFAULT_IMG)
    slug = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
