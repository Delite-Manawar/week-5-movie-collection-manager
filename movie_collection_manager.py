"""
===============================================================================
Program:     Movie Collection Manager
Author:      Delite  (Student ID: L30187745)
Course:      CPSC 50100 - Programming Fundamentals
Assignment:  Week 5 Programming Assignment - Lists and Dictionaries
Date:        November 22, 2026
Tier:        ADVANCED (Base + Intermediate + Advanced levels completed)

Description:
    Stores, displays and analyzes a personal library of films. Each movie is
    a dictionary (title, year, genres list, rating) and the whole collection
    is a list of those dictionaries. The program adds movies, sorts, slices,
    filters by genre, updates ratings, computes per-genre statistics, groups
    movies into a nested genre catalog, builds a title->rating lookup with a
    dictionary comprehension, finds each genre's champion, and saves the
    collection to movies.csv so it persists between sessions.
===============================================================================

TEST RESULTS (actual output recorded from running this program)
-------------------------------------------------------------------------------
Two sessions were run. Session 1 started with NO movies.csv; session 2
loaded the file saved by session 1. Function-level checks (marked *) were
run by importing the functions on the 7-movie list from session 1.

BASE LEVEL
1. Display pre-loaded collection -> PASS (five movies, genres joined, aligned)
     Your Movie Collection
     ----------------------------------------------------------------------
     Inception                    2010   Sci-Fi / Thriller            8.8
     The Shawshank Redemption     1994   Drama                        9.3
     The Godfather                1972   Crime / Drama                9.2
     Parasite                     2019   Thriller / Drama / Comedy    8.5
     The Dark Knight              2008   Action / Crime / Drama       9.0
2. Add "Rush Hour" with genres typed as "Action, Comedy" -> PASS
     stored genres list: ['Action', 'Comedy']  (two separate strings)
3. Sort and display by year -> PASS (oldest first)
     The Godfather 1972, The Shawshank Redemption 1994, Rush Hour 1998,
     The Dark Knight 2008, Inception 2010, Mad Max: Fury Road 2015,
     Parasite 2019
4. find_top_rated(movies, 3) on 7 movies -> PASS (3 returned, highest first)
     The Shawshank Redemption 9.3 / The Godfather 9.2 / The Dark Knight 9.0
     * original list order unchanged afterwards: True
5. get_average_rating() on 7 movies -> PASS
     Collection average rating: 8.56
     by hand: (9.2+9.3+7.0+9.0+8.8+8.1+8.5) / 7 = 59.9 / 7 = 8.557 -> 8.56
     * get_average_rating([]) returned 0.0

INTERMEDIATE LEVEL
6. Filter by "drama" (lowercase) -> PASS (4 movies returned)
     The Godfather, The Shawshank Redemption, The Dark Knight, Parasite
7. Filter by "western" -> PASS
     No movies match the genre 'western'.
8. Update rating of "rush hour" to 7.5 -> PASS
     Rating for 'rush hour' updated to 7.5.
     Rush Hour shows 7.5 in every later display and in movies.csv
9. Update rating of "Avatar" (not in collection) -> PASS
     update_rating() returned False ->
     No movie titled 'Avatar' was found.
10. get_genre_stats() on 7 movies with overlapping genres -> PASS
     Genre            Avg Rating   Count
     ------------------------------------
     Crime            9.10         2      (9.2+9.0)/2
     Drama            9.00         4      (9.2+9.3+9.0+8.5)/4
     Thriller         8.65         2
     Sci-Fi           8.45         2
     Action           8.20         3      (9.0+8.1+7.5)/3
     Adventure        8.10         1
     Comedy           8.00         2
11. sort_movies(movies, "rating", reverse=True) -> PASS (9.3 down to 7.5)
     * sort_movies(movies, "year", reverse=True) -> 2019 ... 1972
     * original list order unchanged afterwards: True
     * unknown key "length" returned the list unchanged: True

ADVANCED LEVEL
12. build_genre_catalog() on 7 movies -> PASS
     Action has 3 movies (The Dark Knight, Mad Max, Rush Hour); Crime,
     Drama, Sci-Fi, Thriller have 1 each; each movie appears once, under
     its first genre only
13. display_genre_catalog() -> PASS (each section sorted by rating, high first)
     Action (3)
         The Dark Knight               9.0
         Mad Max: Fury Road            8.1
         Rush Hour                     7.5
14. get_rating_lookup() -> PASS (7 entries for 7 movies)
     'Inception' is rated 8.8.
     'Titanic' is not in the rating lookup (...)      [session 2]
15. find_genre_champions(), Action has 3 movies -> PASS
     ===== Genre Champions =====
     Crime       → The Godfather (9.2)
     Drama       → The Shawshank Redemption (9.3)
     Action      → The Dark Knight (9.0)
     Sci-Fi      → Inception (8.8)
     Thriller    → Parasite (8.5)
16. First run with no CSV file -> PASS
     FileNotFoundError caught, starter list used, no traceback;
     "Saved 7 movies to movies.csv. Goodbye!"
17. Second run after saving -> PASS
     All 7 movies from session 1 loaded (Rush Hour at 7.5); genres rebuilt
     from "Action|Comedy" etc. Genres typed as "animation ,  comedy" were
     stored as ['Animation', 'Comedy']. "Saved 9 movies to movies.csv."
===============================================================================
"""

