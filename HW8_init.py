import pickle
from datetime import datetime, timedelta
from collections import UserDict
class Field:
    def __init__(self, value) :   #метод __init__ который вызывается при создании нового обьекта класса (конструктор). Аргумент - value
        self.value = value   #self - это ссылка на текущий обьект класса 
    def __str__(self) :  #метод __str__ это метод котор возвр строковое представление обьекта. Он автоматически вызывается когда мы пытаемся ввести обьект с помощью функции print() или мы хотим преобразов обьект в  строку 
        return str(self.value) # преобразование значения value в строку 
class Name(Field): #класс для хранения имени контакта наследует Field. это пустой класс который полностью использует функционал род класса  Field
    pass
class Phone(Field): 
    def __init__(self, phone): 
        if not phone.isdigit(): 
            raise ValueError("Phone number must contain only digits") 
        if len(phone) != 10: 
            raise ValueError("Phone number must have 10 digits")
        super().__init__(phone) # эта строка вызывает конструктор класса  Field и передает в него телефонный номер. То есть при успешной првоерке номера, мы передаем номер в конструктор класса Field где он будет сохранен в атрибуте value

##new class### 
class Birthday(Field): 
    def __init__(self, value): 
        try: 
            datetime.strptime(value, "%d.%m.%Y") 
            self.value = value  # Сохраняем как строку
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    def __str__(self):
        return self.value # Возвращаем строковое представление
    
    
class Record:
    def __init__(self, name):
        self.name = Name(name) #здесь создаем обьект класса Name котор хранит имя контакта/ мы используем класс Name чтобы унаследов его свойства 
        self.phones = []  #атрибут обьекта (список)
        self.birthday = None
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday) #добавляем обьект класса Birthday, передавая строку с датой
    def add_phone(self, phone): 
        phone_obj = Phone(phone)  #(Phone(phone)) это создание нового обьекта класса Phone, который содержит номер телефона
        self.phones.append(phone_obj) 
    def remove_phone(self, phone): 
        self.phones =[p for p in self.phones if p.value != phone]  #p.value атрибут обьекта Phone
    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone): #существует ли старый номер в списке телефонов 
            raise ValueError(f"old phone {old_phone} not found")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
    def find_phone(self, phone):
        for p in self.phones : #Проходим по каждому объекту телефона в списке
            if p.value == phone:     # Если номер телефона совпадает с переданным возвращаем объект
                return p
        return None
     # Возвращаем строковое представление контакта
    def __str__(self) -> str:
        phones = ' ,  '.join(p.value for p in self.phones)
        birthday= str(self.birthday) if self.birthday else "not specified"
        return f" Contact name: {self.name.value}, phones: {phones}, birthdays: {birthday}  "

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record #это ключ для хранения записи в словаре self.data
    def find(self, name):
        return self.data.get(name, None) #вызывает метод get для словаря self.data чтобы получить значение по ключу name
    def delete(self, name):
        if name in self.data:
            del self.data[name] #удаляет запись по ключу если он есть 
            
    def get_upcoming_birthdays(self): 
        today= datetime.now().date() #получаем текущую дату без учета времени 
        upcoming_birthdays= [] 
        for record in self.data.values(): #Проходим по всем записям в адресной книге. self.data - словарь, ключи - имена контактов, а значения - обьекты Record
            if record.birthday: #проверяем есть ли дата рождения birthday 
                #берем день рождения в текущем году
                birthday_date = datetime.strptime(record.birthday.value,"%d.%m.%Y" ).date()
                birthday_this_year= birthday_date.replace(year = today.year) #с помощью replace устанавливаем текущий год для дня рождения  	
            # проверяем если день рождения уже прошел в этом году
                if birthday_this_year < today: 
                    birthday_this_year = birthday_this_year.replace(year = today.year + 1) #если др был в этом году (дата меньше сегодняшней) переносим на след год
                days_untill= (birthday_this_year - today).days #тут просто получаем кол-во дней до др 
                if 0 <= days_untill <= 7: 
                #корректировка выходных только для вывода
                    if birthday_this_year.weekday() == 5: #суббота 
                        birthday_this_year += timedelta(days=2)
                    elif birthday_this_year.weekday() == 6: #воскресе
                        birthday_this_year += timedelta(days = 1)
        
                    upcoming_birthdays.append ({  #создаем словарь с двумя ключами 
                        "name" : record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y") })
        return upcoming_birthdays
        
    def __str__(self):
         # возвращаем строковое представление всех записей в адресной книге
        return ' ------'.join(str(record) for record in self.data.values())
def save_data(book, filename = "name.pkl"): ###### book обьект adressbook 
    with open(filename, "wb") as f :########
        pickle.dump(book, f)#########
def load_data(filename = "name.pkl"):####### ##
    try:
        with open(filename, "rb") as f:## #
            return pickle.load(f)######## возвр обьект adressbook
    except FileNotFoundError: #### если файл не найден 
        return AddressBook()### возвр пустой обьект adressbook

##########  декораторы ошибок #######
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return str(e)
    return inner
def parse_input(user_input):
    cmd, *args = user_input.split()  # Разбивает ввод пользователя на отдельные слова
    cmd = cmd.strip().lower()
    return cmd, args
@input_error
def add_birthday(args, book):
    name, birthday = args # Разбираем аргументы: имя и дату рождения
    record = book.find(name) #ищем запись по имени 
    if record:
        record.add_birthday(birthday)  #добавл день рождения в запись 
        return f" HB {name}: added"
    return f"contact {name}:  not found"
@input_error
def show_birthday(args, book):
    name = args[0] #  извлекаем имя контакта 
    record = book.find(name) # ищем контакт в адресной книге.
    if record and record.birthday: 
        return f" HB {name}: {record.birthday}"
    elif record:
        return f"{name} not found "
    return f" {name} not found"
@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays() # получаем список ближайших дней рождения
    if upcoming_birthdays:
        result = " soon: "  
        for entry in upcoming_birthdays:
            result += f"{entry['name']}: {entry['birthday']} "
        return result
    return " no birthdays"

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        # return f"Контакт {name} добавлен с телефоном {phone}"
    record.add_phone(phone)
    return f" added:::::    {name}"        
     
@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name) #здесь мы ищем контакт по имени в адресной книге
    if not record:
        return f"contact {name} not found "    
    if not record.find_phone(old_phone):
        return f"in contact {name} number not found {old_phone}"
    record.edit_phone(old_phone, new_phone)
    return f"in number name: {name}. changed on {new_phone}"  

@input_error   
def get_phone(args, book):
    name = args[0] #получаем первое значение из списка args, которое должно быть именем контакта, для которого запрашиваются номера телефонов
    record = book.find(name)
    if record and record.phones:
        phones = ', '.join(p.value for p in record.phones)
        return f"{name}: {phones}"
    elif record:
        return f"error"
    return f"contact {name} not found "

def all_contacts(book):
    if book.data:
        return "\n".join(str(record) for record in book.data.values()) 
    else:
        return "no contacts"
        

def main():
    book = AddressBook()
    print("welcome")
    while True:
        user_input = input("enter command:")
        command, args = parse_input(user_input)
        if command == "close" or command == "exit":
            print("Good bye")
            break 
        elif command == "hello":
            print("how can i help you")
        elif command == "add":
            print(add_contact(args, book))            
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("invalid command")
            
if __name__ == "__main__":
    main()   


# # Створення нової адресної книги
# book = AddressBook()
# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# # Додавання запису John до адресної книги
# book.add_record(john_record)
# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)
# # Виведення всіх записів у книзі
# print(book)
# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555
# # Видалення запису Jane
# book.delete("Jane")











