# Filter Persist

**Filter Persist** is a custom [Streamlit](https://streamlit.io) component that integrates [AG Grid](https://www.ag-grid.com/) and enables persistent filtering using a local JSON file.

Built with care by **Parshav Shivnani**, this component is ideal for dashboards where user filter preferences need to be retained between sessions.
With 0.1.5 version it has majority of AG-Grid builder options
## 🔧 Features

- Interactive AG Grid component for Streamlit
- Filters are saved and restored from a JSON file
- Simple to integrate in any Streamlit workflow
- No need for AG Grid enterprise modules

## 📦 Installation

Install the package from PyPI:

```bash
pip install filter-persist
```

Example using python
```
import streamlit as st
import pandas as pd
import json
from filter_persist import custom_aggrid

# Sample DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 30],
})

# Load saved filters from JSON file
try:
    with open("filter_model.json", "r") as f:
        saved_filters = json.load(f)
except FileNotFoundError:
    saved_filters = None

st.title("Filter Persist - AG Grid with JSON Persistence")

# Call the component
result = custom_aggrid(
    data=df.to_dict("records"),
    column_defs=[{"field": c} for c in df.columns],
    filter_model=saved_filters,
)

# Save current filter state to JSON file
if result:
    with open("filter_model.json", "w") as f:
        json.dump(result, f)

# Display current filters
st.subheader("Current Filter Model:")
st.json(result)
```