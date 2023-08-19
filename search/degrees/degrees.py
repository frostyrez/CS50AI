import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    print(f"Finding path between {source} and {target}")

    # initialise start
    start = Node(state=source,parent=None,action=None)
    current = Node(state=source,parent=None,action=None)
    frontier = StackFrontier()
    explored = StackFrontier()
    frontier.add(start)

    while True:
        if current.state == target:
            print("Found!")
            shortest = [[current.action,current.state]]
            # backtrack
            while not in_movie(shortest[-1][0],source):
                i = 0
                while explored.frontier[i].state != shortest[-1][1]:
                    i += 1
                shortest.append([explored.frontier[i].action,explored.frontier[i].parent])
            # correct movies?
            for j in range(len(shortest)-1):
                state = shortest[j][1]
                parent = shortest[j+1][1]
                for k in explored.frontier:
                    if k.state == state and k.parent == parent:
                        shortest[j][0] = k.action

            shortest = shortest[:-1]               
            return shortest[::-1]
        
        if frontier.empty():
            raise Exception("Empty frontier.")
        
        # grab all neighbors (persons) of current person
        neighbors = neighbors_for_person(current.state)

        # add them to frontier if person not already explored
        for neighbor in neighbors:            
            frontier.add(Node(action=neighbor[0],state=neighbor[1],parent=current.state))
        
        for exp in explored.frontier:
            i = 1
            while i < len(frontier.frontier):
                if frontier.frontier[i].state == exp.state or frontier.frontier[i].state == exp.parent:
                    frontier.frontier.pop(i)
                i += 1

        current = frontier.remove()
        explored.add(current)      
        


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for star_id in movies[movie_id]["stars"]:
            if star_id != person_id:
                neighbors.add((movie_id, star_id))
    return neighbors

def in_movie(movie_id,person_id):
    for star_id in movies[movie_id]["stars"]:
        if star_id == person_id:
            return True
    return False

if __name__ == "__main__":
    main()
