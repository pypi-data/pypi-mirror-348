# ⛔ Exceptions

### [`prohibit_negative_values`][utilsx.prohibit_negative_values]

Suppose you process a list of daily sales amounts
that must never contain negative values, as they represent revenue:

``` py title="manual.py" hl_lines="5-6"
# Daily sales data
sales = [1200.0, 1500.5, -300.0, 1100.0]

# Manual check for negatives
if any(sale < 0 for sale in sales):
    raise ValueError("Sales data contains negative values")
```

This check remains straightforward but forces you to repeat the same pattern
wherever you enforce non-negativity, cluttering your code.

Use UtilsX to make this validation clear and reusable:

``` py title="with_utilsx.py" hl_lines="1 6"
from utilsx import prohibit_negative_values

# Daily sales data
sales = [1200.0, 1500.5, -300.0, 1100.0]

prohibit_negative_values(sales)
```

With `prohibit_negative_values`, you express your intent directly,
improving readability and reducing boilerplate in data validation steps.

### [`raise_key_error_with_suggestions`][utilsx.raise_key_error_with_suggestions]

Suppose you look up car models in a catalog and want to provide helpful feedback
when a user queries a missing model, suggesting alternatives to reduce frustration:

``` py title="plain_key_error.py" hl_lines="9 13"
car_catalog = {
    "Toyota": ["Camry", "Corolla", "Prius"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Ford": ["F-150", "Mustang", "Explorer"],
}

def get_car_models(brand):
    if brand not in car_catalog:
        raise KeyError(f"Car brand {brand} not found.")
    return car_catalog[brand]

get_car_models("Toyta")
# KeyError: Car brand Toyta not found.
```

The error message provides no guidance or suggestions,
leaving users to guess correct brand names and slowing down debugging or user input.

Use UtilsX to enhance your error reporting:

``` py title="key_error_with_suggestion.py" hl_lines="1 11-16 20-21"
from utilsx import raise_key_error_with_suggestions

car_catalog = {
    "Toyota": ["Camry", "Corolla", "Prius"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Ford": ["F-150", "Mustang", "Explorer"],
}

def get_car_models(brand):
    if brand not in car_catalog:
        raise_key_error_with_suggestions(
            attempted_key=brand,
            existing_keys=car_catalog.keys(),
            object_name="car brand",
            attribute_name="name",
        )
    return car_catalog[brand]

get_car_models("Toyta")
# KeyError: Car brand with name Toyta not found.
# Did you mean one of these instead: Toyota, Honda?
```

`raise_key_error_with_suggestions` improves user experience by offering actionable hints,
helping users correct typos or misunderstandings quickly.
