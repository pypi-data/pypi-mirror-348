# tripletex

## Short Description

An efficient and user-friendly Python library crafted specifically for seamless integration with [Tripletex](https://www.tripletex.no)'s accounting and financial management APIs.

## Features

- Easy authentication with the Tripletex API
- Access to invoices, customers, projects, and more
- Clean and extensible design for integration into your own systems

## Installation

Install the library using [Poetry](https://python-poetry.org/):

```bash
poetry add tripletex
```

## Getting Started: Setup & Authentication

To use the Tripletex API, you must configure authentication and initialize the API client. This setup is required for all usage patterns.

### 1. Configure Your Credentials

```python
from tripletex.core.config import TripletexConfig

config = TripletexConfig(
    consumer_token="YOUR_CONSUMER_TOKEN",
    employee_token="YOUR_EMPLOYEE_TOKEN",
    # company_id="123456",           # Optional: set if you need a specific company
    # hostname="https://tripletex.no/", # Optional: override for test/prod
    # version="v2",                  # Optional: API version (default: "v2")
)
```

**Replace** `"YOUR_CONSUMER_TOKEN"` and `"YOUR_EMPLOYEE_TOKEN"` with your actual Tripletex API tokens.

### 2. Initialize the Client and API

```python
from tripletex.core.client import TripletexClient
from tripletex.core.api import TripletexAPI

# Create the internal HTTP client (not used directly for resource operations)
client = TripletexClient(config=config)

# Instantiate the main user-facing API object
api = TripletexAPI(client=client)
```

> **Tip:** You can also instantiate the API directly with `TripletexAPI(client_config=config)` if you prefer.

### 3. Make Your First API Call

```python
# List suppliers
suppliers = api.suppliers.list()
for supplier in suppliers.values:
    print(f"Supplier ID: {supplier.id}, Name: {supplier.name}")
```

---

## Covered Tripletex API Resources

Below is a high-level summary of the Tripletex API resources currently covered by this library and their implementation status:

| Resource                                   | Status  | Description                                                                                   |
|---------------------------------------------|:-------:|-----------------------------------------------------------------------------------------------|
| Activity                                   | ⚠️      | Partially Implemented – Most core endpoints are healthy, some advanced endpoints missing.      |
| Company                                    | ❌      | Not Implemented – Endpoints for company resource are not yet implemented.                      |
| Country                                    | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Department                                 | ⚠️      | Experimental/Skipped – Most endpoints are skipped due to HTTP 422 errors (API key issues).     |
| Employee                                   | ⚠️      | Experimental/Skipped – Some endpoints are healthy, others skipped due to model errors.         |
| Project                                    | ⚠️      | Experimental/Skipped – Only main list endpoint is healthy; others depend on unimplemented APIs.|
| Supplier                                   | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger/Account                             | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger                                     | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger/Payment Type Out                     | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger/Voucher/Historical                  | ⚠️      | Experimental/Skipped – Most endpoints not implemented or skipped due to test env. limitations. |
| Ledger/Voucher/OpeningBalance              | ⚠️      | Partially Implemented – Some endpoints healthy, others not implemented or skipped.             |
| Ledger/Posting                             | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger/Vat Type                            | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger/Voucher                             | ⚠️      | Partially Implemented – Many endpoints healthy, some not implemented or deprecated.            |
| Ledger/Voucher Type                        | ✅      | Fully Implemented – All endpoints are implemented and tested.                                  |
| Ledger/Close Group, Annual Account, Accounting Period, Posting Rules | ❌ | Not Implemented – These resources are not yet implemented.                                     |

**Legend:**
✅ = Fully Implemented & Healthy
⚠️ = Partially Implemented / Experimental / Skipped
❌ = Not Implemented

This overview is based on the latest endpoint health report and provides a quick reference to the current API coverage.

---

## Using the API

Once you have completed the [Setup & Authentication](#getting-started-setup--authentication), you can interact with Tripletex API resources as follows:

### Accessing Resource Clients

Resource clients are available as attributes of the `TripletexAPI` instance:

```python
projects = api.projects      # Project resource client
suppliers = api.suppliers   # Supplier resource client
```

### Common CRUD Operations

- **List resources** (with optional pagination):

  ```python
  all_projects = api.projects.list(count=10, from_=0)
  ```

- **Get a specific resource by ID**:

  ```python
  project = api.projects.get(id=123)
  ```

- **Create a new resource** (using Pydantic models):

  ```python
  from tripletex.endpoints.project.models import ProjectCreate, IdRef

  new_project_data = ProjectCreate(
      name="New Cool Project",
      project_manager=IdRef(id=1)  # Replace with a valid employee ID
  )
  created_project = api.projects.create(data=new_project_data)
  ```

- **Update an existing resource**:

  ```python
  from tripletex.endpoints.project.models import ProjectUpdate, IdRef

  updated_project_data = ProjectUpdate(
      name="Updated Project Name",
      project_manager=IdRef(id=1)
  )
  updated_project = api.projects.update(id=123, data=updated_project_data)
  ```

- **Delete a resource**:

  ```python
  api.projects.delete(id=123)
  ```

### Custom Actions and Extended Methods

Some resource clients provide additional methods for non-standard API operations. For example, the suppliers client includes a `search` method:

```python
matching_suppliers = api.suppliers.search(name="Acme Corp")
```

Refer to the resource client's documentation for details.

### Model Usage

- For `create` and `update` operations, always use the appropriate Pydantic model (e.g., `ProjectCreate`, `ProjectUpdate`).
- API responses are typically returned as Pydantic model instances (e.g., `Project`) or lists thereof.
- Refer to the models in `tripletex/endpoints/<resource>/models.py` for available fields and usage.

---

## Configuration Reference

### `TripletexConfig` Parameters

| Parameter        | Type     | Default                      | Description                                                      |
|------------------|----------|------------------------------|------------------------------------------------------------------|
| consumer_token   | str      | "" (from env if set)         | **Required.** Your Tripletex API consumer token.                 |
| employee_token   | str      | "" (from env if set)         | **Required.** Your Tripletex API employee token.                 |
| company_id       | str      | "0"                          | Optional. The company ID to use for requests.                    |
| hostname         | str      | "https://tripletex.no/"      | Optional. Base URL for the Tripletex API.                        |
| version          | str      | "v2"                         | Optional. API version.                                           |

Other advanced parameters (such as session token management) are handled internally and do not need to be set for typical usage.

> **Note:** For test environments, use `TripletexTestConfig` or set the `DEBUG` environment variable to `"1"` to automatically use test credentials and endpoints.

---

## Error Handling

When interacting with the Tripletex API, errors may occur due to invalid input, failed validation, or HTTP errors (such as 4xx or 5xx responses from the API). The library delegates most error handling to the underlying [`crudclient`](https://github.com/andersinno/crudclient) package, which raises exceptions for non-successful responses and data validation issues.

**Example: Handling API and Validation Errors**

```python
from crudclient.exceptions import DataValidationError

try:
    # Example: Attempt to fetch a non-existent project
    project = api.projects.get(id=9999999)
    print(project)
except DataValidationError as e:
    print(f"Validation error: {e}")
    print(f"Invalid data: {getattr(e, 'data', None)}")
except Exception as e:
    print(f"An error occurred: {e}")
```

**Exception Types**

- `DataValidationError`: Raised when the data provided to a resource operation fails Pydantic validation or does not conform to the expected schema.
- `ValueError`: Raised in rare cases when the response from the API is not in the expected format.
- Other errors, such as network issues or unexpected server responses, may raise generic Python exceptions or exceptions from the `crudclient` package.

See the [`crudclient`](https://github.com/leikaab/crudclient) documentation for more details.

---

## Using Services

Services provide higher-level abstractions or convenience methods for common business operations that may span multiple API resources or require additional logic.

### Posting Service

The `PostingService` helps you create posting drafts from simple information, handling lookups for accounts and suppliers automatically.

**How to Access**

```python
from tripletex.services.posting_service import PostingService

# Assuming you have already set up `api` as shown in [Setup & Authentication](#getting-started-setup--authentication)
posting_service = PostingService(api_client=api)
```

**Main Method: `create_posting_draft`**

```python
from tripletex.endpoints.ledger.models.posting import PostingCreate

posting_draft = posting_service.create_posting_draft(
    description="Office supplies purchase",
    account_no="6540",         # The account number as a string
    amount=1200.00,            # The posting amount
    supplier_name="Staples",   # Optional: supplier name
    supplier_org_nr=None,      # Optional: supplier org number
    row=1                      # Optional: row number in the voucher
)

print(posting_draft)
```

See [`tripletex/services/posting_service.py`](tripletex/services/posting_service.py:1) for more details.

---

## API Rate Limiting

This library supports a built-in, pluggable rate limiter to help manage requests to the Tripletex API and avoid exceeding API rate limits. **Rate limiting is optional and disabled by default.**

### Enabling Rate Limiting

```python
from tripletex.utils.rate_limiter import FileBasedRateLimiter

lock_file = "/tmp/tripletex_rate_limit.lock"
state_file = "/tmp/tripletex_rate_limit_state.json"
rate_limiter = FileBasedRateLimiter(
    lock_file_path=lock_file,
    state_file_path=state_file,
    default_remaining=10,      # Set your max_calls per period
    default_reset_ts=0.0       # Will be managed automatically
)

api = TripletexAPI(
    client_config=config,
    rate_limiter=rate_limiter,
    num_workers=1,    # Adjust if using parallel workers
    buffer_size=1     # Adjust buffer as needed
)
```

### Disabling Rate Limiting

If you do **not** pass a `rate_limiter` to `TripletexAPI`, rate limiting is disabled and all requests will be sent without restriction.

---

## Contributing

We welcome contributions to this project! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Setting up the Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Leikaab/tripletex.git
   cd tripletex
   ```

2. **Install dependencies (including development dependencies):**
   ```bash
   poetry install --with dev
   ```

### Running Tests

- To run all tests (unit and integration):
  ```bash
  poetry run pytest
  ```
  By default, all tests in the `tests/` directory are discovered and run in parallel.

- To run only unit tests with coverage:
  ```bash
  poetry run pytest tests/unit/ --cov --cov-report=term-missing --cov-branch
  ```

### Code Style and Linting

This project uses several tools to ensure code quality and consistency:
- **autoflake** (removes unused imports)
- **isort** (import sorting, Black profile)
- **black** (code formatting)
- **flake8** (style and linting)
- **mypy** (type checking)

All of these are run automatically via [pre-commit](https://pre-commit.com/) hooks. To check all files manually:
```bash
poetry run pre-commit run --all-files
```

### Submitting Changes

- Fork the repository and create a new feature branch.
- Make your changes and ensure all tests and linters pass.
- Commit your changes with clear messages.
- Push your branch and open a pull request (PR) against the main repository.

For larger changes or new features, consider opening an issue first to discuss your proposal.

- Existing issues can be found on the [GitHub Issues page](https://github.com/Leikaab/tripletex/issues).

Thank you for helping improve this project!

---

## License

This project is licensed under a proprietary license. All rights reserved. See the [LICENSE](https://github.com/Leikaab/crudclient/blob/main/LICENSE) file for details.

## Library Structure

- **core/**: Core infrastructure (API client, config, base CRUD, shared models)
- **endpoints/**: Modules for each Tripletex API resource (CRUD logic, resource models)
- **services/**: High-level service abstractions and workflows
- **utils/**: Internal utilities (e.g., rate limiting)
