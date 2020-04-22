class Miss_Anna:

    def __init__(self, student, asignation, birthday):
        self.student = student
        self.homework = asignation
        self.birthday = birthday
    
    def __str__(self):
        return f"Remember, today is {self.birthday}, and is {self.student}\'s Birthday!"
    
    
    def morning_asignation(self):
        return f'{self.student} today is your class of {self.homework}'


class teachers:

    def __init__(self, profesor, asignation):
        self.profesor = profesor
        self.asignation = asignation
    
    def __repr__(self):
        return f'{self.profesor} is aisgnated to '

    def agenda(self):
        return f'{self.profesor}'



# eva = missAnna exam today
# miss anna = teachers, friday is museumvisit

# print ( eva.morning asig)
# print (anna.agenda)

martin = Miss_Anna('Mickey', 'chineese', 'Dec, 12')
# eva = Miss_Anna('Eva', 'be kind others', 'Sep, 10')


print(martin.morning_asignation())
print(str(martin))

# print(eva.morning_asignation())
# print(str(eva))