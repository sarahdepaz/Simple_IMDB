import os
import sys
import re


def create_db():
    db = {}
    with open("movies.txt") as data:
        for line in data.readlines():
            actor, *movies = line.split(",")
            for m in movies:
                m = m.strip()
                db[m] = db.get(m, []) + [actor]
    return db


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


def symmetric_difference(lst1, lst2):
    final_list = list(set(lst1).symmetric_difference(set(lst2)))
    return final_list


def print_queries_helper(res):
    res = sorted(res)
    makeitastring = ', '.join(map(str, res))
    return makeitastring


def clean(list1):
    clean_list = []
    for string in list1:
        string = string.lstrip()
        string = string.rstrip()
        string = string.strip()
        clean_list.append(string)
    return clean_list


def query_by_movie():
    user_query = input("Please select two movies and an operator(&,|,^) separated with ',':\n")
    user_query = user_query.split(",")  # a is converted to a list of strings.
    my_query_list = user_query
    # cleaning trailing whitespace
    clean_list = clean(my_query_list)
    if len(clean_list) < 2:
        print("Error\n")
        entry_menu()
    if (clean_list[-1] != '&') and (clean_list[-1] != '|') and (clean_list[-1] != '^'):
        print("Error\n")
        entry_menu()
    new_db = create_db()
    if clean_list[0] not in new_db:
        entry_menu()
    if clean_list[1] not in new_db:
        entry_menu()
    first_movie_actors = new_db.get(clean_list[0])
    second_movie_actors = new_db.get(clean_list[1])
    if clean_list[-1] == '&':
        # we need the actors that performed in both movies
        res = intersection(first_movie_actors, second_movie_actors)
        res = print_queries_helper(res)
        if len(res) == 0:
            print("There are no actors in this group\n")
            entry_menu()
        else:
            print(res)
            entry_menu()
    if clean_list[-1] == '|':
        res = union(first_movie_actors, second_movie_actors)
        res = print_queries_helper(res)
        if len(res) == 0:
            print("There are no actors in this group\n")
            entry_menu()
        else:
            print(res)
            entry_menu()
    if clean_list[-1] == '^':
        res = symmetric_difference(first_movie_actors, second_movie_actors)
        res = print_queries_helper(res)
        if len(res) == 0:
            print("There are no actors in this group\n")
            entry_menu()
        else:
            print(res)
            entry_menu()


def check_actor(actor_query):
    new_db = create_db()
    if actor_query in [x for v in new_db.values() for x in v]:
        return True
    else:
        return False


def query_by_actor():
    actor_query = input("Please select an actor:\n")
    # cleaning strings from extra trailing spaces
    actor_query = actor_query.strip()
    actor_query = actor_query.rstrip()
    actor_query = actor_query.lstrip()
    new_db = create_db()
    bool = check_actor(actor_query)
    if bool == False:
        entry_menu()
    all = set()
    for key in new_db:
        lst = new_db[key]
        if actor_query in lst:
            all = all.union(set(lst))
    all.remove(actor_query)
    res = sorted(all)
    makeitastring = ', '.join(res)
    print(makeitastring)


def clean_data(list_to_clean):
    for i in range(0, len(list_to_clean)):
        list_to_clean[i] = re.sub(' +', ' ', list_to_clean[i]).strip()
        list_to_clean[i] = re.sub(' +', ' ', list_to_clean[i]).rstrip()
        list_to_clean[i] = re.sub(' +', ' ', list_to_clean[i]).lstrip()
    return list_to_clean


def insert_a_new_movie():
    update_db = input("Please insert a new movie:\n")
    update_db = update_db.split(",")
    my_update_list = update_db
    if len(my_update_list) < 2:
        print("Error\n")
        entry_menu()
    # clean data
    my_update_list = clean(my_update_list)
    new_db = create_db()
    actors_to_add = my_update_list[1:]
    if my_update_list[0] in new_db.keys():  # the movie in the db
        new_db[my_update_list[0]] = union(actors_to_add, new_db[my_update_list[0]])
    else:
        new_db[my_update_list[0]] = my_update_list[1:]
    save_to_file(new_db)
    entry_menu()


def save_to_file(new_db):
    # will return the most recent db
    all = set()
    f = open("output.txt", "a+")
    for key in new_db:
        lst = new_db[key]
        all = all.union(set(lst))
    sorted_actors = sorted(all)

    f.close()
    entry_menu()


def entry_menu():
    user_choice = int(input("Please select an option:\n"
                            "1) Query by movies\n"
                            "2) Query by actor\n"
                            "3) Insert a new movie\n"
                            "4) Save and Exit\n"
                            "5) Exit\n"))
    flag = 1
    while flag:
        if user_choice == 1:
            query_by_movie()
        elif user_choice == 2:
            query_by_actor()
        elif user_choice == 3:
            insert_a_new_movie()
        elif user_choice == 4:
            save_to_file()
        elif user_choice == 5:
            flag = 0
            sys.exit(1)


entry_menu()

