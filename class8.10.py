class Person:
    __slots__ = ['name', 'height', '__birthday']
    species = "human"

    def __init__(self, name, height, birthday):
        self.name = name
        self.height = height
        self.__birthday = birthday

    def greet(self):
        return "My name is {}.".format(self.name)

    def species_name(self):
        return "I am a {}.".format(Person.species)

    def get_info(self):
        return f"Name: {self.name}, Height: {self.height}"

    def __get_birthday(self):
        return self.__birthday

    def __call__(self):
        return self.get_info()

class Student(Person):
    __slots__ = ['age', 'score']

    def __init__(self, name, height, age, score, birthday):
        super().__init__(name, height, birthday)
        self.age = age
        self.score = score

    def greet(self):
        return f"My name is {self.name}."

    def get_age(self):
        return self.age

    def get_score(self):
        return self.score

    def __call__(self):
        return f"Student: {self.name}, Age: {self.age}, Score: {self.score}"

def get_best_student(*students):
    best_student = students[0]
    for stu in students[1:]:
        if stu.get_score() > best_student.get_score():
            best_student = stu
    return best_student

student1 = Student("Haha", 165, 17, 95, "2004-12-30")
student2 = Student("Lala", 169, 18, 90, "2004-12-03")
print(student1.species_name())
print(student1.greet())
print(student1.get_info())
print(f"Best student: {get_best_student(student1, student2).name}")
print(student1()) #call
print(student1._Person__get_birthday())
print(student2._Person__get_birthday())