# bayeshack2016-hhs-marketplace

### How can we make it easy to find a healthcare plan that meets your needs?

#### The Data

The csv files explored in the starter kit gave a comprehensive overview of the Healthcare Plans, but information about the healthcare providers (i.e. Doctors) proved to be more tricky....

Using the JSON files linked by the insurers, we were able to generate files linking which doctors were covered or "in network" for each plan. 
Since healthcare is provided regionally, we subdivided by state to allow smaller file sizes and quick access.
Converting csv to hdf5 also allowed to speedy reading and parsing

Once we have the data at our fingertips, we can start utilizing user input to narrow the field.

##### Understanding the Data
Understanding how the data is organized, the idiosyncracies of the input, etc. was a major part of this project. En route to building an user interface to help consumers navigate the complicated health insurance market, we as team learned a heck of a lot about the health insurance system organization. 

We wrote [a few words](/analysis/quicks.ipynb) about our findings while exploring the the datasets, and we also started a somewhat finicky but [working way](/analysis/download_providers.ipynb) to download the information about health care providers and their relationships to insurers which are only accessible via following a myriad of urls. 




#### The Interface

![Alt text](/screenshots/zipAgeSearch.png?raw=true "Optional Title")

Zipcode and age can narrow things down tremendously right off the bat. A quick bar plot gives you a sense of the price range for different plan levels.

![Alt text](/screenshots/nation_comparison.png?raw=true "Optional Title")

Then you can find out what plans have your Doctor in network. Just start typing their name and you'll get some autocomlete suggestions. Then the bar plot will update to show you how the plans that include your doctor compare to the rest of the state and the nation.

![Alt text](/screenshots/sc3.png?raw=true "Optional Title")

![Alt text](/screenshots/sc4.png?raw=true "Optional Title")

You'll also get a list of some plans 


