# better_doctor

Complete coding assignment for Better Doctor interview.

## Instructions

Here at BetterDoctor we spend the majority of out time processing health care provider data through our data pipeline. The first step in this process is matching a doctor into our system. This coding exercise is intended to give you an opportunity to write some code that will address this problem.

The file attached file (data_files.tgz) includes 2 files:

* `source_data.json`: JSON file that has clean normalized data used as the source for the matching.
* `match_file.csv`: Raw source data that needs to be parsed and normalized.

#### Requirements
* Process the data in match_file.csv against the data in source_data.json
* Try to match based on the following fields: NPI, Name (Use first and last), Address (using street, street_2, city, state and zip)

Send us a GitHub link with your completed work. Good luck and remember to show us your best software engineering practices!


## Notes
### Assumptions

From the instructions, a doctor should have a unique NPI, and a unique [First, Last] name. I'll assume a practice should have a unique Address (using street, street_2, city, state and zip),

We see from the json model that one doctor can have multiple practices. From choice of construction of the validated data model, I will assume that one practice cannot have multiple doctors. *This last assumption requires clarification.*

### Technology choices
I chose to use pandas dataframes to make the data import and manipulation easy, and to work like a database.

In a relational database, I would index the frequently searched columns (or column sets) to improve query time. This equates to a O(1) hash search instead of an O(n) linear search.

This could be done on the python side as well, by assigning a hash to each, say, [First Name, Last Name] pair, but that would add processing time on reading in the data, and query performance doesn't seem to be an issue here yet, so it seems like an over-optimization for now.

### What are we looking for?
Given:

* A validated data set
* A new data set to be matched to our existing data set.

I interpret the problem as

1. We want to see which of the new rows match validated rows (these are true doctors)
1. Which might be new practices of existing doctors
1. Which might be mis-recorded practices of existing doctors:
    1. Mismatched NPI / name
    1. Mismatched Address / name
4. Which might be new doctors?

The possibly new entries will need to be further evaluated to determine if they should be added to the validated data set, or if they are erroneous entries from the new data set, and can be thrown out (or added to some "known invalid data" set).