import csv

CSV_FILENAME = "movies.csv"
VALID_SORT_KEYS = ["title", "year", "rating"]


# -----------------------------------------------------------------------------
# Starter data
# -----------------------------------------------------------------------------

# Returns a fresh copy of the five pre-loaded movies. A function is used so
# that every call builds brand-new dictionaries and nothing is shared by
# accident between the starter data and the working collection.
def get_starter_movies():
    return [
        {"title": "Inception", "year": 2010,
         "genres": ["Sci-Fi", "Thriller"], "rating": 8.8},
        {"title": "The Shawshank Redemption", "year": 1994,
         "genres": ["Drama"], "rating": 9.3},
        {"title": "The Godfather", "year": 1972,
         "genres": ["Crime", "Drama"], "rating": 9.2},
        {"title": "Parasite", "year": 2019,
         "genres": ["Thriller", "Drama", "Comedy"], "rating": 8.5},
        {"title": "The Dark Knight", "year": 2008,
         "genres": ["Action", "Crime", "Drama"], "rating": 9.0},
    ]


# =============================================================================
# BASE LEVEL
# =============================================================================

# Function 1: builds and returns a new movie dictionary from the four values.
# It does not print anything and does not add the movie to any list.
def create_movie(title, year, genres, rating):
    movie = {
        "title": title,
        "year": year,
        "genres": genres,
        "rating": rating,
    }
    return movie


# Function 2: prints a heading, a separator line, and one aligned row per
# movie (title, year, genres joined with " / ", rating).
def display_movies(movies, heading):
    print()
    print(heading)
    print("-" * 70)

    if len(movies) == 0:
        print("No movies in this collection.")
        return

    for movie in movies:
        title = movie["title"]
        if len(title) > 28:                      # keep long titles in their column
            title = title[:27] + "."
        genres_text = " / ".join(movie["genres"])
        print(f"{title:<29}{movie['year']:<7}{genres_text:<28}{movie['rating']:>4.1f}")


# Function 3: returns a NEW list holding the top n movies by rating.
# sorted() leaves the original list untouched; slicing keeps the first n.
def find_top_rated(movies, n):
    sorted_by_rating = sorted(movies, key=lambda movie: movie["rating"], reverse=True)
    return sorted_by_rating[:n]


# Function 4: returns the average rating rounded to 2 decimal places, using a
# for loop and an accumulator (no sum()). Returns 0.0 for an empty list.
def get_average_rating(movies):
    if len(movies) == 0:
        return 0.0

    total = 0.0
    for movie in movies:
        total += movie["rating"]
    return round(total / len(movies), 2)


# =============================================================================
# INTERMEDIATE LEVEL
# =============================================================================

# Function 5: returns a NEW list of movies whose genres list contains the
# given genre. The comparison is case-insensitive on both sides.
def filter_by_genre(movies, genre):
    target = genre.strip().lower()
    matches = []
    for movie in movies:
        for movie_genre in movie["genres"]:          # search the nested list
            if movie_genre.lower() == target:
                matches.append(movie)
                break                                 # stop once this movie matches
    return matches


# Function 6: finds a movie by title (case-insensitive) and changes its rating
# directly inside the existing dictionary. Returns True if found, else False.
# Prints nothing - the caller reports the result.
def update_rating(movies, title, new_rating):
    target = title.strip().lower()
    for movie in movies:
        if movie["title"].lower() == target:
            movie["rating"] = new_rating
            return True
    return False


# Helper: builds a list of every distinct genre in the collection, using a
# membership check (not a set). Shared by step 7 and get_genre_stats() so the
# logic is written once.
def get_unique_genres(movies):
    unique_genres = []
    for movie in movies:
        for genre in movie["genres"]:
            if genre not in unique_genres:
                unique_genres.append(genre)
    return unique_genres


