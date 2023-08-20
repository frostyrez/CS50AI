# Shopping

Predict whether online shopping customers will complete a purchase.

<img width="650" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/0f70712d-8b6c-445e-b3e7-c56f8791d36b">

## Outline

- Being able to accurately predict user shopping habits based on the pages they visit, how long they spend on each page, and other user information is incredibly useful for the shopping website's owner and can single-handedly drive many tangible, targeted improvements to a website.
- In this case, a `scikit-learn` `KNeighborsClassifier` model is trained and tested on a .csv file containing over 12,000 rows of data.
- Instead of outputting a single accuracy percentage on the resulting data, two contrasting accuracy values are provided: sensitivity (or "true positive rate") and specificity (or "true negative rate"). This allows for two separate evaluations of the model, one based on the pool of shoppers that did complete a purchase, and another based on the pool of shoppers that did not complete a purchase.

## Usage
`python shopping.py shopping.csv`
