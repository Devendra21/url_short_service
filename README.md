# URL Shortener Webservice

This is a URL shortener webservice built using FastAPI framework.

## Set up virtual environment

- Extract the files in the zip folder in a preferred directory location
- Change to project directory
- Open terminal and run `python3 -m venv <name_of_virtualenv>`

## Install dependencies

In the terminal, run command `pip install -r requirements.txt`

## Running the webservice

- Once the necessary packages have been installed, run the FastAPI app using the following command
`uvicorn main:app --reload`

- After the command has run, you will see the following message in your terminal window

    `
?[32mINFO?[0m:     Uvicorn running on ?[1mhttp://127.0.0.1:8000?[0m (Press CTRL+C to quit)`

    `?[32mINFO?[0m:     Started reloader process [?[36m?[1m4964?[0m] using ?[36m?[1mstatreload?[0m`

    `?[32mINFO?[0m:     Started server process [?[36m19920?[0m]`

    `?[32mINFO?[0m:     Waiting for application startup.`

    `?[32mINFO?[0m:     Application startup complete.`


- Open browser and go to the link <http://127.0.0.1:8000>

- The [link](http://127.0.0.1:8000) redirects to the automatic interactive API documentation rendered by Swagger UI

## Running unit tests

The API documentation allows us to interact with the `GET` and `POST` methods of the webservice.

1. ### `POST` method `/shorten` example
    - On the documentation page, the methods of the service are shown
        ![FastAPI documentation page](/images/doc_page.PNG "FastAPI documentation page")

    - Open the `POST /shorten` method and click on the 'Try it out' button. ![Post method](/images/post2.png "Post method")

    - Next provide the URL and shortcode. Here I have entered the URL as <https://www.energyworx.com/> and the shortcode as `ewx123
 
        ![URL and shortcode provided](/images/post1.PNG "URL and shortcode provided")
    
    - Execute the request and you can see the Response below
    
        ![Response](/images/post3.PNG "Response")

2. ### `GET` method `/{shortcode}`
    Like the example above, we can add the shortcode to test the method which returns the 302 response with the Location header.

    The following images show the Request and Response of the method.
    - ![Get method request](/images/get1.PNG "Get method request")

    - ![Get method response](/images/get2.PNG "Get method response")

3. ### `GET` method `/{shortcode}/stats`
    This method returns the shortcode statistics such as the timestamp of its creation, timestamp of the last redirect using the shortcode and the redirect count.

    - ![stat request](/images/stats1.PNG "stat request")

    - ![stat response](/images/stats2.PNG "stat response")

## TODO:

- Write tests for the app using `fastapi.testclient` and test using `pytest`

- Create UI using Jinja2 templates

- Improve `GET/{shortcode}` method: currently response contains '302 Error:Found'

- Add validator for URL in `POST/shorten` method