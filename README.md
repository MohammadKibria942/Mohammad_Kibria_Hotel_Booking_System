# Hotel Booking System

Simple booking system using FastAPI and SQLite.

## Prerequisites
- Python 3.10+
- `uv` package manager

## Setup
```bash
./scripts/setup.sh
```


This will also initialize the database with 100 rooms so you can start creating
bookings immediately. Rooms `101-150` are standard, `151-180` are deluxe and
`181-200` are suites.


## Example: Create a booking
After running the server you can create a booking for one of the default rooms.
Here is a sample `curl` request using room 101:

```bash
curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -d '{
  "guest_id": "g1",
  "first_name": "yusef",
  "last_name": "kibria",
  "date_of_birth": "2003-03-08",
  "room_type": "standard",
  "room_number": "101",
  "number_of_guests": 0,
  "check_in": "2025-09-20",
  "check_out": "2025-07-24",
  "cancelled": false,
  "checked_in": true,
  "checked_out": false,
  "paid": true
  }'
```

This can also be done using FastAPI accessing it at http://localhost:8000/docs after executing the run.sh script.

## Run
```bash
./scripts/run.sh
```

## Test
```bash
./scripts/test.sh
```

### Windows
These scripts expect a Bash environment. When running on Windows, use Git
Bash or WSL. The activation path for the virtual environment is detected
automatically so the same setup, run and test commands work unchanged.

