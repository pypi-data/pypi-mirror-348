import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Polygon as sPolygon
from typing import List, Dict, Optional, Tuple, Union
from tqdm import tqdm
import networkx as nx
from scipy.spatial import Voronoi
from collections import defaultdict

def perform_neighbor_analysis(
    polygon_file: pd.DataFrame,
    cell_metadata: pd.DataFrame,
    cell_type_column: str,
    distance_threshold: float = 0.0,
    save_dir: str = "./",
    filename_prefix: str = "neighbor_analysis",
    include_plots: bool = True,
    figsize: Tuple[int, int] = (10, 8),
    dpi: int = 300,
    return_data: bool = True,
    verbose: bool = True
) -> Dict:
    """
    Perform comprehensive neighbor distance analysis for cell polygons.
    
    Parameters
    ----------
    polygon_file : pd.DataFrame
        DataFrame with cell polygon vertices. Must include 'cell', 'x_local_px', 'y_local_px' columns.
    cell_metadata : pd.DataFrame
        DataFrame with cell metadata. Must include 'cell' and cell_type_column.
    cell_type_column : str
        Column in cell_metadata that defines cell types for analysis.
    distance_threshold : float, optional
        Maximum distance between polygons to be considered neighbors, by default 0.0
        (0.0 means polygons must be touching, positive values include nearby non-touching cells)
    save_dir : str, optional
        Directory to save result files, by default "./"
    filename_prefix : str, optional
        Prefix for output filenames, by default "neighbor_analysis"
    include_plots : bool, optional
        Whether to generate and save plots, by default True
    figsize : Tuple[int, int], optional
        Figure size for plots, by default (10, 8)
    dpi : int, optional
        DPI for saved figures, by default 300
    return_data : bool, optional
        Whether to return the analysis data, by default True
    verbose : bool, optional
        Whether to display progress information, by default True
    
    Returns
    -------
    Dict
        Dictionary containing analysis results if return_data is True
    """
    # Check required columns
    poly_required_cols = ['cell', 'x_local_px', 'y_local_px']
    poly_missing_cols = [col for col in poly_required_cols if col not in polygon_file.columns]
    if poly_missing_cols:
        raise ValueError(f"Missing required columns in polygon_file: {poly_missing_cols}")
    
    meta_required_cols = ['cell', cell_type_column]
    meta_missing_cols = [col for col in meta_required_cols if col not in cell_metadata.columns]
    if meta_missing_cols:
        raise ValueError(f"Missing required columns in cell_metadata: {meta_missing_cols}")
    
    # Create output directory
    os.makedirs(save_dir, exist_ok=True)
    
    # Convert polygons to Shapely objects
    if verbose:
        print("Converting cell polygons to Shapely objects...")
    
    polygon_set = []
    cell_ids = []
    
    for cell, group in tqdm(polygon_file.groupby('cell'), disable=not verbose):
        try:
            # Create polygon from vertices
            coords = group[['x_local_px', 'y_local_px']].values
            
            # Skip cells with fewer than 3 vertices
            if len(coords) < 3:
                if verbose:
                    print(f"Warning: Cell {cell} has fewer than 3 vertices. Skipping.")
                continue
                
            # Create Shapely polygon
            polygon_tmp = sPolygon([(x, y) for x, y in coords])
            
            # Skip invalid polygons
            if not polygon_tmp.is_valid:
                if verbose:
                    print(f"Warning: Cell {cell} has an invalid polygon. Skipping.")
                # Could try to fix: polygon_tmp = polygon_tmp.buffer(0)
                continue
                
            polygon_set.append(polygon_tmp)
            cell_ids.append(cell)
        except Exception as e:
            if verbose:
                print(f"Error processing cell {cell}: {e}")
    
    # Create mapping from cell IDs to their positions in the list
    cell_to_index = {cell_id: idx for idx, cell_id in enumerate(cell_ids)}
    
    # Get cell types
    cell_meta_dict = dict(zip(cell_metadata['cell'], cell_metadata[cell_type_column]))
    
    # Get cell types for each polygon
    cell_types = []
    for cell_id in cell_ids:
        if cell_id in cell_meta_dict:
            cell_types.append(cell_meta_dict[cell_id])
        else:
            if verbose:
                print(f"Warning: Cell {cell_id} not found in metadata. Assigning 'Unknown'.")
            cell_types.append("Unknown")
    
    # Get unique cell types
    unique_cell_types = sorted(set(cell_types))
    
    # Find neighboring cells
    if verbose:
        print("Finding neighboring cells...")
    
    neighbor_pairs = []
    neighbor_distances = []
    
    # Use tqdm for progress tracking
    total_comparisons = len(polygon_set) * (len(polygon_set) - 1) // 2
    progress_bar = tqdm(total=total_comparisons, disable=not verbose)
    
    for i in range(len(polygon_set)):
        for j in range(i+1, len(polygon_set)):
            progress_bar.update(1)
            poly1 = polygon_set[i]
            poly2 = polygon_set[j]
            
            # Check if polygons are neighbors
            distance = poly1.distance(poly2)
            if distance <= distance_threshold:
                neighbor_pairs.append((cell_ids[i], cell_ids[j]))
                neighbor_distances.append(distance)
    
    progress_bar.close()
    
    # Create neighbor dataframe
    neighbor_df = pd.DataFrame({
        'cell1': [pair[0] for pair in neighbor_pairs],
        'cell2': [pair[1] for pair in neighbor_pairs],
        'distance': neighbor_distances
    })
    
    # Add cell types
    neighbor_df['cell1_type'] = neighbor_df['cell1'].map(cell_meta_dict)
    neighbor_df['cell2_type'] = neighbor_df['cell2'].map(cell_meta_dict)
    
    # Save neighbor data
    neighbor_df.to_csv(os.path.join(save_dir, f"{filename_prefix}_pairs.csv"), index=False)
    
    # Create a network graph
    if verbose:
        print("Creating cell interaction network...")
    
    G = nx.Graph()
    
    # Add nodes with cell type attributes
    for i, cell_id in enumerate(cell_ids):
        G.add_node(cell_id, cell_type=cell_types[i])
    
    # Add edges with distance attributes
    for _, row in neighbor_df.iterrows():
        G.add_edge(row['cell1'], row['cell2'], distance=row['distance'])
    
    # Compute interaction counts between cell types
    interaction_counts = defaultdict(int)
    interaction_distances = defaultdict(list)
    
    for _, row in neighbor_df.iterrows():
        type_pair = tuple(sorted([row['cell1_type'], row['cell2_type']]))
        interaction_counts[type_pair] += 1
        interaction_distances[type_pair].append(row['distance'])
    
    # Create interaction matrix
    interaction_matrix = np.zeros((len(unique_cell_types), len(unique_cell_types)))
    avg_distance_matrix = np.zeros((len(unique_cell_types), len(unique_cell_types)))
    
    for i, type1 in enumerate(unique_cell_types):
        for j, type2 in enumerate(unique_cell_types):
            type_pair = tuple(sorted([type1, type2]))
            interaction_matrix[i, j] = interaction_counts[type_pair]
            avg_distance_matrix[i, j] = np.mean(interaction_distances[type_pair]) if interaction_distances[type_pair] else np.nan
    
    # Make sure diagonal reflects interactions within same cell type
    for i, cell_type in enumerate(unique_cell_types):
        same_type_pair = (cell_type, cell_type)
        interaction_matrix[i, i] = interaction_counts[same_type_pair]
        avg_distance_matrix[i, i] = np.mean(interaction_distances[same_type_pair]) if interaction_distances[same_type_pair] else np.nan
    
    # Store interaction data
    interaction_df = pd.DataFrame(interaction_matrix, index=unique_cell_types, columns=unique_cell_types)
    avg_distance_df = pd.DataFrame(avg_distance_matrix, index=unique_cell_types, columns=unique_cell_types)
    
    # Save interaction data
    interaction_df.to_csv(os.path.join(save_dir, f"{filename_prefix}_interaction_counts.csv"))
    avg_distance_df.to_csv(os.path.join(save_dir, f"{filename_prefix}_avg_distances.csv"))
    
    # Compute statistics for each cell
    cell_stats = {}
    
    for cell_id in cell_ids:
        neighbors = list(G.neighbors(cell_id))
        neighbor_types = [G.nodes[n]['cell_type'] for n in neighbors]
        type_counts = {cell_type: neighbor_types.count(cell_type) for cell_type in unique_cell_types}
        
        cell_stats[cell_id] = {
            'degree': len(neighbors),
            'cell_type': G.nodes[cell_id]['cell_type'],
            **{f'neighbor_{ct}_count': count for ct, count in type_counts.items()}
        }
    
    cell_stats_df = pd.DataFrame.from_dict(cell_stats, orient='index')
    cell_stats_df.index.name = 'cell'
    cell_stats_df.reset_index(inplace=True)
    
    # Save cell statistics
    cell_stats_df.to_csv(os.path.join(save_dir, f"{filename_prefix}_cell_stats.csv"), index=False)
    
    # Calculate enrichment scores (observed/expected ratios)
    cell_type_counts = {cell_type: cell_types.count(cell_type) for cell_type in unique_cell_types}
    total_cells = len(cell_ids)
    
    enrichment_matrix = np.zeros((len(unique_cell_types), len(unique_cell_types)))
    
    for i, type1 in enumerate(unique_cell_types):
        for j, type2 in enumerate(unique_cell_types):
            # Calculate expected interactions based on frequency
            if type1 == type2:
                expected = (cell_type_counts[type1] * (cell_type_counts[type1] - 1)) / 2
            else:
                expected = cell_type_counts[type1] * cell_type_counts[type2]
            
            # Scale by total possible interactions
            total_possible = (total_cells * (total_cells - 1)) / 2
            expected = expected / total_possible * sum(interaction_counts.values())
            
            # Calculate enrichment (observed/expected)
            observed = interaction_matrix[i, j]
            enrichment = observed / expected if expected > 0 else np.nan
            enrichment_matrix[i, j] = enrichment
    
    # Store enrichment data
    enrichment_df = pd.DataFrame(enrichment_matrix, index=unique_cell_types, columns=unique_cell_types)
    
    # Save enrichment data
    enrichment_df.to_csv(os.path.join(save_dir, f"{filename_prefix}_enrichment.csv"))
    
    # Generate plots if requested
    if include_plots:
        if verbose:
            print("Generating plots...")
            
        # Interaction heatmap
        plt.figure(figsize=figsize)
        sns.heatmap(interaction_df, annot=True, cmap="YlGnBu", fmt=".0f")
        plt.title("Cell Type Interaction Counts")
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f"{filename_prefix}_interaction_heatmap.png"), dpi=dpi)
        plt.close()
        
        # Average distance heatmap
        plt.figure(figsize=figsize)
        sns.heatmap(avg_distance_df, annot=True, cmap="YlGnBu", fmt=".2f")
        plt.title("Average Distance Between Cell Types")
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f"{filename_prefix}_distance_heatmap.png"), dpi=dpi)
        plt.close()
        
        # Enrichment heatmap
        plt.figure(figsize=figsize)
        sns.heatmap(enrichment_df, annot=True, cmap="coolwarm", center=1.0, fmt=".2f")
        plt.title("Cell Type Interaction Enrichment (Observed/Expected)")
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f"{filename_prefix}_enrichment_heatmap.png"), dpi=dpi)
        plt.close()
        
        # Degree distribution by cell type
        plt.figure(figsize=figsize)
        sns.boxplot(x=cell_stats_df['cell_type'], y=cell_stats_df['degree'])
        plt.title("Number of Neighbors by Cell Type")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f"{filename_prefix}_degree_boxplot.png"), dpi=dpi)
        plt.close()
        
        # Network visualization (if fewer than 1000 cells for clarity)
        if len(cell_ids) < 1000:
            plt.figure(figsize=(12, 12))
            
            # Use spring layout for positioning
            pos = nx.spring_layout(G)
            
            # Create a color map for cell types
            color_map = {ct: plt.cm.tab10(i % 10) for i, ct in enumerate(unique_cell_types)}
            node_colors = [color_map[G.nodes[node]['cell_type']] for node in G.nodes()]
            
            # Draw nodes and edges
            nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors, alpha=0.8)
            nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.3)
            
            # Add a legend
            for i, ct in enumerate(unique_cell_types):
                plt.scatter([], [], color=color_map[ct], label=ct)
            plt.legend()
            
            plt.title("Cell Interaction Network")
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(os.path.join(save_dir, f"{filename_prefix}_network.png"), dpi=dpi)
            plt.close()
    
    # Prepare return data
    if return_data:
        return {
            'neighbor_df': neighbor_df,
            'interaction_df': interaction_df,
            'avg_distance_df': avg_distance_df,
            'enrichment_df': enrichment_df,
            'cell_stats_df': cell_stats_df,
            'network': G,
            'polygons': {cell_ids[i]: polygon_set[i] for i in range(len(cell_ids))}
        }
    else:
        return None