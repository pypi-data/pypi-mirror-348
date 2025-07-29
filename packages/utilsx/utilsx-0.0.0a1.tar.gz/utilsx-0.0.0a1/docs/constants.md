# 🪨 Constants

A module with common real-world constants.

## Numbers

Commonly used literal numbers:

- `THOUSAND`
- `MILLION`
- `BILLION`
- `TRILLION`

Besides helping avoid duplication of
[magic numbers](https://code-basics.com/languages/python/lessons/magic-numbers) in your code,
using these constants protects from typos involving missing / extra `0` in magic numbers.

Example:

``` py title="bad_practice.py"
revenue = 2819920021

# The number below has a missing zero - how long would it take for you to spot?
revenue_billions = revenue / 100000000
```

Do instead:

``` py title="good_practice.py"
from utilsx import BILLION

revenue = 2819920021
revenue_billions = revenue / BILLION
```

!!! tip "Constants like `pi`, `e` are available in built-in `math` module"

    See full list [here](https://docs.python.org/3/library/math.html#constants).
    UtilsX does not re-define them, and encourages you to import them from `math`.

## Physics

UtilsX provides a few constants representing common mass and volume ratios.

Similar to numeric constraints, this set fights against duplicated magic numbers in codebases.

But in addition to that, inconsistency here directly makes calculations imprecise:

``` py title="bad_practice.py" hl_lines="3 7"
# Work of one developer
production_kg = 500
production_lbs = production_kg * 2.205

# Work of another developer
consumption_lbs = 1000
consumption_kg = consumption_lbs * (1 / 2.20462)
```

Clearly, a conversion ratio should not be `2.205` in one part of the codebase, and `2.20462` in another.

Do this instead:

``` py title="good_practice.py"
from utilsx import LBS_IN_KG, KG_IN_LBS

# Work of one developer
production_kg = 500
production_lbs = production_kg * LBS_IN_KG

# Work of another developer
consumption_lbs = 1000
consumption_kg = consumption_lbs * KG_IN_LBS
```

You may alternatively use [SciPy's `constants` module](https://docs.scipy.org/doc/scipy/reference/constants.html#).
In fact, for deep scientific projects, likely it would be more suitable.

UtilsX, however:

- More lightweight: does not bring whole SciPy (and NumPy as its transitive dependency) to your venv.
- Uses more explicit names: e.g., `KG_IN_LBS` vs `pound` in SciPy.
- Defines constants missing in SciPy: like `OZ_IN_GAL`, while SciPy only provides gallon-to-cubic-meter ratios.

## Time

Constants like:

- `SECONDS_IN_MINUTE`
- `MINUTES_IN_DAY`
- `HOURS_IN_YEAR`
- ... and others, following the same naming semantics

While the [numeric](#numbers) constants mostly help prevent typos,
and [physics](#physics) ones help achieve precision and consistency,
the biggest benefit of the **time** group is readability.

Consider:

``` py title="bad_practice.py"
# What does this conversion do: hours to minutes or minutes to seconds?
data["revenue"] /= 60
```

Do instead:

``` py title="good_practice.py"
from utilsx import MINUTES_IN_HOUR

data["revenue"] /= MINUTES_IN_HOUR
```
