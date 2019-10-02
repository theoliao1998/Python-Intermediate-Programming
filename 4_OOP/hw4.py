'''
SI 507 F19 homework 4: Classes and Inheritance

Your discussion section:
People you worked with:

######### DO NOT CHANGE PROVIDED CODE ############ 
'''

#######################################################################
#---------- Part 1: Class
#######################################################################

'''
Task A
'''
from random import randrange
class Explore_pet:
    boredom_decrement = -4
    hunger_decrement = -4
    boredom_threshold = 6
    hunger_threshold = 10
    def __init__(self, name="Coco"):
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)

    def mood(self):
        if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
            return "happy"
        elif self.hunger > self.hunger_threshold:
            return "hungry"
        else:
            return "bored"

    def __str__(self):
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state
coco = Explore_pet()

#your code begins here . . . 
coco.hunger = coco.hunger_threshold
coco.boredom = coco.boredom_threshold - coco.boredom_decrement
#print(coco)

brian = Explore_pet("Brian")
brian.hunger = brian.hunger_threshold - brian.hunger_decrement
#print(brian)

'''
Task B
'''
#add your codes inside of the Pet class
class Pet:
    boredom_decrement = -4
    hunger_decrement = -4
    boredom_threshold = 6
    hunger_threshold = 10

    def __init__(self, name="Coco"):
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)
        self.words = ["hello"]

    def mood(self):
        if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
            return "happy"
        elif self.hunger > self.hunger_threshold:
            return "hungry"
        else:
            return "bored"
    
    def clock_tick(self):
        self.hunger += 2
        self.boredom += 2
    
    def say(self):
        print("I know how to say:")
        for word in self.words:
            print(word)
    
    def teach(self,word):
        self.words.append(word)
        self.boredom = 0 if (self.boredom+self.boredom_decrement<0) else self.boredom+self.boredom_decrement
    
    def feed(self):
        self.boredom = 0 if (self.hunger+self.hunger_decrement<0) else self.hunger+self.hunger_decrement
    
    def hi(self):
        print(self.words[randrange(len(self.words))])
        

    def __str__(self):
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state

'''
Task C
'''

def teaching_session(my_pet,new_words):
    #your code begins here . . . 
    for word in new_words:
        my_pet.teach(word)
        my_pet.hi()
        print(my_pet)
        if my_pet.mood == "hungry":
            my_pet.feed()
        my_pet.clock_tick()

        
mypet = Pet("Pett")
teaching_session(mypet,['I am sleepy', 'You are the best','I love you, too'])




#######################################################################
#---------- Part 2: Inheritance - subclasses
#######################################################################
'''
Task A: Dog and Cat    
'''
#your code begins here . . . 

class Dog(Pet):
    def __str__(self):
        return super().__str__().replace(".",", arrrf!")

class Cat(Pet):
    def __init__(self, meow_count, name="Coco"):
        super().__init__(name)
        self.meow_count = meow_count
    
    def hi(self):
        word = self.words[randrange(len(self.words))]
        print("".join([word for _ in range(self.meow_count)]))


'''
Task B: Poodle 
'''
#your code begins here . . . 

class Poodle(Dog):
    def dance(self):
        return "Dancing in circles like poodles do!"
    
    def say(self):
        print(self.dance())
        return super().say()

mypet2 = Poodle("Poo")
mypet2.say()

mypet3 = Cat(5,"Kitty")
mypet3.hi()


