import geopandas as gpd

def get_hcmc_graph_from_geojson(geojson_path='hcmc_districts.geojson'):
    """
    Loads the GeoJSON, computes adjacencies using spatial touches/intersects,
    and returns variables, domains, and neighbors dictionary.
    """
    # Load GeoDataFrame
    gdf = gpd.read_file(geojson_path)
    
    variables = gdf['name'].tolist()
    
    # Initialize domains: 4 colors are usually enough
    num_colors = 4
    domains = {var: list(range(num_colors)) for var in variables}
    
    # Compute adjacency (neighbors)
    neighbors = {var: [] for var in variables}
    
    # We use a spatial join or manual intersection check
    for i, row_i in gdf.iterrows():
        var_i = row_i['name']
        geom_i = row_i['geometry']
        
        for j, row_j in gdf.iterrows():
            if i >= j:
                continue
            var_j = row_j['name']
            geom_j = row_j['geometry']
            
            # Check if they touch or intersect
            if geom_i.touches(geom_j) or geom_i.intersects(geom_j):
                # Extra check to ignore point touches if needed, but intersects is safe
                # We can refine using the intersection length if necessary
                intersection = geom_i.intersection(geom_j)
                if intersection.geom_type in ['LineString', 'MultiLineString', 'Polygon', 'MultiPolygon']:
                    neighbors[var_i].append(var_j)
                    neighbors[var_j].append(var_i)
                elif intersection.length > 0: # Sometimes boundaries overlap slightly
                    neighbors[var_i].append(var_j)
                    neighbors[var_j].append(var_i)

    return variables, domains, neighbors, gdf
