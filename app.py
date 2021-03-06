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

@app.get("/countries/{id}")
async def get_country(id):
    id = int(id)-1
    return countries[id]

@app.post("/countries", status_code=201)
async def add_country(country: Country):
    countries.append(country)
    return country

#curl -i http://127.0.0.1:8000/countries -X POST -H 'Content-Type: application/json' -d '{"name":"Germany", "capital": "Berlin", "area": 357022}' -w '\n'