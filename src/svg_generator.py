import math
import tempfile
import svgwrite


class SVGGenerator:
    def __init__(self):
        self.temp_svg_file = None
    
    def calculate_lines_for_ring(self, ring_widget, radius, ring_depth):
        settings = ring_widget.get_settings()
        rpm = settings['rpm']
        hz = settings['hz']
        single_mode = settings['single_mode']
        shape_type = settings['shape_type']
        density = settings['density']
        dot_size = settings['dot_size']
        
        ring_widget.update_segments_info(radius)
        
        density_factor = 2 if density == "double" else 1
        num_lines_exact = (60 * hz) / rpm * density_factor
        
        num_lines_floor = math.floor(num_lines_exact)
        num_lines_ceil = math.ceil(num_lines_exact)
        
        if num_lines_floor == num_lines_ceil or single_mode:
            if num_lines_floor == num_lines_ceil:
                num_lines = num_lines_floor
            else:
                num_lines = round(num_lines_exact)
            
            circumference = 2 * math.pi * radius
            line_width = circumference / (num_lines * 2)
            
            return {
                'mode': 'single',
                'num_lines': num_lines,
                'line_width': line_width,
                'shape_type': shape_type,
                'dot_size': dot_size
            }
        else:
            outer_circumference = 2 * math.pi * radius
            inner_circumference = 2 * math.pi * (radius - ring_depth)
            
            outer_line_width = outer_circumference / (num_lines_floor * 2)
            inner_line_width = inner_circumference / (num_lines_ceil * 2)
            
            return {
                'mode': 'double',
                'outer_num_lines': num_lines_floor,
                'outer_line_width': outer_line_width,
                'inner_num_lines': num_lines_ceil,
                'inner_line_width': inner_line_width,
                'shape_type': shape_type,
                'dot_size': dot_size
            }
    
    def generate_disc(self, diameter, spindle_diameter, outer_circle_width, 
                     ring_separation, ring_widgets):
        self.temp_svg_file = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
        self.temp_svg_file.close()
        
        dwg = svgwrite.Drawing(
            self.temp_svg_file.name,
            size=(f"{diameter}mm", f"{diameter}mm"),
            profile="tiny",
            viewBox=f"0 0 {diameter} {diameter}",
        )
        
        center = (diameter / 2, diameter / 2)
        
        # Draw Outer Circle
        disc_radius = diameter / 2 - (outer_circle_width / 2 if outer_circle_width > 0 else 0)
        
        if outer_circle_width > 0:
            dwg.add(dwg.circle(
                center=center, 
                r=disc_radius, 
                fill='none', 
                stroke='black', 
                stroke_width=outer_circle_width
            ))
            
        current_radius = disc_radius - (outer_circle_width / 2 if outer_circle_width > 0 else 0)
        
        # Draw each ring from outside to inside
        for i, ring_widget in enumerate(ring_widgets):
            settings = ring_widget.get_settings()
            ring_depth = settings['depth']
            
            inner_radius = current_radius - ring_depth
            
            if inner_radius < spindle_diameter / 2:
                inner_radius = spindle_diameter / 2
                ring_depth = current_radius - inner_radius
            
            lines_info = self.calculate_lines_for_ring(ring_widget, current_radius, ring_depth)
            
            if lines_info['mode'] == 'single':
                self._draw_single_ring(dwg, center, lines_info, current_radius, inner_radius)
            else:
                self._draw_double_ring(dwg, center, lines_info, current_radius, inner_radius, ring_depth)
            
            current_radius = inner_radius - ring_separation
        
        # Draw Spindle Hole
        dwg.add(dwg.circle(
            center=center, 
            r=spindle_diameter/2, 
            fill='black', 
            stroke='black', 
            stroke_width=0.2
        ))
        
        dwg.save()
        return self.temp_svg_file.name
    
    def _draw_single_ring(self, dwg, center, lines_info, current_radius, inner_radius):
        num_lines = lines_info['num_lines']
        line_width = lines_info['line_width']
        shape_type = lines_info['shape_type']
        dot_size = lines_info['dot_size']
        
        angle_increment = 360 / num_lines
        
        for j in range(num_lines):
            angle = math.radians(j * angle_increment)
            
            if shape_type == 'lines':
                x1 = center[0] + current_radius * math.sin(angle)
                y1 = center[1] - (current_radius * math.cos(angle))
                
                x2 = center[0] + inner_radius * math.sin(angle)
                y2 = center[1] - (inner_radius * math.cos(angle))
                
                dwg.add(dwg.line((x1, y1), (x2, y2), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_width=line_width))
            else:
                mid_radius = (current_radius + inner_radius) / 2
                dot_x = center[0] + mid_radius * math.sin(angle)
                dot_y = center[1] - (mid_radius * math.cos(angle))
                
                dot_radius = (line_width / 2) * dot_size
                
                dwg.add(dwg.circle(center=(dot_x, dot_y), r=dot_radius, fill='black'))
    
    def _draw_double_ring(self, dwg, center, lines_info, current_radius, inner_radius, ring_depth):
        shape_type = lines_info['shape_type']
        
        # Outer set
        outer_num_lines = lines_info['outer_num_lines']
        outer_line_width = lines_info['outer_line_width']
        
        angle_increment_outer = 360 / outer_num_lines
        
        for j in range(outer_num_lines):
            angle = math.radians(j * angle_increment_outer)
            
            if shape_type == 'lines':
                x1 = center[0] + current_radius * math.sin(angle)
                y1 = center[1] - (current_radius * math.cos(angle))
                
                mid_radius = current_radius - ring_depth / 2
                x2 = center[0] + mid_radius * math.sin(angle)
                y2 = center[1] - (mid_radius * math.cos(angle))
                
                dwg.add(dwg.line((x1, y1), (x2, y2), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_width=outer_line_width))
            else:
                outer_dot_radius = current_radius - ring_depth / 4
                dot_x = center[0] + outer_dot_radius * math.sin(angle)
                dot_y = center[1] - (outer_dot_radius * math.cos(angle))
                
                dot_size = lines_info['dot_size']
                dot_radius = (outer_line_width / 2) * dot_size
                
                dwg.add(dwg.circle(center=(dot_x, dot_y), r=dot_radius, fill='black'))
        
        # Inner set
        inner_num_lines = lines_info['inner_num_lines']
        inner_line_width = lines_info['inner_line_width']
        
        angle_increment_inner = 360 / inner_num_lines
        
        for j in range(inner_num_lines):
            angle = math.radians(j * angle_increment_inner)
            
            if shape_type == 'lines':
                mid_radius = current_radius - ring_depth / 2
                x1 = center[0] + mid_radius * math.sin(angle)
                y1 = center[1] - (mid_radius * math.cos(angle))
                
                x2 = center[0] + inner_radius * math.sin(angle)
                y2 = center[1] - (inner_radius * math.cos(angle))
                
                dwg.add(dwg.line((x1, y1), (x2, y2), stroke=svgwrite.rgb(0, 0, 0, "%"), stroke_width=inner_line_width))
            else:
                inner_dot_radius = inner_radius + ring_depth / 4
                dot_x = center[0] + inner_dot_radius * math.sin(angle)
                dot_y = center[1] - (inner_dot_radius * math.cos(angle))
                
                dot_size = lines_info['dot_size']
                dot_radius = (inner_line_width / 2) * dot_size
                
                dwg.add(dwg.circle(center=(dot_x, dot_y), r=dot_radius, fill='black'))