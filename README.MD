# FARA FOREIGN PRINCIPALS 
(GOVPREDICT.COM TEST SCRAPER)

This is a Scrapy based crawler what can collapse Foreign Principals 
      from http://fara.gov/quick-search.html site


# Installation requirements

  - Python 2.7
  - Pip
  - Scrapyd 
  - Scrapy 1.03
  - unix like operation systems (i was developed in osx, and tested in ubuntu linux)

# Installation steps
```sh
  -  unpack the archive
  -  ./install (these function install dependencies and requirements)
  -  ./deploy  (these function add project to scrapyd and run the spider)
  - ./make_tests (run unit tests)
```
Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8600
```
### Availabe Commands 
- ```install ```  (installing dependecies and start scrapyd in screen as a baackground process)
 - ```deploy``` (add govpredict project to scrapyd and run spider to generating json to output folder)
- ```destroy``` (remove all generated things and destroy the scrapyd in the screen)
- ```mstart``` (without scrapyd run directly the spider)
### Todos
 - Implement paginations and more sophisticated scraping with phantomjs and/or with selenium
 - fixing bugs 
License
----
BSD
### Author 
 ```Stv@n <istvan.makai@gmail.com>```
``` created @ 2017-02-23 ```