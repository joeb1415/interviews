# 8/8 11am skype and coderpad

# []int{3, 2, 1, 0, 4}
# [3, 2, 3, 0, 4]


# Table "deliveries"
#  Column         | Type                     | Modifiers
# ----------------+--------------------------+-----------------------------------------
#  id             | integer                  | not null default
#  courier_id     | integer                  | not null
#  date_created   | integer                  | not null
#                 |                          | contains unix time timestamp
#  date_completed | integer                  | contains unix time timestamp
#  vehicle_type_id| integer                  | not null FK

# IX_deliveries_vehicle_type_id




#  vehicle_type   | character varying(10)    | not null
#                 |                          | - example values
#                 |                          |  ('bike', 'walk', 'car', 'truck')


# table 'vehicle_type'
# vehicle_type_id   | integer   | not null PK
# 1    | bike
# 2    | walk


# Find number of deliveries in the past 30 days where the courier was a biker or walker
sql = '''
select
count(*)
from deliveries

where
vehicle_type in ('bike', 'walk')
and date_completed is not null
and date_completed >= dateadd(day, -30, getdate())
'''


def list_jump(input_list):
    """returns true if we find a way to reach the end, or, if we appear to get stuck without being able to reach the end, then return false

    Check valid input:
    all integer
    >= 1 elements
    all non-negative
    int overflow
    """

    next_index = 0
    next_value = input_list[next_index]

    if next_value >= len(input_list):
        return True

    while next_value > 0:
        print('next_index: {}, next_value: {}'.format(next_index, next_value))
        next_index = check_range(input_list, next_index + 1, next_index + next_value)
        next_value = input_list[next_index]

        # if we can reach the end, true, else, iterate
        if next_index + next_value >= len(input_list):
            return True

    return False  # true or false


def check_range(input_list, start, end):
    """return postion that itself will reach us the furthest"""

    max_reach = 0
    best_index = 0
    for position in range(start, end + 1):
        print('checking position: {}'.format(position))
        reach = position + input_list[position]
        if reach > max_reach:
            max_reach = reach
            best_index = position

    return best_index


# print(list_jump([3,2,1,0,4]))
# print(list_jump([3,2,3,0,4]))
print(list_jump([2, 0, 0]))
