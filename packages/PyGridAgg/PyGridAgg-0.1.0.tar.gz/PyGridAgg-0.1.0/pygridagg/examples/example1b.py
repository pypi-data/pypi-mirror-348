import matplotlib.pyplot as plt

import pygridagg as pga
from pygridagg.examples import load_japanese_earthquake_data

# Load example data on earthquakes around Japan
quake_coords, magnitudes = load_japanese_earthquake_data()

# Define a square grid layout with 10k cells. The `from_points`
# constructor adjusts grid bounds to encompass all earthquake locations.
layout = pga.SquareGridLayout.from_points(quake_coords, num_cells=100**2)

# Count earthquakes across grid cells
agg_counts = pga.CountAggregator(layout, quake_coords)

# Show a heatmap
agg_counts.plot(title="Earthquakes around Japan (2010-2023)")
plt.show()