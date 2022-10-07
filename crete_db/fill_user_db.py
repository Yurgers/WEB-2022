from faker import Faker

from service.password import get_password_hash
from src.database import Session
from src.models import User
from datetime import timezone


fake = Faker('ru_RU')

# db_obj = self.model(**obj_in.dict())
session = Session()

for i in range(100):
    profile = fake.simple_profile()

    user = User(
        username=profile['username'],
        password=get_password_hash('secret'),
        name=profile['name'],
        email=profile['mail'],
        gender=profile['sex'],
        birthdate=profile['birthdate'],
    )
    print(user)

    session.add(user)

session.commit()

'''ROLI
  - администратор проекта
  - руководитель
  - сотрудниками HR
  - коллег 
  


'''
