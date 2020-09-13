# Hazard Registry Service

## Usage

All responses will have the form

```json
{
    "data": "content of the response",
    "message": "Description of the response"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all notified hazards on the server

**Definition**

`GET /detected_hazards`

**Response**

- `200 OK` on success

```json
[
    {
    "message": "Success",
    "data": [
        {
            "identifier": "h0",
            "hazard_name": "h_name",
            "hazard_type": "pedestrian",
            "location": "1207.66666667"
        },
        {
            "identifier": "h1",
            "hazard_name": "h_name",
            "hazard_type": "pothole",
            "location": "1533.91666667"
        },
        {
            "identifier": "h2",
            "hazard_name": "h_name",
            "hazard_type": "ice patch",
            "location": "1731.83333333"
        }
    ]
}
]
```

### When the vehicle attempts to post a detected hazard

**Definition**

`POST /detected_hazards`

**Arguments**

- `"identifier":string` a globally unique identifier for the hazard
- `"hazard_name":string` a name given to the hazard
- `"hazard_type":string` the type of detected hazard (pothole, pedestrian, icepatch, ...)
- `"location":number` the position of where the vehicle has detected the hazard

If a hazard with the given identifier already exists, the existing hazard will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "identifier": "h1",
    "hazard_name": "hazard_detected",
    "hazard_type": "pothole",
    "location": "1334.6"
}
```

##  hazard details

`GET /detected_hazard/<identifier>`

**Response**

- `404 Not Found` if the hazard identifier does not exist on the DB
- `200 OK` on success

```json
{
    "identifier": "h1",
    "hazard_name": "hazard_detected",
    "hazard_type": "pothole",
    "location": "1334.6"
}
```

## Delete a device

**Definition**

`DELETE /detected_hazard/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `204 No Content` on success