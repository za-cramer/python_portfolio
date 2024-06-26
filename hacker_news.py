from csv import reader
import os
from pprint import *
import datetime as dt
# Check Working Directory #
cwd = os.getcwd()
cwd

# assign title of csv #
data = 'HN_posts_year_to_Sep_26_2016.csv'

### The Hacker News data set ###
opened_file = open(data, encoding='utf8')
read_file = reader(opened_file)
hacker = list(read_file)
hacker_head = hacker[0]
hacker = hacker[1:]

# inspect data (as list of lists) #
pprint(hacker_head)
pprint(hacker[0:5])

# Filter for AskHN or ShowHN using startswith #
ask_posts = []
show_posts = []
other_posts = []

for i in hacker:
    title = i[1].lower()
    if title.startswith('ask hn'):
        ask_posts.append(i)
    if title.startswith('show hn'):
        show_posts.append(i)
    else:
        other_posts.append(i)

print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))

# Avg # of Comments for Ask HN & Show HN lists [index 4]#
def average_comments(df):
    total = 0
    for i in df:
        comment_field = int(i[4])
        total += comment_field
    avg_comments = total / len(df)
    return(avg_comments)

avg_comments_ask = average_comments(ask_posts)
avg_comments_show = average_comments(show_posts)

print(avg_comments_ask)
print(avg_comments_show)

# Given the traffic ASK receives, we'll focus there #
# Do folks comment more frequently depending on post time? #

# 1. Calculate the amount of ask posts and comments by hour created
    # field: createdat index: -1
    #for row in ask_posts:
    # result_list.append([row[6],int(row[4])])

result_list = []
for i in ask_posts:
    post_time = i[-1]

    # Extract DateTime, then use strftime to extract Hour #
    post_time_dt = dt.datetime.strptime(post_time,"%m/%d/%Y %H:%M").strftime("%H")

    # Extract Comments on that post #
    comments = int(i[4])
    
    # append to result_list #
    result_list.append([post_time_dt,comments])

# 2. Dictionaries for counts & comments by hour #
counts_by_hour = {}
comments_by_hour = {}

for i in result_list:
    hour = i[0]
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = i[1] 
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += i[1]

counts_by_hour
comments_by_hour

# Avg Comments per Post by Hour #
avg_by_hour = []
for i in counts_by_hour:
    if i in comments_by_hour:
        avg_by_hour.append([i, round(comments_by_hour[i] / counts_by_hour[i],2)])
pprint(avg_by_hour)

# Sort by Avg Num of Comments per Post by Hour #
## First Swap column positions into new list of lists ##
swap_avg_by_hour = []
for i in avg_by_hour:
    swap_avg_by_hour.append([i[1], i[0]])

pprint(swap_avg_by_hour)

## sort and store in new list of lists ## 
sorted_swap = sorted(swap_avg_by_hour, reverse=True)

for i in sorted_swap[:5]:
    hr_obj = dt.datetime.strptime(i[1],"%H")
    hr_s = hr_obj.strftime("%H:%M")
    print("{} {:.1f} average comments per post".format(hr_s, i[0]))
