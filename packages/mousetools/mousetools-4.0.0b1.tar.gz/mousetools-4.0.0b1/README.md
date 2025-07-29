# MouseTools
[![PyPI version](https://badge.fury.io/py/MouseTools.svg)](https://badge.fury.io/py/MouseTools) [![Downloads](https://pepy.tech/badge/mousetools)](https://pepy.tech/project/mousetools)


An unofficial Python wrapper for the Disney API. Data is pulled directly from Disney. This package supports Walt Disney World and Disneyland.

Read the [documentation](https://caratozzoloxyz.gitlab.io/public/MouseTools/).


### Installation
You can install using pip:
```bash
pip install MouseTools
```
You can also install directly from this repo in case of any changes not uploaded to Pypi.
```bash
pip install git+https://gitlab.com/caratozzoloxyz/public/MouseTools
```

### Quick Start

Define an entity object directly.

```python
from mousetools.entities import Attraction

big_thunder = Attraction("80010110")

print(big_thunder.name)
#> 'Big Thunder Mountain Railroad'

print(big_thunder.ancestor_theme_park_id)
#> '80007944'

print(big_thunder.get_status())
#> 'OPERATING'

print(big_thunder.get_wait_time())
#> 45

```

Use the already created destination objects to get children entities.

```python
from mousetools.entities import WALT_DISNEY_WORLD_DESTINATION, DISNEYLAND_RESORT_DESTINATION
from mousetools.ids import FacilityServiceEntityTypes

print(WALT_DISNEY_WORLD_DESTINATION.get_children_entity_ids(FacilityServiceEntityTypes.ENTERTAINMENT_VENUES))
#> ['10460', '80008033', '80008259']

print(DISNEYLAND_RESORT_DESTINATION.get_children_entity_ids(FacilityServiceEntityTypes.RESORT_AREAS))
#> ['330338', '15597760']
```

### License
This project is distributed under the MIT license. For more information see [LICENSE](https://gitlab.com/caratozzoloxyz/public/MouseTools/-/blob/master/LICENSE?ref_type=heads)

### Disclaimer
This project is in no way affiliated with The Walt Disney Company and all use of Disney Services is subject to the [Disney Terms of Use](https://disneytermsofuse.com/).

This package uses the [ThemeParks.wiki API](https://themeparks.wiki/). 