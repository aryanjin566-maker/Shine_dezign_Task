# Parent class
class animal_parent:
   def sound(self):
      print("hello")
   
# Child class
class dog_child(animal_parent):
   def sound(self):
      print("bye")

class person:
   def __init__(self):
      self.__name = "aryan"

   def get_name(self):
        return self.__name
   

dog = dog_child()
dog.sound()  

animal = animal_parent()
animal.sound()  

person_instance = person()
print(person_instance.get_name())  
   
    
