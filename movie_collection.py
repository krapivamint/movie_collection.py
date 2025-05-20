from typing import Dict, List, Iterator, Optional

class Movie:
    def __init__(self, title: str, year: int, genre: str, director: str, rating: float = 0.0):
        self.title = title
        self.year = year
        self.genre = genre
        self.director = director
        self.rating = rating

    def __str__(self) -> str:
        return f"{self.title} ({self.year}) | {self.genre} | Реж. {self.director} | Рейтинг: {self.rating}"

class MovieCollectionIterator(Iterator):
    def __init__(self, movies: List[Movie]):
        self._movies = movies
        self._index = 0

    def __next__(self) -> Movie: 
        if self._index < len(self._movies):
            movie = self._movies[self._index]
            self._index += 1
            return movie
        raise StopIteration

class MovieCollection:
    def __init__(self):
        self._movies: Dict[str, Movie] = {}
        self._collections: Dict[str, List[str]] = {} 

    def add_movie(self, movie: Movie) -> bool:
        if movie.title in self._movies:
            return False
        self._movies[movie.title] = movie
        return True

    def remove_movie(self, title: str) -> bool:
        movie = self._movies.pop(title, None)
        if not movie:
            return False

        for collection in self._collections.values():
            if title in collection:
                collection.remove(title)
        return True

    def create_collection(self, name: str) -> None:
        self._collections.setdefault(name, [])

    def add_to_collection(self, title: str, collection_name: str) -> bool:
        if title not in self._movies or collection_name not in self._collections:
            return False
        if title not in self._collections[collection_name]:
            self._collections[collection_name].append(title)
            return True
        return False

    def remove_from_collection(self, title: str, collection_name: str) -> bool:
        if title not in self._movies or collection_name not in self._collections:
            return False
        if title in self._collections[collection_name]:
            self._collections[collection_name].remove(title)
            return True
        return False

    def search(self, **kwargs) -> List[Movie]:
        return [movie for movie in self._movies.values()
                if all(getattr(movie, key) == value for key, value in kwargs.items())]

    def __iter__(self) -> MovieCollectionIterator: 
        return MovieCollectionIterator(list(self._movies.values()))

    @property
    def collections(self) -> Dict[str, List[str]]: 
        return self._collections


if __name__ == "__main__":
 
    collection = MovieCollection()

    collection.add_movie(Movie("Начало", 2010, "фантастика", "Кристофер Нолан", 8.8))
    collection.add_movie(Movie("Побег из Шоушенка", 1994, "драма", "Фрэнк Дарабонт", 9.3))

    collection.create_collection("Лучшие фильмы")
    collection.add_to_collection("Начало", "Лучшие фильмы")

    results = collection.search(year=2010, genre="фантастика")
    print("Результаты поиска:")
    for movie in results:
        print(movie)


    print("\nВсе фильмы в коллекции:")
    for movie in collection:
        print(movie)
