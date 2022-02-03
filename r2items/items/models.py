from django.db import models

DEFAULT_IMG = 'media/img_default.jpg'


def monster_directory_path(instance, filename):
    return 'media/monsters/img_{0}'.format(filename)


class Location(models.Model):
    title = models.CharField(verbose_name="Название", max_length=150)
    local_img = models.ImageField(upload_to="media/locations",
                                  default=DEFAULT_IMG)
    url = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Monster(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    monster_img = models.FileField(upload_to=monster_directory_path,
                                   default=DEFAULT_IMG)
    # models.ImageField(upload_to=upload_function,
    #                                 null=True,
    #                                 blank=True)
    url = models.SlugField(max_length=250, unique=True)
    locatinons = models.ManyToManyField(Location)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Монстр"
        verbose_name_plural = "Монстры"


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    url = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория предмета"
        verbose_name_plural = "Категории предметов"


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

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
