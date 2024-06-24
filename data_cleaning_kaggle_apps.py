'''
Purpose: to help our developers understand what type of apps are likely 
            to attract more users on Google Play and the App Store

Kaggle Datasource: https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps
Kaggle Datasource (2): https://www.kaggle.com/datasets/lava18/google-play-store-apps

'''
from pprint import pprint 
import pandas as pd
import os 
from csv import reader

ios_csv = 'AppleStore.csv'
android_csv = 'googleplaystore.csv'
# Check Working Directory #
cwd = os.getcwd()
cwd

### The Google Play data set ###
opened_file = open(android_csv, encoding='utf8')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ###
opened_file = open(ios_csv, encoding='utf8')
read_file = reader(opened_file)
apple = list(read_file)
apple_header = apple[0]
apple = apple[1:]

pprint(apple_header)

''' 
---
APPLE
---
id              
track_name
size_bytes
currency
price
rating_count_tot 
rating_count_ver
user_rating
user_rating_ver
ver
cont_rating
prime_genre
sup_devices.num
ipadSc_urls.num
lang.num
vpp_lic
'''

pprint(android_header)

'''
---
ANDROID 
---
App
Category        [X]
Rating          [X]
Reviews         [X]
Size
Installs        [X]
Type
Price           [X]
Content Rating  [X]
Genres          [X]
Last Updated
Current Ver
Android Ver
'''

# Clean Data #

# Discussion identified errant row of data 
print(android[10472])

# drop row & save df #
del android[10472] # use only once per session

# check that it was dropped #
print(android[10472])

# Function to identify duplicates & unique apps in df #
duplicates = []
unique = []
for app in android:
    name = app[0]
    if name in unique:
        duplicates.append(name)
    else:
        unique.append(name)

print(len(duplicates))
print(duplicates[:15])

print(len(unique))
print(unique[:15])

# We'll keep the record with the highest number of 
# app ratings and remove all else.
reviews_max = {}

# use android (df without header) #
for i in android:
    name = i[0] # app name is the 0 index of each row
    n_reviews = float(i[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    if name not in reviews_max:
        reviews_max[name] = n_reviews

print(len(reviews_max))

android_clean = [] # will store cleaned df
already_added = [] # will store app names

for i in android:
    name = i[0]
    n_reviews = float(i[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(i)
        already_added.append(name)

print(len(android_clean))

## Remove non english apps identified by ASCII code (0-127) ##
for i in "爱奇艺PPS -《欢乐颂2》电视剧热播":
    if ord(i) < 127:
        "English"
    else: 
        "Not English"

# However, some English apps have non-English characters (emojis, tm, etc).
#   Modify to exclude any app name with over 3 non-English Characters 
string_count = 0
for i in "Instagram":
    if ord(i) < 127:
        string_count += 0
    else:
        string_count += 1
if string_count > 3:
    "Non-English"
else: 
    "English"

# OR #
def check_language(s):
    string_count = sum(1 for i in s if ord(i) >= 127)
    return "Non-English" if string_count > 3 else "English"

# Example usage
check_language("Docs To Go™ Free Office Suite")
check_language("爱奇艺PPS -《欢乐颂2》电视剧热播")

# Filter out NON-ENGLISH Apps with above criteria #
android_english = []
android_non_english = []
apple_english = []
apple_non_english = []

for i in android_clean:
    if check_language(i[0]) == 'English':
        android_english.append(i)
    else:
        android_non_english.append(i)
print(len(android_english))

for i in apple:
    if check_language(i[1]) == 'English':
        apple_english.append(i)
    else:
        apple_non_english.append(i)

print(len(apple_english))

# Isolate only the free apps for our analysis #
# Android index == 6
# IOS index == 4
print(android_english[0])

android_en_free = []
apple_en_free = []
for i in android_english:
    if i[6] == 'Free':
        android_en_free.append(i)

print(len(android_en_free))

print(type(apple_english[1][4]))
print((apple_english[1][4]))

for i in apple_english:
    if i[4] == '0.0':
        apple_en_free.append(i)
print(len(apple_en_free))

# Now have FREE ENGLISH APPS in Apple & Android #
# Apple_en_free & Android_en_free #
