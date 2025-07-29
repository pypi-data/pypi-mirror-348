# CarbonawareScheduler

Types:

```python
from carbonaware_scheduler.types import RetrieveResponse
```

Methods:

- <code title="get /">client.<a href="./src/carbonaware_scheduler/_client.py">retrieve</a>() -> <a href="./src/carbonaware_scheduler/types/retrieve_response.py">RetrieveResponse</a></code>

# Schedule

Types:

```python
from carbonaware_scheduler.types import CloudZone, ScheduleOption, ScheduleCreateResponse
```

Methods:

- <code title="post /v0/schedule/">client.schedule.<a href="./src/carbonaware_scheduler/resources/schedule.py">create</a>(\*\*<a href="src/carbonaware_scheduler/types/schedule_create_params.py">params</a>) -> <a href="./src/carbonaware_scheduler/types/schedule_create_response.py">ScheduleCreateResponse</a></code>

# Regions

Types:

```python
from carbonaware_scheduler.types import RegionListResponse
```

Methods:

- <code title="get /v0/regions/">client.regions.<a href="./src/carbonaware_scheduler/resources/regions.py">list</a>() -> <a href="./src/carbonaware_scheduler/types/region_list_response.py">RegionListResponse</a></code>

# Health

Types:

```python
from carbonaware_scheduler.types import HealthCheckResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/carbonaware_scheduler/resources/health.py">check</a>() -> <a href="./src/carbonaware_scheduler/types/health_check_response.py">HealthCheckResponse</a></code>