# Function 7: returns a list of (genre, average_rating, count) tuples, one per
# unique genre, sorted by average rating from highest to lowest.
def get_genre_stats(movies):
    stats = []
    for genre in get_unique_genres(movies):
        ratings = []
        for movie in movies:
            if genre in movie["genres"]:
                ratings.append(movie["rating"])

        total = 0.0
        for rating in ratings:
            total += rating
        average = round(total / len(ratings), 2)

        stats.append((genre, average, len(ratings)))

    stats.sort(key=lambda stat: stat[1], reverse=True)
    return stats


# Function 8: returns a NEW list sorted by "title", "year" or "rating".
# reverse=True gives descending order. An unknown key returns the list
# unchanged. The original list is never sorted in place.
def sort_movies(movies, sort_key, reverse=False):
    if sort_key not in VALID_SORT_KEYS:
        return movies

    if sort_key == "title":
        return sorted(movies, key=lambda movie: movie["title"].lower(), reverse=reverse)
    return sorted(movies, key=lambda movie: movie[sort_key], reverse=reverse)


# =============================================================================
# ADVANCED LEVEL
# =============================================================================

# Feature 1a: groups the movies into a nested dictionary keyed by primary
# genre (the first item in each genres list). Each value is a list of movie
# dictionaries. Built with an explicit loop and if/else.
def build_genre_catalog(movies):
    catalog = {}
    for movie in movies:
        primary_genre = movie["genres"][0]
        if primary_genre in catalog:
            catalog[primary_genre].append(movie)
        else:
            catalog[primary_genre] = [movie]
    return catalog


# Feature 1b: prints each genre as a section heading, then its movies
# (highest rated first) indented underneath.
def display_genre_catalog(catalog):
    print()
    print("===== Genre Catalog (by primary genre) =====")
    for genre, genre_movies in catalog.items():
        print(f"{genre} ({len(genre_movies)})")
        ranked = sorted(genre_movies, key=lambda movie: movie["rating"], reverse=True)
        for movie in ranked:
            print(f"    {movie['title']:<30}{movie['rating']:.1f}")
    print("=" * 44)


# Function 9: one-line dictionary comprehension mapping title -> rating,
# used for fast lookups without scanning the whole list.
def get_rating_lookup(movies):
    return {movie["title"]: movie["rating"] for movie in movies}


# Function 10: returns { genre: title_of_highest_rated_movie } by walking the
# nested catalog with .items() and comparing ratings manually (no max()).
def find_genre_champions(catalog):
    champions = {}
    for genre, genre_movies in catalog.items():
        best_movie = genre_movies[0]
        for movie in genre_movies:
            if movie["rating"] > best_movie["rating"]:
                best_movie = movie
        champions[genre] = best_movie["title"]
    return champions


# Feature 2a: loads the collection from a CSV file. Genres are stored in the
# file as a "|"-separated string and turned back into a list here. If the
# file does not exist yet, the five starter movies are returned instead.
def load_from_csv(filename):
    try:
        movies = []
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)                              # skip the header row
            for row in reader:
                if len(row) < 4:                      # ignore blank/broken lines
                    continue
                title, year, genres_text, rating = row[0], row[1], row[2], row[3]
                genres = genres_text.split("|")
                movies.append(create_movie(title, int(year), genres, float(rating)))
        return movies
    except FileNotFoundError:
        return get_starter_movies()


# Feature 2b: writes the header and one row per movie to the CSV file.
# The genres list is joined with "|" only here, at the file boundary.
def save_to_csv(movies, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "year", "genres", "rating"])
        for movie in movies:
            genres_text = "|".join(movie["genres"])
            writer.writerow([movie["title"], movie["year"], genres_text, movie["rating"]])


# =============================================================================
# INPUT HELPERS (keep asking until the user types a valid value)
# =============================================================================

# Asks for a whole number; repeats on invalid input.
def ask_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("  Please enter a whole number (e.g. 2010).")


# Asks for a decimal number between low and high; repeats on invalid input.
def ask_float(prompt, low=0.0, high=10.0):
    while True:
        try:
            value = float(input(prompt).strip())
            if low <= value <= high:
                return value
            print(f"  Please enter a number from {low} to {high}.")
        except ValueError:
            print("  Please enter a number (e.g. 8.5).")


