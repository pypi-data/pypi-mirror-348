from setuptools import setup

setup(
    name="prophet-tool", # имя модуля, которое будет использоваться при установке через pip install
    version="0.1", # версия модуля. при каждом обновлении её надо увеличивать
    description="Мои личные инструменты", # описание проекта, его можно не использовать
    packages=["prophet-tool"], # список с названиями папок, которые нужно залить
    author_email="prophet.incorporated@gmail.com", # почта автора
    zip_safe=False, # пароль, можно не указывать
    install_requires = [], # список дополнительных модулей, которые необходимы для использования вашего модуля
)