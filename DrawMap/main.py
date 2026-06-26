import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import matplotlib.pyplot as plt
import copy
import textwrap
from matplotlib.widgets import Button, RadioButtons
from geo_map import get_hcmc_graph_from_geojson
from Backtracking import CSP as CSP_BT
from ForwardChecking import CSP as CSP_FC

# Colors for mapping (Domain)
COLORS = ["#ff9999", "#99ccff", "#99ff99", "#ffcc99", "#cc99ff", "#ffff99"]
COLOR_NAMES = ["Đỏ nhạt", "Xanh lam", "Xanh lá", "Cam", "Tím", "Vàng"]

def main():
    logs = []

    # Clear old log file
    with open("log_quatrinh.txt", "w", encoding="utf-8") as f:
        f.write("BẮT ĐẦU CHẠY THUẬT TOÁN TÔ MÀU BẢN ĐỒ\n" + "="*50 + "\n")
        
    plt.ion() # Interactive mode on for animation
    fig, (ax_log, ax_map) = plt.subplots(1, 2, figsize=(18, 9), gridspec_kw={'width_ratios': [1, 2.2]})
    plt.subplots_adjust(bottom=0.15)
    fig.canvas.manager.set_window_title("HCMC Map Coloring CSP - Detailed Polygons")
    
    ax_log.set_axis_off()
    # Use Consolas or Arial to support Vietnamese characters properly
    log_text_obj = ax_log.text(0.02, 0.98, "", transform=ax_log.transAxes, verticalalignment='top', fontsize=9, family='Consolas')

    state = {
        'all_logs': [],
        'view_lines': 45,
        'scroll_offset': 0, # 0 = bottom, >0 = scrolled up
        'auto_scroll': True
    }

    def update_log_display():
        n = len(state['all_logs'])
        start_idx = max(0, n - state['view_lines'] - state['scroll_offset'])
        end_idx = start_idx + state['view_lines']
        visible = state['all_logs'][start_idx:end_idx]
        log_text_obj.set_text("\n".join(visible))
        fig.canvas.draw_idle()
        fig.canvas.flush_events()

    def on_scroll(event):
        if event.button == 'up':
            state['scroll_offset'] += 3
        elif event.button == 'down':
            state['scroll_offset'] -= 3

        _enforce_scroll_bounds()

    def on_key(event):
        if event.key == 'up':
            state['scroll_offset'] += 1
        elif event.key == 'down':
            state['scroll_offset'] -= 1
        elif event.key == 'pageup':
            state['scroll_offset'] += state['view_lines']
        elif event.key == 'pagedown':
            state['scroll_offset'] -= state['view_lines']
        else:
            return
            
        _enforce_scroll_bounds()
        
    def _enforce_scroll_bounds():
        max_offset = max(0, len(state['all_logs']) - state['view_lines'])
        if state['scroll_offset'] > max_offset:
            state['scroll_offset'] = max_offset
            
        if state['scroll_offset'] <= 0:
            state['scroll_offset'] = 0
            state['auto_scroll'] = True
        else:
            state['auto_scroll'] = False
            
        update_log_display()

    fig.canvas.mpl_connect('scroll_event', on_scroll)
    fig.canvas.mpl_connect('key_press_event', on_key)

    def log_message(msg):
        print(msg, flush=True)
        with open("log_quatrinh.txt", "a", encoding="utf-8") as f:
            f.write(str(msg) + "\n")
            
        for line in str(msg).split('\n'):
            # Wrap lines so they don't spill over to the map (limit to ~60 chars)
            wrapped_lines = textwrap.wrap(line, width=65)
            if not wrapped_lines:
                state['all_logs'].append("")
            for wl in wrapped_lines:
                state['all_logs'].append(wl)
        
        if state['auto_scroll']:
            state['scroll_offset'] = 0
            
        update_log_display()

    log_message("Loading geographic data and computing adjacencies...")
    variables, domains, neighbors, gdf = get_hcmc_graph_from_geojson('hcmc_districts.geojson')
    log_message(f"Loaded {len(variables)} districts.")

    def draw_graph(assignment, current_var, current_domains):
        """Callback function to animate geographic polygons at each step"""
        ax_map.clear()
        
        # Add a column for color
        gdf['color'] = "#e0e0e0" # Light gray default
        
        for idx, row in gdf.iterrows():
            name = row['name']
            if name in assignment:
                gdf.at[idx, 'color'] = COLORS[assignment[name]]
            
            # Draw highlight for current var
            if name == current_var:
                gdf.at[idx, 'color'] = "#ff3333" # Red highlight when evaluating
                
        # Plot all geometries
        gdf.plot(ax=ax_map, color=gdf['color'], edgecolor='white', linewidth=0.8)
        
        # Add labels at centroid
        for idx, row in gdf.iterrows():
            centroid = row['geometry'].centroid
            ax_map.text(centroid.x, centroid.y, row['name'], fontsize=8, ha='center', va='center', fontweight='bold', color='#333333')

        # Add info text
        info_text = f"Assignments: {csp.assignments} | Backtracks: {csp.backtracks}\n"
        if current_var:
            info_text += f"Evaluating: {current_var}\n"
        ax_map.set_title("CSP Map Coloring: HCMC Districts", fontsize=16, fontweight='bold')
        ax_map.text(0.02, 0.98, info_text, transform=ax_map.transAxes, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax_map.set_axis_off() # Hide lat/lon axes for cleaner look
        
        # Don't pause if the figure is closed
        if not plt.fignum_exists(fig.number):
            return
            
        plt.pause(0.5) # Dừng lâu hơn một chút (0.5s) để dễ đọc log
        
        while app_state['paused'] and plt.fignum_exists(fig.number):
            plt.pause(0.1)
            if app_state['reset']:
                break
                
        if app_state['reset']:
            raise ResetInterrupt()

    # Application Control State
    app_state = {
        'paused': True,
        'reset': False,
        'algorithm': 'Backtracking'
    }

    def start_cb(event):
        app_state['paused'] = False

    def stop_cb(event):
        app_state['paused'] = True

    def reset_cb(event):
        app_state['reset'] = True
        app_state['paused'] = False
        
    ax_start = fig.add_axes([0.55, 0.05, 0.1, 0.06])
    ax_stop = fig.add_axes([0.68, 0.05, 0.1, 0.06])
    ax_reset = fig.add_axes([0.81, 0.05, 0.1, 0.06])

    btn_start = Button(ax_start, 'Start')
    btn_start.on_clicked(start_cb)

    btn_stop = Button(ax_stop, 'Stop')
    btn_stop.on_clicked(stop_cb)

    btn_reset = Button(ax_reset, 'Reset')
    btn_reset.on_clicked(reset_cb)
    
    ax_radio = fig.add_axes([0.70, 0.60, 0.28, 0.22], facecolor='lightgoldenrodyellow')
    radio = RadioButtons(ax_radio, ('Backtracking', 'Forward Checking', 'AC-3', 'Min-Conflicts'))
    
    def algo_cb(label):
        app_state['algorithm'] = label
        app_state['reset'] = True
        app_state['paused'] = True
        
    radio.on_clicked(algo_cb)
    
    class ResetInterrupt(Exception):
        pass

    while plt.fignum_exists(fig.number):
        app_state['reset'] = False
        app_state['paused'] = True
        
        state['all_logs'].clear()
        with open("log_quatrinh.txt", "w", encoding="utf-8") as f:
            f.write("BẮT ĐẦU CHẠY THUẬT TOÁN TÔ MÀU BẢN ĐỒ\n" + "="*50 + "\n")
        update_log_display()

        # --- Print Initial Problem Formulation ---
        log_message("\nBiểu diễn dưới dạng CSP:")
        log_message(f"- Biến: {{{', '.join(variables)}}}")
        log_message(f"- Miền giá trị: {{{', '.join(COLOR_NAMES[:len(domains[variables[0]])])}}}")
        constraints = []
        for u, v_list in neighbors.items():
            for v in v_list:
                if u < v:
                    constraints.append(f"{u}≠{v}")
        log_message(f"- Ràng buộc: {', '.join(constraints)}")
        log_message("\nÁp dụng Backtracking:")
    
        # --- Run CSP Solver ---
        # Make a deep copy of domains for this run so a reset has clean domains
        current_domains = copy.deepcopy(domains)
        
        if app_state['algorithm'] == 'Backtracking':
            csp = CSP_BT(variables, current_domains, neighbors, COLOR_NAMES, log_func=log_message)
            alg_name = "Backtracking + MRV"
            USE_FC = False
            USE_AC3 = False
            is_min_conflicts = False
        elif app_state['algorithm'] == 'Forward Checking':
            csp = CSP_FC(variables, current_domains, neighbors, COLOR_NAMES, log_func=log_message)
            alg_name = "Forward Checking + MRV"
            USE_FC = True
            USE_AC3 = False
            is_min_conflicts = False
        elif app_state['algorithm'] == 'AC-3':
            csp = CSP_BT(variables, current_domains, neighbors, COLOR_NAMES, log_func=log_message)
            alg_name = "AC-3 (MAC) + MRV"
            USE_FC = False
            USE_AC3 = True
            is_min_conflicts = False
        elif app_state['algorithm'] == 'Min-Conflicts':
            from MinConflicts import CSP as CSP_MC
            csp = CSP_MC(variables, current_domains, neighbors, COLOR_NAMES, log_func=log_message)
            alg_name = "Min-Conflicts"
            USE_FC = False
            USE_AC3 = False
            is_min_conflicts = True
            
        log_message("Starting CSP Map Coloring (Paused - Click Start to begin)...")
        log_message(f"Algorithm: {alg_name}")
        
        USE_MRV = True
        
        initial_assignment = {}
        
        try:
            # Optional: AC3 initialization before search
            if USE_AC3 and not is_min_conflicts:
                log_message("Running initial AC-3 Constraint Propagation...")
                csp.ac3()
                
            draw_graph(initial_assignment, None, csp.domains)
            
            # Wait until user presses Start
            while app_state['paused'] and plt.fignum_exists(fig.number):
                plt.pause(0.1)
                if app_state['reset']:
                    break
            
            if app_state['reset'] or not plt.fignum_exists(fig.number):
                if app_state['reset']:
                    raise ResetInterrupt()
                break
                
            if is_min_conflicts:
                result = csp.min_conflicts(
                    initial_assignment,
                    max_steps=1000,
                    callback=draw_graph
                )
            elif app_state['algorithm'] == 'Forward Checking':
                result = csp.backtrack(
                    initial_assignment, 
                    use_mrv=USE_MRV, 
                    use_fc=USE_FC, 
                    use_ac3=USE_AC3, 
                    callback=draw_graph
                )
            else:
                result = csp.backtrack(
                    initial_assignment, 
                    use_mrv=USE_MRV, 
                    use_ac3=USE_AC3, 
                    callback=draw_graph
                )
            
            # --- Result Output ---
            if result:
                log_message("\nSolution found!")
                log_message(f"Total Assignments: {csp.assignments}")
                log_message(f"Total Backtracks: {csp.backtracks}")
                for var, color_idx in result.items():
                    log_message(f"{var}: Color {color_idx}")
                # Final draw
                draw_graph(result, None, csp.domains)
            else:
                log_message("\nNo solution found with the given constraints and number of colors.")
                
            log_message("\nFinished. You can review the logs or click Reset to run again.")
            
            # Idle loop until reset or exit
            while not app_state['reset'] and plt.fignum_exists(fig.number):
                plt.pause(0.1)
                
        except ResetInterrupt:
            log_message("\n--- SYSTEM RESET ---")
            continue

if __name__ == "__main__":
    main()
