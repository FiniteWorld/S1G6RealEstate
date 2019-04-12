from django.db import models
from enum import Enum
import datetime


# Create your models here.
class PropertyCategoryChoice(Enum):
    SingleHouse = "Single House"
    AttachedHouse = "Attached House"
    TownHouse = "Town House"
    Apartment = "Apartment"
    Store = "Store"
    Farm = "Farm"
    Factory = "Factory"
    Mall = "Mall"
    Building = "Building"
    Other = "Other"


class Property_Category(models.Model):
    propertyCategory = models.CharField(max_length=25,
                                        choices=[(tag.value, tag.name) for tag in PropertyCategoryChoice])

    def __str__(self):
        return self.propertyCategory


class PropertySectorChoice(Enum):
    Private = "Private"
    Residential = "Residential"
    Commercial = "Commercial"
    Government = "Government"
    Rural = "Rural"
    Other = "Other"


class Property_Sector(models.Model):
    SECTOR_CHOICES = (
        ('Private', 'Private'),
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Government', 'Government'),
        ('Rural', 'Rural'),
        ('Other', 'Other'),
    )
    propertySector = models.CharField(max_length=25, choices=SECTOR_CHOICES, default='Private')

    def __str__(self):
        return self.propertySector


class PropertyFacingChoice(Enum):
    North = "North"
    South = "South"
    East = "East"
    West = "West"
    Other = "Other"


class Property_Facing(models.Model):
    propertyFacing = models.CharField(max_length=25,
                                      choices=[(tag.value, tag.name) for tag in PropertyFacingChoice])

    def __str__(self):
        return self.propertyFacing


class Property(models.Model):
    def __str__(self):
        return str(self.propertyID)

    propertyID = models.AutoField(primary_key=True)
    propertyTitle = models.CharField(max_length=100)
    propertyCategory = models.CharField(max_length=25,
                                        choices=[(tag.value, tag.name) for tag in PropertyCategoryChoice])
    propertySector = models.CharField(max_length=25,
                                      choices=[(tag.value, tag.name) for tag in PropertySectorChoice])
    propertyFacing = models.CharField(max_length=25,
                                      choices=[(tag.value, tag.name) for tag in PropertyFacingChoice])
    propertyCountry = models.CharField(max_length=100)
    propertyProvince = models.CharField(max_length=100)
    propertyCity = models.CharField(max_length=100)
    propertyStreet = models.CharField(max_length=100)
    propertyPostalCode = models.CharField(max_length=100)
    propertyStreetNumber = models.CharField(max_length=100)
    propertyConstructionDate = models.DateField()
    propertyRegisterationDate = models.DateField()
    propertyNoofHalls = models.IntegerField()
    propertyNumberOfRooms = models.IntegerField()
    propertyNoofBathrooms = models.FloatField()
    propertyNoofFloors = models.IntegerField()
    propertyTotalArea = models.FloatField()
    propertyAskingPrice = models.CharField(max_length=100)
    propertySellingPrice = models.CharField(max_length=100)
    memberName = models.CharField(max_length=100)

    def __str__(self):
        return str(self.propertyTitle)


class PropertyImages(models.Model):
    def __str__(self):
        return self.propertyImageDescription

    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    memberName = models.CharField(max_length=100)
    propertyImageID = models.CharField(max_length=100)
    propertyImageDescription = models.CharField(max_length=500)
    propertyImage = models.ImageField(blank=True, null=True)


class Country(models.Model):
    countryName = models.CharField(max_length=100)

    def __str__(self):
        return str(self.countryName)


class Province(models.Model):
    countryName = models.ForeignKey(Country, on_delete=models.CASCADE)
    provinceName = models.CharField(max_length=100)

    def __str__(self):
        return str(self.provinceName)


class City(models.Model):
    countryName = models.ForeignKey(Country, on_delete=models.CASCADE)
    provinceName = models.ForeignKey(Province, on_delete=models.CASCADE)
    cityName = models.CharField(max_length=100)

    def __str__(self):
        return str(self.cityName)


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    userName = models.CharField(max_length=50)

    def __str__(self):
        return str(self.firstName)

    def roles(self):
        return ', '.join([a.name for a in self.user.role_set.all()])


class Password(models.Model):
    userId = models.OneToOneField(User, primary_key=True, related_name="password", on_delete=models.CASCADE)
    encryptedPassword = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    userAccountExpiryDate = models.DateField(default=datetime.date.today, blank=True)
    passwordMustChanged = models.DateField(default=datetime.date.today, blank=True)

def __str__(self):
    return "User Id: " + str(self.userId) + "UserName: " + str(User.userName)


class Role(models.Model):
    name = models.CharField(max_length=55)
    users = models.ManyToManyField(User, through='UserRole')

    def __str__(self):
        return self.name

    def permissions(self):
        return ', '.join([a.sysFeature for a in self.permission_set.all()])


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return ' | '.join([self.user.__str__(), self.role.__str__(), self.date_assigned.__str__()])


class Permission(models.Model):
    code = models.CharField(max_length=10)
    sysFeature = models.CharField(max_length=75)
    roles = models.ManyToManyField(Role, through='RolePermission')

    def __str__(self):
        return self.sysFeature


class RolePermission(models.Model):
    PERMISSION_TYPE = (
        ('read', 'Read'),
        ('write', 'Write'),
        ('update', 'Update'),
        ('delete', 'Delete')
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    permissionType = models.CharField(max_length=20, choices=PERMISSION_TYPE)

    def __str__(self):
        return ' | '.join([self.role.__str__(), self.permission.__str__(), self.permissionType.__str__()])
