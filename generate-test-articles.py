import random
import lorem
from datetime import datetime, timedelta


def generate_random_date(start_date, end_date):
    # Convert start_date and end_date to datetime objects
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    # Generate a random number of days between start_date and end_date
    random_days = random.randint(0, (end_dt - start_dt).days)

    # Add the random number of days to start_date
    random_date = start_dt + timedelta(days=random_days)

    # Format the random_date as YYYY-MM-DD
    formatted_date = random_date.strftime("%Y-%m-%d")

    return formatted_date


authors = ["Kormos kristóf", "Zoller András", "ChatGPT",
           "Juhász István", "Dallos Levente", "Kalos Marcell", "Tóth Gábor"]
authors = [f'"{i}"' for i in authors]
headings = [
    "facilisis",
    "matematika",
    "nunc",
    "sport",
    "tristique",
    "zene",
    "újságírás"]

for i in range(50):
    num_of_authors = random.randint(1, 3)
    auths = random.sample(authors, num_of_authors)
    random_date = generate_random_date("2011-01-01", "2021-12-31")

    doc = f"""---
title: "{lorem.sentence()}"
date: {random_date}
draft: false 
authors: [{",".join(auths)}]
heading: "{random.sample(headings, 1)[0]}"
summary: "{lorem.sentence()}"
images: ["https://picsum.photos/seed/{random_date}/1280/853.webp"]
cover: "https://picsum.photos/seed/{random_date}/1280/853.webp"
---
"""
    seed = random.randint(1, 6)

    for j in range(6):
        image = f'{{{{<image src="https://picsum.photos/seed/{i}{j}{seed}/1280/853.webp">}}}}' if i % seed == 0 else ""

        par = f"""# {lorem.sentence()}        
{lorem.paragraph()}
{image}
"""

        doc += par

    with open(f"./content/articles/boilerplate{i}.md", "w") as f:
        print(doc, file=f)
