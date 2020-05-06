# Using Selenium Python and Twilio API to get Great Deals at Revolve

Revolve is one of my favorite places to shop, but sometimes it can be a pain to scroll for hours looking for the best deals.

I made this small project to have a little fun. 

It uses Selenium in Python to search for deals. The app comes with a simple command line interface to let you search:
    1. by clothing categories: clothing, shoes, or denim
    2. by clothing sizes
    3. sorting criteria including: best sellers, new arrivals, featured items, price low to high, and price high to low
    4. the number of items you want to search for
    5. how often to run the app. (It is currently set to 2 hours, but your need for deals might be much lower than this)

# Example

```
    python3 revolve.py --category=apparel --size=m --order=low-to-high --number=4 --time=3600
```

# Requirements

1. selenium
2. numpy
3. csv
4. twilio.rest
5. python3

You will need to get a developer account at Twilio and enable their messaging service to send an SMS. 


# Considerations

Since Revolve's app uses dynamic URL's, the driver mimics the natural behavior of a user. 

This makes the proejct brittle, but can be a good starting point if you want to get some practice manipulating the DOM!

Because I personally enjoy watching my browser automagically do things, I have included a visible browsing session.

If you would rather not have the browser be visible, run the driver with `--headless` enabled as an option. 







