from distutils.command.upload import upload
from tabnanny import verbose
from unicodedata import category
from django.db import models
from .utils import upload_function


class Location(models.Model):
    title = models.CharField(verbose_name="Название", max_length=150)
    local_img = models.ImageField(upload_to=upload_function, null=True, blank=True)
    url = models.SlugField(max_length=250, unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Monster(models.Model):
    name = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    monster_img = models.ImageField(upload_to=upload_function, null=True, blank=True)
    url = models.SlugField(max_length=250, unique=True)
    locatinons = models.ManyToManyField(Location, verbose_name="Локация", related_name="monster_location")
    
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
    category = models.ForeignKey(Category,verbose_name="Категория" )
    monster = models.ManyToManyField(Monster, verbose_name="Локация", related_name="monster_item")
    url = models.SlugField(max_length=250, unique=True)
    item_img = models.ImageField(upload_to=upload_function, null=True, blank=True)
    
        
    def __str__(self):
        return self.name
    
    class Meta:
         verbose_name = "Предмет"
         verbose_name_plural = "Предметы"
