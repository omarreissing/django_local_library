from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    """
    Modelo que representa un género literario, por ejemplo ciencia ficción, poesía, etc
    """
    name=models.CharField(max_length=200, help_text="Ingrese el nombre del género (por ej. Ciencia Ficción, Poesía, etc")

    def __str__(self):
        return self.name 


class Languaje(models.Model):
    # Modelo representa un lenguaje

    name=models.CharField(max_length=200,help_text='Ingrese un lenguaje')

    def __str__(self):
        return self.name 
    


class Book(models.Model):
    """
    Modelo que representa un libro
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',on_delete=models.SET_NULL, null=True )
    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre,help_text="Seleccione un género para este libro")

    languaje= models.ForeignKey('Languaje',on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        # string que representa el objeto book

        return self.title

    def get_absolute_url(self):
        # devuelve el url a una instancia particular de book

        return reverse('book-detail',args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    
    display_genre.short_description = 'Genre'

    
import uuid 

class BookInstance (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro")
    book = models.ForeignKey('Book',on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back =models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True, default='m',help_text='Disponibilidad del libro')


    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)   

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    """
    Modelo que representa un autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s, %s' % (self.id, self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']

