
import pickle
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
            raise ValueError("phone number must contain only digits")
        if len(phone) != 10: 
            raise ValueError("phone number must have 10 digits")
        super().__init__(phone) # эта строка вызывает конструктор класса  Field и передает в него телефонный номер. То есть при успешной првоерке номера, мы передаем номер в конструктор класса Field где он будет сохранен в атрибуте value
            
class Record:
    def __init__(self, name) :
        self.name = Name(name) #здесь создаем обьект класса Name котор хранит имя контакта мы используем класс Name чтобы унаследов его свойства 
        self.phones = []  #атрибут обьекта (список)
    def add_phone(self, phone): 
        self.phones.append(Phone(phone))  #(Phone(phone)) это создание нового обьекта класса Phone, который содержит номер телефона
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
        return f" Contact name: {self.name.value}, phones: {'__'.join(p.value for p in self.phones)}  "

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
    def add_record(self, record):
        self.data[record.name.value] = record  #это ключ для хранения записи в словаре self.data
    def find(self, name):
        return self.data.get(name, None)  #вызывает метод get для словаря self.data чтобы получить значение по ключу name
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    def __str__(self):
         # возвращаем строковое представление всех записей в адресной книге
        return '  '.join(str(record) for record in self.data.values())

def save_data(book, filename = "name.pkl"): ###### book обьект adressbook 
    with open(filename, "wb") as f :########
        pickle.dump(book, f)#########
def load_data(filename = "name.pkl"):####### ##
    try:
        with open(filename, "rb") as f:## #
            return pickle.load(f)######## возвр обьект adressbook
    except FileNotFoundError: #### если файл не найден 
        return AddressBook()### возвр пустой обьект adressbook
    
            
def main():
    book = load_data() 
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)
    
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    print(book) #Виведення всіх записів у книзі
    
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)
    
    found_phone = john.find_phone("5555555555")
    print(f"\n{john.name}: {found_phone}") 
    book.delete("Jane")
    print(book)
    save_data(book)  #сохранение книги перед выходом
    print("saved")

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