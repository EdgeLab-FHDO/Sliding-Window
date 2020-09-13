# SEHNS Individual cases

This files run SEHNS to test the E2EL obtained in each of the four cases of the border problem.
Each case must be run individually and the scenario files adjusted accordinly.

## Usage
1. Configure AdvantEDGE for port mapping
2. Configure the scenario.json file to set the initial position of the vehicles.
3. Update the scenarioReader script to read your scenario.
4. Run the SEHNS server (`s1`).
5. Run the publisher.
6. Run the receiver.

- `"identifier":string` a globally unique identifier for the hazard


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

