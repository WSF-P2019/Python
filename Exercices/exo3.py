# Q1.2
class Voiture(object):
  pass

#Q1.3
renault = Voiture()

#Q1.4
print renault

#Q1.5
class Voiture(object):
  def __init__(self, arg):
    super(Voiture, self).__init__() # Bonne pratique ;)

#Q1.6
class Voiture(object):
  color = 'red' # Définition d'un attribut
  name = 'basicName'
  def __init__(self, arg):
    super(Voiture, self).__init__() # Bonne pratique ;)

#Q1.7
renault = Voiture()
print renault.color

#Q1.8
renault = Voiture()
renault.color = 'green' # Modification de l'attribut

#Q1.9
renault = Voiture()
renault.name = 'maPetiteVoiture' # Définition à la volée
print renault.name

#Q1.10
def set_name(self, arg):
  self.name = arg

renault.set_name('newName')

#Q2.1
class Ferrari(object):
  def __init__(self, arg):
    super(Ferrari, self).__init__() # Bonne pratique ;)

class Mercedes(object):
  def __init__(self, arg):
    super(Mercedes, self).__init__() # Bonne pratique ;)

#Q2.2
class Ferrari(Voiture):
  def __init__(self, arg):
    super(Ferrari, self).__init__() # Bonne pratique ;)

class Mercedes(Voiture):
  def __init__(self, arg):
    super(Mercedes, self).__init__() # Bonne pratique ;)

classA = Mercedes()
F430 = Ferrari()
print classA.name
F430.name = 'newName'
print F430.name

#Q2.3
class Ferrari(Voiture):
  speed = '300'
  def __init__(self, arg):
    super(Ferrari, self).__init__() # Bonne pratique ;)

F430 = Ferrari()
print F430.speed

#Q2.4
class Mercedes(Voiture):
  speed = '300'
  def __init__(self, arg):
    super(Mercedes, self).__init__() # Bonne pratique ;)

classA = Mercedes()
print classA.speed

#3.1
def deco(myFunction):
  return myFunction

@deco
def myFunction(arg):
  print arg

myFunction('lol')

#Q3.2
def deco_multiply(myFunction):
  def myNewFunction(arg):
    return myFunction(arg * 2)
  return myNewFunction

@deco_multiply
def myFunction(arg):
  print arg

myFunction(3)

# BONUS /o/
def deco_multiply(paramDuDecorateur): # On passe le param' en premier
  def func(myNumber): # Puis on rajoute un cran pour y passer la function
    def myNewFunction(arg):
      return myNumber(arg * paramDuDecorateur)
    return myNewFunction
  return func

@deco_multiply(5) # Si on passe un paramDuDecorateur
def myNumber(arg):
  print arg

myNumber(3)

#Q3.3

def deco_is_admin(checkRole):
  def checkAdmin(roles):
    if roles.has_key('admin'):
      return raise Exception
    else:
      return checkRole(roles)
  return checkAdmin

@deco_is_admin
def checkRole(roles):
  print roles

roles = {'admin':True}
checkRole(roles)

# Q3.4
def deco_is_admin(checkRole):
  def checkAdmin(roles):
    if roles['admin'] is not True:
      return raise Exception
    else:
      return checkRole(roles)
  return checkAdmin

@deco_is_admin
def checkRole(roles):
  print roles

roles = {'admin':True}
checkRole(roles)
