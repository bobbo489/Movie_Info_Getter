'''
Created on Nov 6, 2018

@author: robedrye
'''

class Movie(object):
    '''
    classdocs
    '''


    def __init__(self,name, year, rating, release_date, runtime, genre, poster):
        '''
        Constructor
        '''
        self.name = name
        self.year = year
        self.rating = rating
        self.release_date = release_date
        self.runtime = runtime
        self.genre = genre
        self.poster = poster
        
    def get_name(self):
    
        return self.name
    
    def get_year(self):
        
        return self.year
    
    def get_rating(self):
        
        return self.rating
    
    def get_runtime(self):
        
        return self.runtime.strip(' min')
    
    def get_genre(self):
        
        return self.genre 
    
    def get_release_date(self):
        
        return self.release_date   
    
    def get_poster(self):
        
        return self.poster
        
    
def movie_creator(movie_data):
        
    movie_name = movie_data[1]
    movie_year = movie_data[3]
    movie_rating = movie_data[5]
    movie_release_date = movie_data[7]
    movie_runtime = movie_data[9]
    movie_genre = movie_data[11]
    movie_poster = movie_data[27]
        
    return Movie(movie_name, movie_year, movie_rating, movie_release_date, movie_runtime, movie_genre, movie_poster)
    
    
