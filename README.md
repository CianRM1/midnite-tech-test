# Midnite Technical Task

## Getting Started

This project implements a Django API endpoint /event to monitor user activity and trigger alerts based on predefined rules.

The endpoint processes user actions (like deposits and withdrawals) and returns whether any alerts have been triggered for the user.

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management
- Django 5.1.5

### Install Dependencies

```sh
poetry install
```

### Start API Server

```sh
poetry run python user_monitoring/manage.py runserver
```

The server will run at http://127.0.0.1:8000.

### Run Tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{ }'
```

## Logic and Rules

### Rules Implemented

Withdrawal Over 100 (Code: 1100):

- Triggered when a single withdrawal exceeds 100.

Three Consecutive Withdrawals (Code: 30):

- Triggered when 3 consecutive actions for the same user are withdrawals.

Three Consecutive Increasing Deposits (Code: 300):

- Triggered when the user makes 3 consecutive deposits where each deposit is larger than the previous one (ignoring withdrawals in between).

Total Deposits Exceeding 200 in 30 Seconds (Code: 123):

- Triggered when the sum of deposits in the last 30 seconds exceeds 200.

## Notes

- All logic for alerts is encapsulated in utils.py for modularity and reusability.
- Alert codes are stored in constants.py for better maintainability.
- In-memory caching is used to store the last 10 user actions for efficient rule evaluation.
