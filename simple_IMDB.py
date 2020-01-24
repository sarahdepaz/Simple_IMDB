import os
import sys

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: create_db	*

* The Input: A movies txt file in the given format	*

* The output: A dictionary called db, where the keys are the movies, *

* And the values are the list of actors appeared in. *

* The Function operation: Reads line by line from the file and unpacks the data to the dictionary*

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def create_db(movies_file):
    db = {}
    f = open(movies_file)
    for line in f.readlines():
        actor, *movies = line.split(",")
        for m in movies:
            m = m.strip()
            # uses get to locate if the value-movie already exists
            db[m] = db.get(m, []) + [actor]
    return db


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: intersection	*

* The Input: Two lists	*

* The output: The intersection of the two lists *

* The Function operation: List comprehension - iterates on the values of lst1 *

* Adds it to lst3 if appeared in lst2 as well. *
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: union	*

* The Input: Two lists	*

* The output: A list which is the union of the two given lists *

* The Function operation: Converts the list to sets, calculates their union *

* Converts it back to a list and returns the unified list *
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: symmetric_difference*

* The Input: Two lists	*

* The output: A list which is the symmetric difference of the two given lists *

* The Function operation: Converts the list to sets, calculates their symmetric difference *

* Converts it back to a list and returns the new list *
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def symmetric_difference(lst1, lst2):
    final_list = list(set(lst1).symmetric_difference(set(lst2)))
    return final_list


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: print_queries_helper *

* The Input: A result of a query (list)	*

* The output: A String, which is also sorted *

* The Function operation: Sorts the list and then coverts it to a string *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def print_queries_helper(res):
    res = sorted(res)
    makeitastring = ', '.join(map(str, res))
    return makeitastring


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: clean *

* The Input: A query (list)	*

* The output: A list which has been cleaned from trailing whitespaces *

* The Function operation: Iterates on the given list, uses strips to remove the whitespaces *

* Appends the cleaned list to a new one and return it *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def clean(list1):
    clean_list = []
    for string in list1:
        string = string.lstrip()
        string = string.rstrip()
        string = string.strip()
        clean_list.append(string)
    return clean_list


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: query_by_movie *

* The Input: A data-base (dictionary)	*

* The output: The result of the user's query *

* The Function operation: Gets the query from the user in the requested format *

* If '&' is given we return the intersection of the actors appeared in both given movies *

* If '|' is given we return the union of the actors appeared in both given movies *

* If '^' is given we return the symmetric difference of the actors appeared in both given movies *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def query_by_movie(our_db):
    user_query = input("Please select two movies and an operator(&,|,^) separated with ',':\n")
    user_query = user_query.split(",")  # the query is converted to a list of strings.
    my_query_list = user_query
    # cleaning trailing whitespace
    clean_list = clean(my_query_list)
    # Invalid input
    if len(clean_list) < 2:
        print("Error")
        return
    # Invalid input
    if (clean_list[-1] != '&') and (clean_list[-1] != '|') and (clean_list[-1] != '^'):
        print("Error")
        return
    # Invalid input
    if clean_list[0] not in our_db:
        return
    # Invalid input
    if clean_list[1] not in our_db:
        return
    # gets the actors that appeared in the given movies
    first_movie_actors = our_db.get(clean_list[0])
    second_movie_actors = our_db.get(clean_list[1])
    if clean_list[-1] == '&':
        # we need the actors that performed in both movies
        res = intersection(first_movie_actors, second_movie_actors)
        res = print_queries_helper(res)
        if len(res) == 0:
            print("There are no actors in this group")
            return
        else:
            print(res)
            return
    if clean_list[-1] == '|':
        # we need the actors that performed in one or more of the movies
        res = union(first_movie_actors, second_movie_actors)
        res = print_queries_helper(res)
        if len(res) == 0:
            print("There are no actors in this group")
            return
        else:
            print(res)
            return
    if clean_list[-1] == '^':
        res = symmetric_difference(first_movie_actors, second_movie_actors)
        res = print_queries_helper(res)
        if len(res) == 0:
            print("There are no actors in this group")
            return
        else:
            print(res)
            return


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: checks_actor - helper function *

