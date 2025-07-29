<p align="center">
  <img src="https://raw.githubusercontent.com/Ahghaffari/stm_graph/master/images/STM-Graph-logo.svg" alt="STM-Graph Logo" width="400">
</p>

# STM-Graph: Spatial-Temporal Mapping for Graph Neural Networks Predictions

STM-Graph is a Python framework for analyzing spatial-temporal urban data and doing predictions using Graph Neural Networks. It provides a complete end-to-end pipeline from raw event data to trained GNN models, making it easier to understand and predict urban events.

## Key Features

- **Complete Pipeline**: From raw data to trained models in a unified framework
- **Flexible Spatial Mapping**: Grid-based, Voronoi, or administrative boundary mapping
- **Urban Knowledge Graph**: Extract features from OpenStreetMap for urban context
- **Multiple GNN Models**: Support for various state-of-the-art graph neural networks
- **Visualization Tools**: Comprehensive spatial and temporal visualizations
- **Integration**: Weights & Biases integration for experiment tracking

## Installation

### From PyPI

```bash
# First install the base package
pip install stm-gnn

# Then install PyTorch with CUDA
pip install torch==2.4.0 --extra-index-url https://download.pytorch.org/whl/cu118

# Finally install the PyTorch extensions
pip install stm-gnn[torch-extensions]
```
### From Source

```bash
# Clone the repository
git clone https://github.com/Ahghaffari/stm_graph.git
cd stm_graph

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
import stm_graph

# 1. Preprocess your data
gdf = stm_graph.preprocess_dataset(
    data_path="data/",
    dataset="events.csv",
    time_col="timestamp",
    lat_col="latitude",
    lng_col="longitude"
)

# 2. Create spatial mapping
mapper = stm_graph.GridMapping(cell_size=1000.0)
district_gdf, point_to_partition = mapper.create_mapping(gdf)

# 3. Extract urban features
osm_features = stm_graph.extract_osm_features(
    regions_gdf=district_gdf,
    feature_types=['poi', 'road', 'junction']
)

# 4. Build graph representation
graph_data = stm_graph.build_graph_and_augment(
    grid_gdf=district_gdf,
    points_gdf=gdf,
    point_to_cell=point_to_partition,
    static_features=osm_features
)

# 5. Create temporal dataset
temporal_dataset, _, _ = stm_graph.create_temporal_dataset(
    edge_index=graph_data["edge_index"],
    augmented_df=graph_data["augmented_df"],
    node_ids=graph_data["node_ids"],
    static_features=osm_features,
    time_col="timestamp",
    bin_type="daily"
)

# 6. Train a model
model = stm_graph.create_model("stgcn", task="classification")
results = stm_graph.train_model(
    model=model,
    dataset=temporal_dataset,
    task="classification"
)
```

## Example Notebooks

The repository includes two example notebooks in the `examples/` folder that demonstrate the complete workflow:

1. **NYC 311 Service Request Analysis** (`examples/nyc_311_example.ipynb`): Analyzing and predicting 311 service requests across New York City
2. **NYC Traffic Crash Analysis** (`examples/nyc_crash_example.ipynb`): Analyzing and predicting traffic crashes across New York City

These notebooks showcase the complete workflow from data preprocessing to model training and visualization. They are excellent starting points to understand how to use the STM-Graph framework with real-world datasets.

## Framework Components

### 1. Data Preprocessing

Load and preprocess spatial-temporal data:

```python
gdf = stm_graph.preprocess_dataset(
    data_path="data",
    dataset="events.csv",
    time_col="timestamp",
    lat_col="latitude",
    lng_col="longitude",
    filter_dates=("2020-01-01", "2020-12-31")
)
```

### 2. Spatial Mapping

Divide the area into spatial regions:

```python
# Grid-based mapping
mapper = stm_graph.GridMapping(cell_size=1000.0)
district_gdf, point_to_partition = mapper.create_mapping(gdf)

# Voronoi-based mapping
mapper = stm_graph.VoronoiDegreeMapping()
district_gdf, point_to_partition = mapper.create_mapping(gdf)

# Administrative boundary mapping
mapper = stm_graph.AdministrativeMapping(districts_file="districts.shp")
district_gdf, point_to_partition = mapper.create_mapping(gdf)
```

### 3. Feature Extraction

Extract urban features from OpenStreetMap:

```python
osm_features = stm_graph.extract_osm_features(
    regions_gdf=district_gdf,
    feature_types=['poi', 'road', 'junction'],
    normalize=True
)
```

### 4. Graph Construction

Build a graph representation:

```python
graph_data = stm_graph.build_graph_and_augment(
    grid_gdf=district_gdf,
    points_gdf=gdf,
    point_to_cell=point_to_partition,
    static_features=osm_features
)
```

### 5. Temporal Dataset Creation

Create a temporal dataset for model training:

```python
temporal_dataset, _, _ = stm_graph.create_temporal_dataset(
    edge_index=graph_data["edge_index"],
    augmented_df=graph_data["augmented_df"],
    node_ids=graph_data["node_ids"],
    static_features=osm_features,
    time_col="timestamp",
    bin_type="daily",
    history_window=3,
    task="classification"
)
```

### 6. Visualization

Visualize spatial and temporal patterns:

```python
# Plot time series
stm_graph.plot_node_time_series(
    temporal_dataset,
    num_nodes=5,
    selection_method="highest_activity"
)

# Plot spatial network
stm_graph.plot_spatial_network(
    regions_gdf=district_gdf,
    edge_index=graph_data["edge_index"],
    node_values=node_counts,
    node_ids=graph_data["node_ids"]
)

# Plot temporal heatmap
stm_graph.plot_temporal_heatmap(
    temporal_dataset,
    max_timesteps=168
)
```

### 7. Model Training

Train a GNN model:

```python
# Create a model
model = stm_graph.create_model(
    model_name="stgcn",
    task="classification"
)

# Train the model
results = stm_graph.train_model(
    model=model,
    dataset=temporal_dataset,
    task="classification",
    num_epochs=100,
    learning_rate=0.001
)
```
## Contributing
Contributions to STM-Graph are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use STM-Graph in your research, please cite the repo and our article:

```
@software{stm_graph,
  author = {Amirhossein Ghaffari},
  title = {STM-Graph: Spatial-Temporal Modeling with Graph Neural Networks Predictions},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Ahghaffari/stm_graph}
}
```

## Acknowledgments

- PyTorch Geometric Temporal
- OSMnx
- Weights & Biases
- NetworkX
