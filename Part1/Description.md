# Part I: Description

    Author: William Santos
    Date: 10/20/2019

## Information

    Dataset Name: Comics & Graphic Novel Reviews (from Goodreads)
    Format: json
    
    Note:
    Please see the accompanying Results.md for stat information.

___

## Description

> This dataset is comprised of all reviews for Graphic Novels from Goodreads. To make the data easier to identify, I also created a filtered version of its companion dataset, "graphic_novels_raw.json", which contains data on each graphic novel. That dataset can be found in Data->RawData along with the python file that filters it and writes the newly filtered json file. This filtered version, "graphic_novels.json", merely contains a dictionary where the key is the "book_id" and the value is the "title".
___
> Below is a sample of each json file that I will be using for this project:

## Graphic Novel Review Sample JSON

```json
"graphic_novel_reviews.json" (542,338 reviews)
{
    "user_id": "dc3763cdb9b2cae805882878eebb6a32",
    "book_id": "18471619",
    "review_id": "66b2ba840f9bd36d6d27f46136fe4772",
    "rating": 3,
    "review_text":
        "Sherlock Holmes and the Vampires of London
        ...
        I would have to say pass on this one. \n That artwork is good, cover is great, story is lacking
        so I am giving it 2.5 out of 5 stars.",
    "date_added": "Thu Dec 05 10:44:25 -0800 2013",
    "date_updated": "Thu Dec 05 10:45:15 -0800 2013",
    "read_at": "Tue Nov 05 00:00:00 -0800 2013",
    "started_at": "",
    "n_votes": 0,
    "n_comments": 0
}
...
```

___

## Graphic Novel Data Sample JSON

```json
"graphic_novels.json" (89,411 book entries)
{
    "25742454": "The Switchblade Mamma",
    "30128855": "Cruelle",
    ...
}
```
