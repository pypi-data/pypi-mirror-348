# Spatial Transcriptomics Analysis Toolkit

This toolkit provides a comprehensive set of Python modules for analyzing spatial transcriptomics data, enabling researchers to visualize and interpret gene expression in a spatial context.

## Table of Contents
- [Overview](#overview)
- [Main Components](#main-components)
- [Spatioloji Class](#spatioloji-class)
- [Visualization Functions](#visualization-functions)
- [Spatial Analysis](#spatial-analysis)
- [Quality Control](#quality-control)
- [Usage Examples](#usage-examples)

## Overview

The Spatial Transcriptomics Analysis Toolkit is designed to handle, analyze, and visualize spatially-resolved gene expression data. It supports operations across multiple fields of view (FOVs), offers various visualization techniques, enables spatial relationship analysis, and includes robust quality control methods.

## Main Components

The toolkit consists of three main Python modules:

1. **Spatial_Object.py**: Contains the core `Spatioloji` class for data management and the `Spatioloji_qc` class for quality control.
2. **Plot_Spatial_Image.py**: Provides functions for visualizing spatial data with various plotting methods.
3. **Spatial_function.py**: Implements spatial analysis functions such as neighbor detection and interaction analysis.

## Spatioloji Class

The `Spatioloji` class is the core data structure that manages spatial transcriptomics data:

```python
from Spatial_Object import Spatioloji

# Create a Spatioloji object
spatioloji_obj = Spatioloji(
    polygons=polygons_df,          # Cell polygon coordinates
    cell_meta=cell_meta_df,        # Cell metadata
    adata=anndata_obj,             # Gene expression data (AnnData)
    fov_positions=fov_positions_df # Field of view positions
)

# Load from files
spatioloji_obj = Spatioloji.from_files(
    polygons_path="polygons.csv",
    cell_meta_path="cell_meta.csv",
    adata_path="expression.h5ad",
    fov_positions_path="fov_positions.csv",
    images_folder="images/",       # Optional: folder with FOV images
)

# Save/load using pickle
spatioloji_obj.to_pickle("spatioloji_data.pkl")
loaded_obj = Spatioloji.from_pickle("spatioloji_data.pkl")
```

Key attributes:
- **polygons**: DataFrame with cell polygon vertex coordinates in local and global space
- **cell_meta**: DataFrame with cell metadata, including cell centers and properties
- **adata**: AnnData object containing gene expression data
- **fov_positions**: DataFrame with global coordinates of FOVs
- **images**: Dictionary mapping FOV IDs to image arrays
- **custom**: Dictionary for any user-defined additional data

## Visualization Functions

The `Plot_Spatial_Image.py` module offers multiple visualization approaches:

### 1. FOV Image Stitching

```python
from Plot_Spatial_Image import stitch_fov_images

# Create a stitched image of multiple FOVs
stitched_obj = stitch_fov_images(
    spatioloji_obj,
    fov_ids=["1", "2", "3"],  # Optional: specific FOVs to include
    flip_vertical=True,       # Whether to flip images vertically
    save_path="stitched.png", # Path to save the image
    show_plot=True            # Whether to display the plot
)
```

### 2. Global Visualization by Feature Values

```python
from Plot_Spatial_Image import plot_global_polygon_by_features

# Plot cell polygons colored by a continuous feature
plot_global_polygon_by_features(
    spatioloji_obj,
    feature="Gene_X",               # Feature to visualize (e.g., gene name)
    background_img=True,            # Show stitched image in background
    colormap="viridis",             # Matplotlib colormap
    save_dir="./figures/"           # Directory to save output
)

# Plot cell dots colored by a continuous feature
plot_global_dot_by_features(
    spatioloji_obj,
    feature="Gene_X",               
    background_img=True,
    dot_size=20,                   # Size of dots
    colormap="viridis"             
)
```

### 3. Categorical Visualization

```python
from Plot_Spatial_Image import plot_global_polygon_by_categorical

# Plot cell polygons colored by categorical data (e.g., cell types)
plot_global_polygon_by_categorical(
    spatioloji_obj,
    feature="cell_type",           # Column with categorical values
    background_img=True,
    color_map=None,                # None for auto-assignment or provide dict
    edge_color="black",
    alpha=0.8                      # Transparency
)

# Plot cell dots colored by categorical data
plot_global_dot_by_categorical(
    spatioloji_obj,
    feature="cell_type",
    dot_size=20,
    background_img=True
)
```

### 4. FOV-level Visualizations

```python
from Plot_Spatial_Image import plot_local_polygon_by_features, plot_local_dots_by_categorical

# Plot multiple FOVs with continuous feature coloring
plot_local_polygon_by_features(
    spatioloji_obj,
    feature="Gene_X",
    fov_ids=["1", "2", "3", "4"],   # FOVs to visualize
    background_img=True,
    grid_layout=(2, 2)              # Optional layout as (rows, columns)
)

# Plot multiple FOVs with categorical coloring
plot_local_dots_by_categorical(
    spatioloji_obj,
    feature="cell_type",
    fov_ids=["1", "2", "3", "4"],
    background_img=True
)
```

## Spatial Analysis

The `Spatial_function.py` module enables analysis of spatial relationships between cells:

```python
from Spatial_function import perform_neighbor_analysis

# Analyze cell neighborhood relationships
results = perform_neighbor_analysis(
    polygon_file=spatioloji_obj.polygons,
    cell_metadata=spatioloji_obj.cell_meta,
    cell_type_column="cell_type",    # Column defining cell types
    distance_threshold=0.0,          # 0.0 means cells must be touching
    save_dir="./analysis/",          # Directory to save results
    include_plots=True               # Generate visualization plots
)
```

This analysis produces several outputs:
- Cell-cell interaction pairs
- Cell type interaction counts and statistics
- Interaction enrichment scores (observed/expected ratios)
- Visualizations including heatmaps and network graphs

## Quality Control

The `Spatioloji_qc` class in `Spatial_Object.py` provides quality control functionality:

```python
from Spatial_Object import Spatioloji_qc

# Initialize QC object
qc = Spatioloji_qc(
    expr_matrix=expr_df,         # Expression matrix
    cell_metadata=metadata_df,   # Cell metadata
    output_dir="./qc_output/"    # Output directory
)

# Run complete QC pipeline
filtered_cells, filtered_genes = qc.run_qc_pipeline()

# Or run individual QC steps
qc.prepare_anndata()
qc.qc_negative_probes()
qc.qc_cell_area()
qc.qc_cell_metrics()
qc.qc_fov_metrics()
filtered_cells = qc.filter_cells()
filtered_genes = qc.filter_genes()
```

The QC pipeline includes:
- Negative probe analysis (background signal control)
- Cell area and morphology assessment
- Cell-level metrics (counts, mitochondrial genes, etc.)
- FOV-level metrics comparisons
- Cell and gene filtering based on quality thresholds

## Usage Examples

### Complete Workflow

```python
import scanpy as sc
import pandas as pd
from Spatial_Object import Spatioloji
from Plot_Spatial_Image import stitch_fov_images, plot_global_polygon_by_categorical
from Spatial_function import perform_neighbor_analysis

# 1. Load data
spatioloji_obj = Spatioloji.from_files(
    polygons_path="polygons.csv",
    cell_meta_path="cell_meta.csv",
    adata_path="expression.h5ad",
    fov_positions_path="fov_positions.csv",
    images_folder="images/"
)

# 2. Create stitched image of all FOVs
stitched_obj = stitch_fov_images(
    spatioloji_obj,
    save_path="stitched_image.png"
)

# 3. Visualize cell types across the tissue
plot_global_polygon_by_categorical(
    stitched_obj,
    feature="cell_type",
    background_img=True,
    save_dir="./figures/"
)

# 4. Analyze cell-cell interactions
interaction_results = perform_neighbor_analysis(
    polygon_file=stitched_obj.polygons,
    cell_metadata=stitched_obj.cell_meta,
    cell_type_column="cell_type",
    save_dir="./analysis/"
)

# 5. Access and use the results
enrichment_df = interaction_results['enrichment_df']
print("Top cell-cell interactions:")
print(enrichment_df.unstack().sort_values(ascending=False).head(10))
```

This toolkit enables comprehensive spatial transcriptomics analysis, from data management and visualization to sophisticated spatial relationship investigations.
I will continue to add more features to it.