* The Input: A data-base (dictionary)	*

* The output: True or False *

* The Function operation: Iterates of the dictionary values and check if the actor appears in the actors list *

* If the actors is found returns True, else returns False *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def check_actor(actor_query, our_db):
    if actor_query in [x for v in our_db.values() for x in v]:
        return True
    else:
        return False


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: query_by_actor *

* The Input: A data-base (dictionary)	*

* The output: The result of the user query *

* The Function operation: Checks if the actress is indeed in the data-base, if found, *

* For each movie (key) she appeared on, it adds it to a set, and return the union of this set *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def query_by_actor(our_db):
    actor_query = input("Please select an actor:\n")
    # cleaning strings from extra trailing spaces
    actor_query = actor_query.strip()
    actor_query = actor_query.rstrip()
    actor_query = actor_query.lstrip()
    bool = check_actor(actor_query, our_db)
    if bool == False:
        print("Error")
        return
    all = set()
    for key in our_db:
        lst = our_db[key]
        if actor_query in lst:
            all = all.union(set(lst))
    all.remove(actor_query)
    res = sorted(all)
    makeitastring = ', '.join(res)
    print(makeitastring)
    return


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: insert_a_new_movie *

* The Input: A movies and actresses to add to our data-base*

* The output: None *

* The Function operation: Checks if the movie is in the data-base, if found, *

* We add the actresses to our data base, if not, we create it in our data-base*

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def insert_a_new_movie(our_db):
    update_db = input("Please insert a new movie:\n")
    update_db = update_db.split(",")
    my_update_list = update_db
    if len(my_update_list) < 2:
        print("Error")
        return
    # clean data
    my_update_list = clean(my_update_list)
    actors_to_add = my_update_list[1:]
    if my_update_list[0] in our_db.keys():  # the movie is in the db
        our_db[my_update_list[0]] = union(actors_to_add, our_db[my_update_list[0]])
    else:
        our_db[my_update_list[0]] = my_update_list[1:]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: save_to_file *

* The Input: A data-base and an output txt file *

* The output: None *

* The Function operation: Creates a new dictionary where the key is the actress and the values are *

* the list of the movies she apperead in (unsorted). Then, when print it sorted to the file, one by one *

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def save_to_file(our_db, output_file):
    os.chmod(output_file, 0o777)
    output_file = open(output_file, 'w')
    all = set()
    for key in our_db:
        lst = our_db[key]
        all = all.union(set(lst))
    # actors are sorted beforehand
    sorted_actors = sorted(all)
    list_actors = list(sorted_actors)
    new_db = {}
    for actor in list_actors:
        for movie, list_actors in our_db.items():
            if actor in list_actors:
                if actor not in new_db:
                    new_db[actor] = [movie]
                else:
                    new_db[actor].append(movie)

    for actor, movies in new_db.items():
        output_file.write(actor)
        output_file.write(', ')
        # helper will sort the movies and converts is to a string
        output_file.write(print_queries_helper(new_db[actor]))
        output_file.write('\n')
    output_file.close()
    return


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Function name: enry_menu *

* The Input: A movies input txt file an output txt file, given as arguments from the command-line*

* The output: None *

* The Function operation: Gets from the user an option and calls the relevant function *

* If 4 is chosen we save the output file and exit, if 5 is chosen we stop the program*

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def entry_menu(movies_file, output_file):
    print("Processing...")
    our_db = create_db(movies_file)
    flag = True
    while flag:
        user_choice = int(input("Please select an option:\n "
                                "1) Query by movies\n "
                                "2) Query by actor\n "
                                "3) Insert a new movie\n "
                                "4) Save and Exit\n 5) Exit\n"))
        if user_choice == 1:
            query_by_movie(our_db)
        elif user_choice == 2:
            query_by_actor(our_db)
        elif user_choice == 3:
            insert_a_new_movie(our_db)
        elif user_choice == 4:
            save_to_file(our_db, output_file)
            flag = False
        elif user_choice == 5:
            flag = False


if __name__ == '__main__':
    entry_menu(sys.argv[1], sys.argv[2])

