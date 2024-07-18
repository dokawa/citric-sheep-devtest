# Dev Test Solution

## Design Considerations

#### Simplicity is prioritized

Considering that it is a test and not meant for production, there are some hardcoded paths and no env configs or database password to make the setup of the code as simple as possible

#### Avoiding premature optimization

From the task README, "an elevator" is mentioned, there is no support for more than one elevator. In a real case scenario it would need clarification if there is a chance of needing more. If that is the case, we could just create the elevator model and write a migration to assign current data to it

#### Fit for purpose solution

For data for one elevator, SQLite would be enough, even considering 4 events/min on average for 24 hours:

4 * 24 * 60 = 5760 events/day

Let's say each entry is 200 bytes per entry

5760 * 200 ~= 1MB/day

365 * 1MB = 365MB/year

That is about 3.7GB in ten years, which SQLite is more than enough to handle


#### Data model

**timestamp**: to be used for sorting and deriving rush hours, weekday cycles, holidays, etc

**floor**: to be used to calculate travel distances

**target_floor**: mandatory for the moving event type, should be empty for other event types

**operation_mode**:

- REGULAR
- OUT_OF_ORDER: so that can be filtered out and explain unusual inactivity or maintenance test movements
- SPECIAL: for [special modes](https://elevation.fandom.com/wiki/List_of_elevator_special_modes) which  can also be filtered out. Does not include maintenance

**number_of_passengers**: assuming we have a way to count passengers for each trip, we could use it to prioritize by number of passengers. Should be 0 for resting event. It is not being validated on endpoint but resting events with number_of_passengers should be treated on the processing phase

**type**:

- DEMAND: logged when a user presses a button
- MOVING: logged at the start of any movement and requires target_floor field
- RESTING: logged as soon as the elevator is empty and there are no pending demands

**temperature**: maybe on nice temperatures people on first floors are more likely to use the stairs. Can be null because we don't want to drop the record if the temperature sensor is not working and with timestamp we can fetch climate data for the day in the location as fallback

## Setup

**Prerequisites**
- Python (tested with Python 3.11.6)
- pip (tested with 23.2.1)

#### Running the application

Install dependencies with:

```
pip3 install -r requirements.txt
```

Run the server:

```
python3 main.py
```

#### Running tests

```
py.test tests/
```
