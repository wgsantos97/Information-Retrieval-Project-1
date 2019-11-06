# Part II: Description

    Author: William Santos
    Date: 11/5/2019

## Information

    Dataset Name: Comics & Graphic Novel Reviews (from Goodreads)
    Format: json
    
    Note:
    Please see the accompanying Results.md for stat information.

___

## Description

> In part II, we are now compiling the data into something more meaningful. It should be noted that the parsing of this data took over 13 hours. The code attempted to parse 500,000+ json entries. The resulting file was so large that I was unable to push it here. However, if you run the code, you can get the same results and folders. Just be aware that it may take awhile and will take 1-2GB of storage on your machine.

> The Results.md has a summary of the data parsing as well as the global frequency of the 5 search queries. These queries were written to simulate an art person who is trying to find a good graphic novel to read from DC comics.

## Notes
> The data parsing was relatively straightforward. Lowercase, tag, lemmatize, and stem the words into each doc object. Then run this into a global frequency dictionary. This was where the process took quite some time. I went back and tried to streamline the process further and also included print statements that help to show overall parsing progress.
