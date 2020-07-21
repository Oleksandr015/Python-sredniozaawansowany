from dataclasses import dataclass
from typing import *
from abc import *

"""

    1. Mamy zdefiniowane składniki.
    2. Mamy zdefiniowane posiłki i ich cenę
    3. Możemy tworzyć zamówienia.
    4. Możemy przypisać kucharza do zamówienia.
    
    Wszystko zapisujemy do plików.
    Robimy najprościej jak się da.
    Menu aplikacji oparte o 1,2,3...

"""


class FileWritable(ABC):

    @staticmethod
    @abstractmethod
    def file_name():
        pass

    @abstractmethod
    def to_csv_string(self, sep=';'):
        pass

    @staticmethod
    @abstractmethod
    def from_csv_string(csv_string, sep=';', members=None):
        pass


@dataclass
class Ingredient(FileWritable):
    id: int
    name: str

    @staticmethod
    def file_name():
        return 'ingredients.csv'

    @staticmethod
    def from_csv_string(csv_string: str, sep=';', **kwargs):
        splited = csv_string.strip().split(sep)
        return Ingredient(int(splited[0]), splited[1])

    def to_csv_string(self, sep=';'):
        return f'{self.id};{self.name}'


@dataclass
class Meal(FileWritable):
    id: int
    name: str
    ingredients: List[Ingredient]

    @staticmethod
    def file_name():
        return 'meals.csv'

    @staticmethod
    def from_csv_string(csv_string: str, members=None, sep=';'):
        if members is None:
            raise Exception
        ingredients_dict = {ingredient.id: ingredient for ingredient in members}
        splited = csv_string.split(sep)
        return Meal(int(splited[0]), splited[1], Meal.__map_ingredients(splited[2], ingredients_dict))

    def to_csv_string(self, sep=';'):
        ingredients = ','.join(map(lambda i: str(i.id), self.ingredients))
        return f'{self.id};{self.name};{ingredients}'

    @staticmethod
    def __map_ingredients(ids_string: str, ingredients: Dict[int, Ingredient]):
        ids = map(int, ids_string.split(','))
        return [ingredients[id] for id in ids]


@dataclass
class Cook(FileWritable):
    id: int
    first_name: str
    last_name: str

    @staticmethod
    def file_name():
        return 'cooks.csv'

    @staticmethod
    def from_csv_string(csv_string, sep=';', members=None):
        splited = csv_string.strip().split(sep)
        return Cook(int(splited[0]), splited[1], splited[2])

    def to_csv_string(self, sep=';'):
        return f'{self.id}{sep}{self.first_name}{sep}{self.last_name}'


@dataclass
class Order(FileWritable):
    id: int
    cook: Cook
    meals: List[Meal]

    @staticmethod
    def file_name():
        return 'orders.csv'

    @staticmethod
    def from_csv_string(csv_string, sep=';', members=None):
        cooks = members['cooks']
        meals = members['meals']

        cooks_dict = {cook.id: cook for cook in cooks}
        meals_dict = {meal.id: meal for meal in meals}

        splited = csv_string.strip().split(sep)

        return Order(
            int(splited[0]),
            cooks[int(splited[1])],
            Order.__map_meals(splited[2], meals)
        )

    def to_csv_string(self, sep=';'):
        meals = map(lambda x: str(x.id), self.meals)
        return f'{self.id}{sep}{self.cook.id}{sep}{meals}'

    @staticmethod
    def __map_meals(ids_string: str, meals: Dict[int, Meal]):
        ids = map(int, ids_string.split(','))
        return [meals[id] for id in ids]


def read_ingredients():
    return read_csv_file(Ingredient)


def read_meals():
    ingredients = read_ingredients()
    return list(read_csv_file(Meal, members=ingredients))


def read_orders():
    pass


def read_cooks():
    pass


def write_csv_file(cls: Type[FileWritable], objects: List[FileWritable], encoding='utf-8', sep=';'):
    with open(cls.file_name(), 'w', encoding=encoding) as f:
        for object in objects:
            f.write(object.to_csv_string(sep=sep) + '\n')


def read_csv_file(cls: Type[FileWritable], encoding='utf-8', sep=';', members=None):
    with open(cls.file_name(), 'r', encoding=encoding) as f:
        for line in f:
            yield cls.from_csv_string(line, sep=sep, members=members)


if __name__ == '__main__':
    i1 = Ingredient(1, 'pomidor')
    i2 = Ingredient(2, 'papryka')

    meal = Meal(1, 'Sałatka Szewska', [i1, i2])
    print(meal.to_csv_string())
    print(meal)
    write_csv_file(Meal, [meal])
    write_csv_file(Ingredient, [i1, i2])
    meals = read_meals()
    print(meals)
