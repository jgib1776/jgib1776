from django.contrib.auth.models import User
from django.db import models
# Pillow for working with images
from PIL import Image

AUTHOR_TYPES = (
    ('Au', 'Author'),
    ('Co', 'Co-Author'),
)
REFERENCE_TYPES = (
    ('Ac', 'Act'),
    ('Ar', 'Article'),
    ('Au', 'Audio Recording'),
    ('Bk', 'Book'),
    ('Bs', 'Book Section'),
    ('Cp', 'Book Chapter'),
    ('Jn', 'Journal'),
    ('Mg', 'Magazine'),
    ('Mv', 'Movie'),
    ('Np', 'News Paper'),
    ('Op', 'Opera'),
    ('Pc', 'Podcast'),
    ('Pi', 'Picture'),
    ('Pl', 'Play'),
    ('Po', 'Poem'),
    ('Sy', 'Symphony'),
    ('Vs', 'Verse'),
    ('Ws', 'Website'),
)

class Address(models.Model):
    country = models.ForeignKey('Country', on_delete=models.SET_NULL,
        blank=True, null=True)


class Author(models.Model):
    author_type = models.CharField(max_length=2, choices=AUTHOR_TYPES)
    display_name = models.CharField(max_length=128)

    class Meta:
        abstract = True
        #db_table = 'author'
        ordering = ['author_type','display_name']

class AuthorPerson(Author):
    first_name = models.CharField(max_length=128, blank=False, null=True)
    last_name = models.CharField(max_length=128, blank=False, null=True)
    middle_name = models.CharField(max_length=128, blank=False, null=True)
    birth_date = models.DateField()
    death_date = models.DateField()

    class Meta:
        db_table = 'author_person'

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}"

class AuthorOrganization(Author):
    org_name = models.CharField(max_length=128, blank=False, null=True)
    date_began = models.DateField()
    date_ended = models.DateField()

    class Meta:
        db_table = 'author_organization'

    def __str__(self):
        return f"{self.org_name} {self.date_began}"

# Links one or more authors to one or more references
class Authorship(models.Model):
    reference = models.ForeignKey('Reference', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    author_type = models.CharField(max_length=2, choices=AUTHOR_TYPES)

    class Meta:
        db_table='reference_author'

# Citations are composed of one or more references
class Citation(models.Model):
    references = models.ManyToManyField('Reference')
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'citation'


class Country(models.Model):
    name = models.CharField(max_length=128, blank=False)

    class Meta:
        db_table = 'country'

    def __str__(self):
        return f"{self.name}"


# Reference are heirarchical in nature.  Lower-level objects (like verse), can be
#   children of zero or more parents.  In this way, low level objects can be organized
#   in many different ways
class Reference(models.Model):
    title = models.CharField(max_length=128, blank=False, null=True)
    # Don't remove children when the parent if deleted
    # Since a reference can have multiple parents, store children
    children_references = models.ForeignKey('Reference', on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name="child reference")
    reference_type = models.CharField(max_length=2, choices=REFERENCE_TYPES)
    date_published = models.DateField()
    #authors = models.ManyToManyField(Author)
    # Many to many - Reference could have many authors and authors many references
    #   We also need to store stuff about the relationship - use 'through' for that
    #   so we can define specific table
    authors = models.ManyToManyField('Author', through='Authorship')

    class Meta:
        db_table='reference'
        ordering = ['reference_type','title']

    def __str__(self):
        return f"{self.reference_type} - {self.title}"

# Extension of contrib user user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_on = models.DateField(auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
