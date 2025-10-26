# How to run the project
* Clone the repo `git clone git@github.com:elebur/VoteAPI.git`
* Build the docker images `docker compose build`
* Run docker compose `docker compose up`

## Create superuser
* Connect to the container `docker exec -it vote_api bash`
* `cd company/`
* `python manage.py createsuperuser`
* Provide credentials for the new super user
* `exit` - to return to the host terminal


## Using the service
The service will be available under this address http://127.0.0.1:8000/

# Endpoints
## Authentication

`POST`: `/api/token/` - get new JWT token

The body of the request (all fields are required):
```json
{
    "username": "user",
    "password": "password"
}
```
---

`POST`: `/api/token/refresh/` - refresh access token

The body of the request (all fields are required):
```json
{
    "refresh": "refresh_token_here"
}
```

## Employees
`POST`: `/api/employee/` - create new employee.
> Requires admin rights

The body of the request (all fields are required):
```json
{
    "first_name": "User",
    "last_name": "Name",
    "username": "username",
    "password": "password",
    "email": "user@name.com"
}
```
---

`GET`: `/api/employee/<employee_id>` - get info about employee.

`<employee_id>` - the ID of the employee

---

## Restaurant
`POST`: `/api/restaurant/` - create new restaurant
> Requires admin rights

The body of the request (all fields are required):
```json
{
     "name": "Pepo's"
}
```
---

`GET`: `/restaurant/<restaurant_id>` - get info about the restaurant

`<restaurant_id>` - the ID of the restaurant

## Menu
`POST`: `/api/menu/` - create new menu.

The body of the request:
`title` and `notes` are optional
```json
{
    "restaurant": 1,
    "title": "Menu title",
    "notes": "Note about the menu",
    "launch_date": "2025-10-25",
    "items": [
        {
            "title": "Item#1",
            "description": "Descr#1"
        },
        {
            "title": "Item#2",
            "description": "Descr#2"
        }
    ]
}
```

---

`GET`: `/api/menu/<menu_id>/` - get info about the menu

---

`GET`: `/api/menu/` - returns today's menus

---
`GET`: `menu/<YYYY-DD-MM>/` - returns menus for the given date

## Vote
`POST`: `menu/<menu_id>/vote/` - add like/dislike for the given menu

> User must be authenticated

```json
{
    // integer
    "employee_id": 1,
    // bool
    "like": false
}
```

---
`GET`: `vote/results/` - returns results for today's menus.