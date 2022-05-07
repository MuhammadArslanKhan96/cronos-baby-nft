import random

things = ["common","Earnings","Masks","glasses","specials",]
chance = [70,5,5,4.5,0.5]

results = random.choices(things,chance,k=10000)

from collections import Counter
print(Counter(results))