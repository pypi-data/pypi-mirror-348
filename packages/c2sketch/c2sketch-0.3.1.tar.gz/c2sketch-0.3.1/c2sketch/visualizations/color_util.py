"""Utility functions for handling color in visualizations"""

def relative_luminance(hexcolor):
    #From https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
    rs_rgb = int(hexcolor[1:3],base=16) / 255
    gs_rgb = int(hexcolor[3:5],base=16) / 255
    bs_rgb = int(hexcolor[5:7],base=16) / 255
    
    r = (rs_rgb / 12.92) if rs_rgb <= 0.04045 else ((rs_rgb + 0.055)/1.055) ** 2.4
    g = (gs_rgb / 12.92) if gs_rgb <= 0.04045 else ((gs_rgb + 0.055)/1.055) ** 2.4
    b = (bs_rgb / 12.92) if bs_rgb <= 0.04045 else ((bs_rgb + 0.055)/1.055) ** 2.4
    
    return (0.2126 * r + 0.7152 * g + 0.0722 * b)

def black_or_white(background_color):
    return '#ffffff' if relative_luminance(background_color) <= 0.3 else '#000000'