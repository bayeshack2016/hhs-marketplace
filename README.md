# bayeshack2016-hhs-marketplace

### How can we make it easy to find a healthcare plan that meets your needs?

#### The Data

The csv files explored in the starter kit gave a comprehensive overview of the Healthcare Plans, but information about the healthcare providers (i.e. Doctors) proved to be more tricky....

Using the JSON files linked by the insurers, we were able to generate files linking which doctors were covered or "in network" for each plan. 
Since healthcare is provided regionally, we subdivided by state to allow smaller file sizes and quick access.
Converting csv to hdf5 also allowed to speedy reading and parsing

Once we have the data at our fingertips, we can start utilizing user input to narrow the field.

#### The Interface

![alt tag](https://raw.githubusercontent.com/xinluh/bayeshack2016-hhs-marketplace/.png)

Zipcode and age can narrow things down tremendously right off the bat. A quick bar plot gives you a sense of the price range for different plan levels.

(Show screenshot here?)

Then you can find out what plans have your Doctor in network. Just start typing their name and you'll get some autocomlete suggestions. Then the bar plot will update to show you how the plans that include your doctor compare to the rest of the state and the nation.

(Maybe another screenshot?)

You'll also get a list of some plans 

