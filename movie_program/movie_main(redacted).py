'''
Created on Nov 6, 2018

@author: robedrye
'''
#import movie_class
import urllib3
import mysql.connector
import re
import string
from movie_class import movie_creator
import webbrowser


cnx = mysql.connector.connect(user='root', password='mysql8013',
                                  host='127.0.0.1', database='movie_database')

key = ''  #Personal Key =


def main():    
    
    movie_info = []

    print_intro()
    get_key()
    
    while True:
        selection = get_selection()
            
        if selection == 'q':
            search_type = get_search_type()
            
            if search_type == 't':
                while True:
                    movie = get_movie_request()

                    if len(movie) > 0:
                        break
                
                in_database = query_for_name(movie)
                
                if in_database == 'n':
                    content = retrieve_movie_info(movie)
                    real_movie = in_omdb(content)
                    
                    if not real_movie:
                        print()
                        print("The movie you have requested does not exist.  Please make a new selection.")
                        print()
                        continue
                    
                    movie_info = modify_returned_info(content)
                    movie_object = movie_creator(movie_info)
                    send_to_database(movie_object)
                    print_movie_info(movie_object)
                    print()
                    
            elif search_type == 'y':
                year = get_movie_year()
                query_for_year(year)
            
            elif search_type == 'g':
                genre = get_movie_genre()
                query_for_genre(genre)
                
        elif selection == 'l':
            list_movies()

        elif selection == 'e':
            end_program()
            break
        
    cnx.close()
        
    return
    
        
def get_movie_request():
    return input("Enter a movie title: ")


def get_movie_year():
    print()
    
    while True:
        try:
            year = int(input("Enter a year to search for: "))
            return year
        except ValueError:
            print("Invalid year, please try again!")
            print()
            

def get_movie_genre():
    print()
    return input("Enter a movie genre (i.e. Action, Comedy, Sci-Fi...: ")


def get_key():
    global key
    temp_key = str(input("Enter your API key from OMDb: "))
    
    if len(temp_key) > 0:
        key = temp_key
    
    return


def retrieve_movie_info(movie):
    http = urllib3.PoolManager()
    movie = movie.replace(" ", "-")
            
    return http.request('GET', 'http://www.omdbapi.com/?apikey='+key+'&t='+movie+'&type=movie&r=xml')


def print_intro():
    print("Welcome to the Movie Database.")
    print("This program will display what movies are currently in the database or ")
    print("information on a specific movie title.  If that movie is not currently ")
    print("in the local database it will query OMDB and add that information locally.")
    print()
    
    
def get_selection():
    while True:
        option = input("You can (l)ist or (q)uery the database for a movie, or (e)nd: ")
        if len(option) > 0:
            option = option[0].lower()
            if option == 'l' or option == 'e' or option == 'q':
                return option


def end_program():
    print("Thank you for using this program.  Any data you have asked for has been added ")
    print("to the database and will be available for future queries.")
    
    return


def list_movies():
    cursor = cnx.cursor()
    query = "SELECT * FROM movies"
    
    cursor.execute(query)
    
    movies = cursor.fetchall()
    print()
    
    for movie in movies:
        print(movie[0])        
     
    print()
    
    return
     

def modify_returned_info(content):
    movie_info = (str(content.data).strip("/root>'")).split('<')

    del movie_info[0]
    del movie_info[0]
    del movie_info[0]
            
    movie_info = movie_info[0].split('"')
    movie_name = movie_info[1]
    fixed_movie = re.sub('[^a-zA-Z0-9\n\.]', ' ', movie_name)
    fixed_movie = string.capwords(fixed_movie)
    
    movie_info.insert(1, fixed_movie)
    
    del movie_info[2]    

    return movie_info


def alter_movie_name(movie_name):
    fixed_movie = re.sub('[^a-zA-Z0-9\n\.]', ' ', movie_name)
    fixed_movie = string.capwords(fixed_movie)
    
    return fixed_movie


def send_to_database(movie_object):
    cursor = cnx.cursor()
    query = "INSERT INTO movies(movie_name, movie_year, rating, released, runtime, genre, poster) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    args = (movie_object.get_name(), movie_object.get_year(), movie_object.get_rating(), 
            movie_object.get_release_date(), movie_object.get_runtime(), movie_object.get_genre(), 
            movie_object.get_poster())
    
    cursor.execute(query, args)
    cnx.commit()
    
    return


def query_for_name(movie_name):
    name = alter_movie_name(movie_name)  
    cursor = cnx.cursor()
    name = string.capwords(name)
    query = "SELECT * FROM movies WHERE movie_name LIKE '%"+name+"%'"
    
    cursor.execute(query)
    
    movie = cursor.fetchall()
    
    if len(movie) > 0:
        for item in range(len(movie)):
            returned_movie = []
            
            for location in range(0,40): 
                if (location == 0 or location % 2 == 0 or location > (2* len(movie[item]))) and location != 27:
                    returned_movie.append('null')
                elif location == 27:
                    returned_movie.append(movie[item][6])
                    #del returned_movie[27]
                else:
                    temp_data = str(movie[item][int(location/2)])
                    returned_movie.append(temp_data)
            print(returned_movie)        
            movie_object = movie_creator(returned_movie)
            print_movie_info(movie_object)
         
        print()
                           
        return 'y'
    return 'n'


def query_for_year(year):
    cursor = cnx.cursor()
    year = str(year)
    query = "SELECT * FROM movies WHERE movie_year = '"+year+"'"
    
    cursor.execute(query)
    
    movie_list = cursor.fetchall()
    
    if len(movie_list) > 0:
        print("These movies came out in "+year+".")
        
        for item in range(len(movie_list)):
            print(str(movie_list[item][0]))
            
        print()
    
    else:
        print("No movies that came out in "+year+" are in the local database!")
        print()
    
    return


def query_for_genre(genre):
    cursor = cnx.cursor()
    query = "SELECT * FROM movies WHERE genre LIKE '%"+genre+"%'"
    
    cursor.execute(query)
    
    movie_list = cursor.fetchall()
    
    if len(movie_list) > 0:
        print("These movies fall into the "+genre+" genre.")
        
        for item in range(len(movie_list)):
            print(str(movie_list[item][0]))
            
        print()
    else:
        print("No movies that fall into the "+genre+" are in the local database!")
        print()
        
    return


def print_movie_info(movie_object):
    print()
    print(str(movie_object.get_name()), "was released", str(movie_object.get_release_date()) + ", was rated", 
            str(movie_object.get_rating()) + ", ran for", str(movie_object.get_runtime()) + 
            " mins, and was a", str(movie_object.get_genre()))
    
    if see_poster(movie_object):
        retrieve_poster(movie_object)
    
    return


def see_poster(movie_object):
    while True:
        
        while True:
            response = input("Would you like to see the movie poster for "+movie_object.get_name()+" (y/n): ")
            
            if len(response) > 0:
                break
        response = response[0].lower()
        
        if response == 'y':
            return True
        else:
            return False


def retrieve_poster(movie_object):
    webbrowser.open(movie_object.get_poster())
    
    return


def in_omdb(content):
    if 'Movie not found' in str(content.data):
        return False
    else:
        return True
    
    
def get_search_type():
    print()
    
    while True:
        while True:
            response = input("You can search for a (t)itle, (y)ear, or (g)enre: ")
            
            if len(response) > 0:
                break
            
        response = response[0].lower()
        
        if response == 't' or response == 'y' or response == 'g':
            return response


if __name__ == '__main__':
    main()