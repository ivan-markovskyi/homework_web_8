from typing import Any
from models import Author, Quote


def find_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


def find_by_author(author: str) -> list[list[Any]]:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == "__main__":
    while True:
        user_input = input(
            "Введіть команду у форматі 'name: Steve Martin' або 'tag:life' >>> "
        )
        if user_input == "exit":
            break

        user_info = user_input.split(":")

        try:
            if user_info[0].strip() == "name":
                print(find_by_author(user_info[1]))
            elif user_info[0].strip() == "tag":
                tags = user_info[1].split(",")
                print([find_by_tag(el) for el in tags])
            else:
                print("Команди введені не коректно")
        except IndexError:
            print("Дані введено не коректно")
