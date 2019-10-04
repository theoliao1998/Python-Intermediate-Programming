import unittest
import proj1_f19 as proj1

class TestClasses(unittest.TestCase):
    
    def testConstructor(self):
        media = proj1.Media("1999", "Prince", "2000")
        self.assertIsInstance(media,proj1.Media)
        self.assertEqual(media.title, "1999")
        self.assertEqual(media.author, "Prince")
        self.assertEqual(media.release_year, "2000")
        
        song = proj1.Song("Hey Jude", "The Beatles", "1968", "The Beatles 1967-1970 (The Blue Album)", "Rock",431333)
        self.assertIsInstance(song,proj1.Song)
        self.assertEqual(song.title, "Hey Jude")
        self.assertEqual(song.author, "The Beatles")
        self.assertEqual(song.release_year, "1968")
        self.assertEqual(song.album, "The Beatles 1967-1970 (The Blue Album)")
        self.assertEqual(song.genre, "Rock")
        self.assertEqual(song.track_length, 431333)
        
        movie = proj1.Movie("Jaws", "Steven Spielberg", "1975", "PG", 7451455)
        self.assertIsInstance(movie,proj1.Movie)
        self.assertEqual(movie.title, "Jaws")
        self.assertEqual(movie.author, "Steven Spielberg")
        self.assertEqual(movie.release_year, "1975")
        self.assertEqual(movie.rating, "PG")
        self.assertEqual(movie.movie_length, 7451455)
    
    def testStrLen(self):
        media = proj1.Media("1999", "Prince", "2000")
        self.assertEqual(media.__str__(),"1999 by Prince (2000)")
        self.assertEqual(media.__len__(),0)
        
        song = proj1.Song("Hey Jude", "The Beatles", "1968", "The Beatles 1967-1970 (The Blue Album)", "Rock",431333)
        self.assertEqual(song.__str__(),"Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(song.__len__(),431.333)
        
        movie = proj1.Movie("Jaws", "Steven Spielberg", "1975", "PG", 7451455)
        self.assertEqual(movie.__str__(),"Jaws by Steven Spielberg (1975) [PG]")
        self.assertEqual(movie.__len__(),124)
    
    def testInstanceVariables(self):
        media = proj1.Media("1999", "Prince", "2000")
        with self.assertRaises(AttributeError):
            media.album
        with self.assertRaises(AttributeError):
            media.genre
        with self.assertRaises(AttributeError):
            media.track_length
        with self.assertRaises(AttributeError):
            media.rating
        with self.assertRaises(AttributeError):
            media.movie_length
        
        song = proj1.Song("Hey Jude", "The Beatles", "1968", "The Beatles 1967-1970 (The Blue Album)", "Rock",431333)
        with self.assertRaises(AttributeError):
            song.rating
        with self.assertRaises(AttributeError):
            song.movie_length
        
        movie = proj1.Movie("Jaws", "Steven Spielberg", "1975", "PG", 7451455)
        with self.assertRaises(AttributeError):
            movie.album
        with self.assertRaises(AttributeError):
            movie.genre
        with self.assertRaises(AttributeError):
            movie.track_length


import json

filename = "sample_json.json"

with open(filename, 'r') as f:
    data = f.read()

data = json.loads(data)

class TestJson(unittest.TestCase):
    def testConstructor(self):
        media = proj1.Media(json=data[0])
        self.assertIsInstance(media,proj1.Media)
        self.assertEqual(media.title, "Jaws")
        self.assertEqual(media.author, "Steven Spielberg")
        self.assertEqual(media.release_year, "1975")
        
        song = proj1.Song(json=data[1])
        self.assertIsInstance(song,proj1.Song)
        self.assertEqual(song.title, "Hey Jude")
        self.assertEqual(song.author, "The Beatles")
        self.assertEqual(song.release_year, "1968")
        self.assertEqual(song.album, "The Beatles 1967-1970 (The Blue Album)")
        self.assertEqual(song.genre, "Rock")
        self.assertEqual(song.track_length, 431333)
        
        movie = proj1.Movie(json=data[0])
        self.assertIsInstance(movie,proj1.Movie)
        self.assertEqual(movie.title, "Jaws")
        self.assertEqual(movie.author, "Steven Spielberg")
        self.assertEqual(movie.release_year, "1975")
        self.assertEqual(movie.rating, "PG")
        self.assertEqual(movie.movie_length, 7451455)
    
    def testStrLen(self):
        media = proj1.Media(json=data[0])
        self.assertEqual(media.__str__(),"Jaws by Steven Spielberg (1975)")
        self.assertEqual(media.__len__(),0)
        
        song = proj1.Song(json=data[1])
        self.assertEqual(song.__str__(),"Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(song.__len__(),431.333)
        
        movie = proj1.Movie(json=data[0])
        self.assertEqual(movie.__str__(),"Jaws by Steven Spielberg (1975) [PG]")
        self.assertEqual(movie.__len__(),124)
    
    def testInstanceVariables(self):
        media = proj1.Media(json=data[0])
        with self.assertRaises(AttributeError):
            media.album
        with self.assertRaises(AttributeError):
            media.genre
        with self.assertRaises(AttributeError):
            media.track_length
        with self.assertRaises(AttributeError):
            media.rating
        with self.assertRaises(AttributeError):
            media.movie_length
        
        song = proj1.Song(json=data[1])
        with self.assertRaises(AttributeError):
            song.rating
        with self.assertRaises(AttributeError):
            song.movie_length
        
        movie = proj1.Movie(json=data[0])
        with self.assertRaises(AttributeError):
            movie.album
        with self.assertRaises(AttributeError):
            movie.genre
        with self.assertRaises(AttributeError):
            movie.track_length

class TestFetch(unittest.TestCase):
    def testFetch(self):
        params1 = {"term":"baby love","limit":10}
        params2 = {"term":"moana helter skelter","limit":15}
        params3 = {"term":"&@#!$","limit":10}
        params4 = {"term":"","limit":20}
        res1 = proj1.fetchData(params1)
        res2 = proj1.fetchData(params2)
        res3 = proj1.fetchData(params3)
        res4 = proj1.fetchData(params4)
        
        self.assertTrue(res1[0]["resultCount"]<=10 and res1[0]["resultCount"]>=0)
        self.assertTrue(res2[0]["resultCount"]<=15 and res1[0]["resultCount"]>=0)
        self.assertTrue(res3[0]["resultCount"]<=10 and res1[0]["resultCount"]>=0)
        self.assertTrue(res4[0]["resultCount"]<=20 and res1[0]["resultCount"]>=0)

        


unittest.main()
