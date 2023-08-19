# Degrees of Separation

Determine how many "degrees of separation" exist between two people.

<img width="600" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/517f83e5-2f7b-4bbe-a443-9d528d30d56f">

## Outline

- Load csv data into memory
- Prompt user for two names
- Retrieve person ids (prompt user to clarify if multiple ids for one name)
- Use depth-first search and backtracking to obtain smallest path

## Usage
python degrees.py small

(a "large" directory was also used comprising the entirety of IMDb's database where:  
movies.csv had 344,277 rows  
people.csv had 1,044,500 rows  
stars.csv had 1,189,595 rows  
Unfortunately its 56 MBs exceed github's limit)