# Asks for genres separated by commas and returns a clean list of strings.
# .strip() removes the spaces around each genre and .title() gives them
# consistent capitals, so "comedy" and "Comedy" count as the same genre.
def ask_genres(prompt):
    while True:
        raw_text = input(prompt)
        genres = [genre.strip().title() for genre in raw_text.split(",") if genre.strip() != ""]
        if len(genres) > 0:
            return genres
        print("  Please enter at least one genre.")


# Prompts for one movie's details and returns the new movie dictionary.
def ask_for_movie(number):
    print(f"\nEnter details for new movie #{number}:")
    title = input("  Title: ").strip()
    year = ask_int("  Year: ")
    genres = ask_genres("  Genres (separate with commas): ")
    rating = ask_float("  Rating (0-10): ")
    return create_movie(title, year, genres, rating)


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    # 1. Load the collection (starter list on the first run, CSV afterwards)
    movies = load_from_csv(CSV_FILENAME)

    # 2. Show the collection as loaded
    display_movies(movies, "Your Movie Collection")

    # 3. Add two new movies from user input
    for number in range(1, 3):
        new_movie = ask_for_movie(number)
        movies.append(new_movie)

    # 4. Sort in place by year (oldest first) and display
    movies.sort(key=lambda movie: movie["year"])
    display_movies(movies, "All Movies Sorted by Year")

    # 5. Top 3 rated movies
    top_three = find_top_rated(movies, 3)
    display_movies(top_three, "Top 3 Rated Movies")

    # 6. Average rating
    print(f"\nCollection average rating: {get_average_rating(movies):.2f}")

    # ----- Intermediate -----

    # 7. All unique genres, sorted alphabetically
    unique_genres = get_unique_genres(movies)
    unique_genres.sort()
    print("\nGenres in your collection:", ", ".join(unique_genres))

    # 8. Filter by a genre chosen by the user
    genre_choice = input("\nEnter a genre to filter by: ").strip()
    genre_matches = filter_by_genre(movies, genre_choice)
    if len(genre_matches) == 0:
        print(f"No movies match the genre '{genre_choice}'.")
    else:
        display_movies(genre_matches, f"Movies in genre: {genre_choice}")

    # 9. Optionally update a rating
    answer = input("\nDo you want to update a rating? (y/n): ").strip().lower()
    if answer in ["y", "yes"]:
        title_choice = input("  Movie title: ").strip()
        new_rating = ask_float("  New rating (0-10): ")
        if update_rating(movies, title_choice, new_rating):
            print(f"Rating for '{title_choice}' updated to {new_rating:.1f}.")
            display_movies(movies, "Updated Movie Collection")
        else:
            print(f"No movie titled '{title_choice}' was found.")

    # 10. Genre statistics table
    print()
    print("===== Genre Statistics =====")
    print(f"{'Genre':<17}{'Avg Rating':<13}{'Count'}")
    print("-" * 36)
    for genre, average, count in get_genre_stats(movies):
        print(f"{genre:<17}{average:<13.2f}{count}")

    # 11. Sort by the user's choice of key and direction
    sort_key = input("\nSort by (title / year / rating): ").strip().lower()
    while sort_key not in VALID_SORT_KEYS:
        sort_key = input("  Please type title, year or rating: ").strip().lower()
    direction = input("Ascending or descending? (a/d): ").strip().lower()
    descending = direction in ["d", "desc", "descending"]
    order_word = "Descending" if descending else "Ascending"
    sorted_view = sort_movies(movies, sort_key, reverse=descending)
    display_movies(sorted_view, f"Movies Sorted by {sort_key.title()} ({order_word})")

    # ----- Advanced -----

    # Genre catalog (nested dictionary)
    catalog = build_genre_catalog(movies)
    display_genre_catalog(catalog)

    # Rating lookup (dictionary comprehension) + membership check with "in"
    rating_lookup = get_rating_lookup(movies)
    lookup_title = input("\nEnter a movie title to look up its rating: ").strip()
    if lookup_title in rating_lookup:
        print(f"'{lookup_title}' is rated {rating_lookup[lookup_title]:.1f}.")
    else:
        print(f"'{lookup_title}' is not in the rating lookup "
              f"(titles must match exactly, including capitals).")

    # Genre champions
    champions = find_genre_champions(catalog)
    print()
    print("===== Genre Champions =====")
    for genre, champion_title in champions.items():
        print(f"{genre:<12}→ {champion_title} ({rating_lookup[champion_title]:.1f})")
    print("=" * 27)

    # Save once, at the very end
    save_to_csv(movies, CSV_FILENAME)
    print(f"\nSaved {len(movies)} movies to {CSV_FILENAME}. Goodbye!")


if __name__ == "__main__":
    main()
