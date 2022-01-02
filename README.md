
[FastAPI](https://fastapi.tiangolo.com/)  is a Python web framework that’s optimized for building APIs. It uses  [Python type hints](https://realpython.com/python-type-checking/)  and has built-in support for  [async operations](https://realpython.com/async-io-python/). FastAPI is built on top of  [Starlette](https://www.starlette.io/)  and  [Pydantic](https://pydantic-docs.helpmanual.io/)  and is very performant.

Below is an example of the REST API built with FastAPI:

```
# app.py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

def _find_next_id():
    return max(country.country_id for country in countries) + 1

class Country(BaseModel):
    country_id: int = Field(default_factory=_find_next_id, alias="id")
    name: str
    capital: str
    area: int

countries = [
    Country(id=1, name="Thailand", capital="Bangkok", area=513120),
    Country(id=2, name="Australia", capital="Canberra", area=7617930),
    Country(id=3, name="Egypt", capital="Cairo", area=1010408),
]

@app.get("/countries")
async def get_countries():
    return countries

@app.post("/countries", status_code=201)
async def add_country(country: Country):
    countries.append(country)
    return country
```


This application uses the features of FastAPI to build a REST API for the same  `country`  data you’ve seen in the other examples.

You can try this application by installing  `fastapi`  with  `pip`:

`$ python -m pip install fastapi` 

You’ll also need to install  `uvicorn[standard]`, a server that can run FastAPI applications:

`$ python -m pip install uvicorn[standard]` 

If you’ve installed both  `fastapi`  and  `uvicorn`, then save the code above in a file called  `app.py`. Run the following command to start up a development server:

```
$ uvicorn app:app --reload
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The server is now running. Open up a browser and go to  `http://127.0.0.1:8000/countries`. You’ll see FastAPI respond with this:

```
[
    {
        "id": 1,
        "name":"Thailand",
        "capital":"Bangkok",
        "area":513120
    },
    {
        "id": 2,
        "name":"Australia",
        "capital":"Canberra",
        "area":7617930
    },
    {
        "id": 3,
        "name":"Egypt",
        "capital":"Cairo",
        "area":1010408
    }
]
```

FastAPI responds with a JSON array containing a list of  `countries`. You can also add a new country by sending a  `POST`  request to  `/countries`:

```
$ curl -i http://127.0.0.1:8000/countries \
-X POST \
-H 'Content-Type: application/json' \
-d '{"name":"Germany", "capital": "Berlin", "area": 357022}' \
-w '\n'

HTTP/1.1 201 Created
content-type: application/json
...

{"id":4,"name":"Germany","capital":"Berlin","area": 357022}
``` 

You added a new country. You can confirm this with  `GET /countries`:

```
$ curl -i http://127.0.0.1:8000/countries -w '\n'

HTTP/1.1 200 OK
content-type: application/json
...

[
 {
 "id":1,
 "name":"Thailand",
 "capital":"Bangkok",
 "area":513120,
 },
 {
 "id":2,
 "name":"Australia",
 "capital":"Canberra",
 "area":7617930
 },
 {
 "id":3,
 "name":"Egypt",
 "capital":"Cairo",
 "area":1010408
 },
 {
 "id":4,
 "name": "Germany",
 "capital": "Berlin",
 "area": 357022
 }
]
``` 

FastAPI returns a JSON list including the new country you just added.

You’ll notice that the FastAPI application looks similar to the Flask application. Like Flask, FastAPI has a focused feature set. It doesn’t try to handle all aspects of web application development. It’s designed to build APIs with modern Python features.

If you look near the top of  `app.py`, then you’ll see a class called  `Country`  that extends  `BaseModel`. The  `Country`  class describes the structure of the data in the REST API:

```
class Country(BaseModel):
    country_id: int = Field(default_factory=_find_next_id, alias="id")
    name: str
    capital: str
    area: int
```

This is an example of a  [Pydantic model](https://pydantic-docs.helpmanual.io/usage/models/). Pydantic models provide some helpful features in FastAPI. They use Python type annotations to enforce the data type for each field in the class. This allows FastAPI to automatically generate JSON, with the correct data types, for API endpoints. It also allows FastAPI to validate incoming JSON.

It’s helpful to highlight the first line as there’s a lot going on there:

`country_id: int = Field(default_factory=_find_next_id, alias="id")` 

In this line, you see  `country_id`, which stores an  [integer](https://realpython.com/python-numbers/#integers)  for the ID of the  `Country`. It uses the  [`Field`  function](https://pydantic-docs.helpmanual.io/usage/schema/#field-customisation)  from Pydantic to modify the behavior of  `country_id`. In this example, you’re passing  `Field`  the keyword arguments  `default_factory`  and  `alias`.

The first argument,  `default_factory`, is set to  `_find_next_id()`. This argument specifies a function to run whenever a new  `Country`  is created. The return value will be assigned to  `country_id`.

The second argument,  `alias`, is set to  `id`. This tells FastAPI to output the key  `"id"`  instead of  `"country_id"`  in the JSON:

```
{
    "id":1,
    "name":"Thailand",
    "capital":"Bangkok",
    "area":513120,
},
```
 

This  `alias`  also means you can use  `id`  when you create a new  `Country`. You can see this in the  `countries`  list:

```
countries = [
    Country(id=1, name="Thailand", capital="Bangkok", area=513120),
    Country(id=2, name="Australia", capital="Canberra", area=7617930),
    Country(id=3, name="Egypt", capital="Cairo", area=1010408),
]
```

This list contains three instances of  `Country`  for the initial countries in the API. Pydantic models provide some great features and allow FastAPI to easily process JSON data.

Now take a look at the two API functions in this application. The first,  `get_countries()`, returns a list of  `countries`  for  `GET`  requests to  `/countries`:

`@app.get("/countries")
async def get_countries():
    return countries` 

FastAPI will automatically create JSON based on the fields in the Pydantic model and set the right JSON data type from the Python type hints.

The Pydantic model also provides a benefit when you make a  `POST`  request to  `/countries`. You can see in the second API function below that the parameter  `country`  has a  `Country`  annotation:

`@app.post("/countries", status_code=201)
async def add_country(country: Country):
    countries.append(country)
    return country` 

This type annotation tells FastAPI to validate the incoming JSON against  `Country`. If it doesn’t match, then FastAPI will return an error. You can try this out by making a request with JSON that doesn’t match the Pydantic model:

```
$ curl -i http://127.0.0.1:8000/countries \
-X POST \
-H 'Content-Type: application/json' \
-d '{"name":"Germany", "capital": "Berlin"}' \
-w '\n'

HTTP/1.1 422 Unprocessable Entity
content-type: application/json
...

{
 "detail": [
 {
 "loc":["body","area"],
 "msg":"field required",
 "type":"value_error.missing"
 }
 ]
}
``` 

The JSON in this request was missing a value for  `area`, so FastAPI returned a response with the status code  `422 Unprocessable Entity`  as well as details about the error. This validation is made possible by the Pydantic model.

This example only scratches the surface of what FastAPI can do. With its high performance and modern features like  `async`  functions and automatic documentation, FastAPI is worth considering for your next REST API.
