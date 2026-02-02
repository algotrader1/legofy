"""
Legofy - Convert images to Lego tile patterns for screen printing molds
"""

from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import io
import base64
from collections import defaultdict

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Lego piece definitions with official LEGO part numbers
LEGO_PIECES = {
    # Standard rectangular tiles
    '1x1': {'width': 1, 'height': 1, 'name': 'Tuile 1x1', 'part_num': '3070', 'shape': 'rect'},
    '1x2': {'width': 2, 'height': 1, 'name': 'Tuile 1x2', 'part_num': '3069', 'shape': 'rect'},
    '1x3': {'width': 3, 'height': 1, 'name': 'Tuile 1x3', 'part_num': '63864', 'shape': 'rect'},
    '1x4': {'width': 4, 'height': 1, 'name': 'Tuile 1x4', 'part_num': '2431', 'shape': 'rect'},
    '1x6': {'width': 6, 'height': 1, 'name': 'Tuile 1x6', 'part_num': '6636', 'shape': 'rect'},
    '1x8': {'width': 8, 'height': 1, 'name': 'Tuile 1x8', 'part_num': '4162', 'shape': 'rect'},
    '2x2': {'width': 2, 'height': 2, 'name': 'Tuile 2x2', 'part_num': '3068', 'shape': 'rect'},
    '2x3': {'width': 3, 'height': 2, 'name': 'Tuile 2x3', 'part_num': '26603', 'shape': 'rect'},
    '2x4': {'width': 4, 'height': 2, 'name': 'Tuile 2x4', 'part_num': '87079', 'shape': 'rect'},

    # Round tiles
    'round_1x1': {'width': 1, 'height': 1, 'name': 'Tuile ronde 1x1', 'part_num': '98138', 'shape': 'round'},
    'quarter_1x1': {'width': 1, 'height': 1, 'name': 'Tuile quart de rond 1x1', 'part_num': '25269', 'shape': 'quarter'},
    'half_1x2': {'width': 2, 'height': 1, 'name': 'Tuile demi-ronde 1x2', 'part_num': '1126', 'shape': 'half'},

    # Macaroni tiles (outer quarter circle)
    'macaroni_2x2': {'width': 2, 'height': 2, 'name': 'Tuile Macaroni 2x2', 'part_num': '27925', 'shape': 'macaroni'},
    'macaroni_3x3': {'width': 3, 'height': 3, 'name': 'Tuile Macaroni 3x3', 'part_num': '79393', 'shape': 'macaroni'},
    'macaroni_4x4': {'width': 4, 'height': 4, 'name': 'Tuile Macaroni 4x4', 'part_num': '27507', 'shape': 'macaroni'},
}


def image_to_base64(img):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()


def process_image(image_data, threshold, grid_width, grid_height, invert=False):
    """Process image: convert to binary using threshold and resize to grid dimensions"""
    img = Image.open(io.BytesIO(image_data))
    img = img.convert('L')
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)

    img_array = np.array(img)
    binary = (img_array > threshold).astype(np.uint8) * 255

    if invert:
        binary = 255 - binary

    return binary


def apply_threshold_only(image_data, threshold, invert=False):
    """Apply threshold to image without resizing (for live preview)"""
    img = Image.open(io.BytesIO(image_data))
    img = img.convert('L')

    max_size = 400
    ratio = min(max_size / img.width, max_size / img.height)
    if ratio < 1:
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    img_array = np.array(img)
    binary = (img_array > threshold).astype(np.uint8) * 255

    if invert:
        binary = 255 - binary

    return Image.fromarray(binary)


def is_corner(grid, x, y, target_value):
    """
    Detect if position (x,y) is at a corner of the filled area.
    Returns corner type: 'tl', 'tr', 'bl', 'br' or None
    """
    h, w = grid.shape

    def get(dx, dy):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            return grid[ny, nx] == target_value
        return False

    current = grid[y, x] == target_value
    if not current:
        return None

    # Check for outer corners (convex)
    # Top-left corner: no cell above or to the left
    if not get(0, -1) and not get(-1, 0):
        return 'tl'
    # Top-right corner
    if not get(0, -1) and not get(1, 0):
        return 'tr'
    # Bottom-left corner
    if not get(0, 1) and not get(-1, 0):
        return 'bl'
    # Bottom-right corner
    if not get(0, 1) and not get(1, 0):
        return 'br'

    return None


def can_place_macaroni(grid, placed, x, y, size, corner, target_value):
    """
    Check if a macaroni tile can be placed at (x, y) with given size and corner orientation.
    Macaroni tiles fill a quarter-circle pattern within a square bounding box.
    """
    h, w = grid.shape

    # Define the cells that a macaroni occupies based on corner type
    # For simplicity, we'll approximate: macaroni fills all cells in its bounding box
    # that are "inside" the quarter circle

    cells = []
    for dy in range(size):
        for dx in range(size):
            nx, ny = x + dx, y + dy
            if nx >= w or ny >= h:
                return None

            # Check if this cell is within the macaroni's coverage
            # Approximate: for corner 'tl', the curve goes from bottom-left to top-right
            in_macaroni = True
            if corner == 'tl':
                # Quarter circle from (0, size-1) to (size-1, 0)
                dist = ((dx) ** 2 + (dy) ** 2) ** 0.5
                in_macaroni = dist <= size
            elif corner == 'tr':
                dist = ((size - 1 - dx) ** 2 + (dy) ** 2) ** 0.5
                in_macaroni = dist <= size
            elif corner == 'bl':
                dist = ((dx) ** 2 + (size - 1 - dy) ** 2) ** 0.5
                in_macaroni = dist <= size
            elif corner == 'br':
                dist = ((size - 1 - dx) ** 2 + (size - 1 - dy) ** 2) ** 0.5
                in_macaroni = dist <= size

            if in_macaroni:
                if placed[ny, nx] or grid[ny, nx] != target_value:
                    return None
                cells.append((nx, ny))

    return cells if cells else None


def greedy_tile_placement(grid, selected_pieces, fill_white=True, use_curves=True):
    """
    Greedy algorithm to place tiles on the grid.
    Places largest pieces first, with optional curved pieces for corners.
    """
    height, width = grid.shape
    target_value = 255 if fill_white else 0

    placed = np.zeros((height, width), dtype=bool)

    # Separate rectangular and special pieces
    rect_pieces = [(k, v) for k, v in LEGO_PIECES.items()
                   if k in selected_pieces and v['shape'] == 'rect']
    macaroni_pieces = [(k, v) for k, v in LEGO_PIECES.items()
                       if k in selected_pieces and v['shape'] == 'macaroni']
    quarter_pieces = [(k, v) for k, v in LEGO_PIECES.items()
                      if k in selected_pieces and v['shape'] == 'quarter']
    half_pieces = [(k, v) for k, v in LEGO_PIECES.items()
                   if k in selected_pieces and v['shape'] == 'half']

    # Sort by size (largest first)
    rect_pieces = sorted(rect_pieces, key=lambda x: x[1]['width'] * x[1]['height'], reverse=True)
    macaroni_pieces = sorted(macaroni_pieces, key=lambda x: x[1]['width'], reverse=True)

    placements = []
    piece_counts = defaultdict(int)

    # First pass: place macaroni tiles at corners if enabled
    if use_curves and macaroni_pieces:
        for y in range(height):
            for x in range(width):
                if placed[y, x] or grid[y, x] != target_value:
                    continue

                corner = is_corner(grid, x, y, target_value)
                if corner:
                    # Try to place largest macaroni that fits
                    for piece_id, piece_info in macaroni_pieces:
                        size = piece_info['width']

                        # Adjust position based on corner type
                        px, py = x, y
                        if corner == 'tr':
                            px = x - size + 1
                        elif corner == 'bl':
                            py = y - size + 1
                        elif corner == 'br':
                            px = x - size + 1
                            py = y - size + 1

                        if px < 0 or py < 0:
                            continue

                        cells = can_place_macaroni(grid, placed, px, py, size, corner, target_value)
                        if cells:
                            for cx, cy in cells:
                                placed[cy, cx] = True
                            placements.append({
                                'piece': piece_id,
                                'x': px,
                                'y': py,
                                'width': size,
                                'height': size,
                                'rotation': 0,
                                'corner': corner,
                                'shape': 'macaroni'
                            })
                            piece_counts[piece_id] += 1
                            break

    # Second pass: fill remaining with rectangular pieces
    for y in range(height):
        for x in range(width):
            if placed[y, x] or grid[y, x] != target_value:
                continue

            piece_placed = False

            # Try rectangular pieces
            for piece_id, piece_info in rect_pieces:
                pw, ph = piece_info['width'], piece_info['height']

                for rot, (w, h) in enumerate([(pw, ph), (ph, pw)]):
                    if pw == ph and rot == 1:
                        continue
                    if x + w > width or y + h > height:
                        continue

                    can_place = True
                    for dy in range(h):
                        for dx in range(w):
                            if placed[y + dy, x + dx] or grid[y + dy, x + dx] != target_value:
                                can_place = False
                                break
                        if not can_place:
                            break

                    if can_place:
                        for dy in range(h):
                            for dx in range(w):
                                placed[y + dy, x + dx] = True
                        placements.append({
                            'piece': piece_id,
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'rotation': rot,
                            'shape': 'rect'
                        })
                        piece_counts[piece_id] += 1
                        piece_placed = True
                        break

                if piece_placed:
                    break

            # Fallback to 1x1
            if not piece_placed and '1x1' in selected_pieces:
                if grid[y, x] == target_value and not placed[y, x]:
                    placed[y, x] = True
                    placements.append({
                        'piece': '1x1',
                        'x': x,
                        'y': y,
                        'width': 1,
                        'height': 1,
                        'rotation': 0,
                        'shape': 'rect'
                    })
                    piece_counts['1x1'] += 1

    return placements, dict(piece_counts)


def draw_macaroni(pixels, x, y, size, corner, cell_size, color):
    """Draw a macaroni (quarter circle) tile"""
    for dy in range(size):
        for dx in range(size):
            # Calculate if pixel is inside the quarter circle
            for py in range(dy * cell_size, (dy + 1) * cell_size):
                for px in range(dx * cell_size, (dx + 1) * cell_size):
                    # Pixel position relative to corner
                    rel_x = px - dx * cell_size + dx * cell_size
                    rel_y = py - dy * cell_size + dy * cell_size

                    # Check if inside quarter circle
                    in_circle = False
                    center_x, center_y = 0, 0
                    radius = size * cell_size

                    if corner == 'tl':
                        center_x, center_y = 0, 0
                        dist = ((x * cell_size + px - dx * cell_size) ** 2 +
                                (y * cell_size + py - dy * cell_size) ** 2) ** 0.5
                        in_circle = dist <= radius
                    elif corner == 'tr':
                        center_x = size * cell_size
                        dist = ((size * cell_size - (px - dx * cell_size + dx * cell_size)) ** 2 +
                                (py - dy * cell_size + dy * cell_size) ** 2) ** 0.5
                        in_circle = dist <= radius
                    elif corner == 'bl':
                        center_y = size * cell_size
                        dist = ((px - dx * cell_size + dx * cell_size) ** 2 +
                                (size * cell_size - (py - dy * cell_size + dy * cell_size)) ** 2) ** 0.5
                        in_circle = dist <= radius
                    elif corner == 'br':
                        center_x, center_y = size * cell_size, size * cell_size
                        dist = ((size * cell_size - (px - dx * cell_size + dx * cell_size)) ** 2 +
                                (size * cell_size - (py - dy * cell_size + dy * cell_size)) ** 2) ** 0.5
                        in_circle = dist <= radius

                    if in_circle:
                        abs_x = x * cell_size + px - dx * cell_size + dx * cell_size
                        abs_y = y * cell_size + py - dy * cell_size + dy * cell_size
                        # Simplified: just fill the bounding box for now
                        pass


def generate_preview_image(grid, placements, cell_size=20):
    """Generate a BLACK/WHITE preview image showing the Lego placement"""
    height, width = grid.shape
    img_width = width * cell_size
    img_height = height * cell_size

    preview = Image.new('L', (img_width, img_height), 255)
    pixels = preview.load()

    # Draw placed pieces
    for p in placements:
        x, y = p['x'], p['y']
        w, h = p['width'], p['height']
        shape = p.get('shape', 'rect')
        corner = p.get('corner', 'tl')

        if shape == 'macaroni':
            # Draw quarter circle
            size = w
            for py_off in range(size * cell_size):
                for px_off in range(size * cell_size):
                    # Calculate distance from corner
                    if corner == 'tl':
                        dist = (px_off ** 2 + py_off ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    elif corner == 'tr':
                        dist = ((size * cell_size - 1 - px_off) ** 2 + py_off ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    elif corner == 'bl':
                        dist = (px_off ** 2 + (size * cell_size - 1 - py_off) ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    elif corner == 'br':
                        dist = ((size * cell_size - 1 - px_off) ** 2 +
                                (size * cell_size - 1 - py_off) ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    else:
                        in_circle = True

                    if in_circle:
                        abs_x = x * cell_size + px_off
                        abs_y = y * cell_size + py_off
                        if 0 <= abs_x < img_width and 0 <= abs_y < img_height:
                            pixels[abs_x, abs_y] = 0
        else:
            # Rectangular piece
            for py in range(y * cell_size, (y + h) * cell_size):
                for px in range(x * cell_size, (x + w) * cell_size):
                    if 0 <= px < img_width and 0 <= py < img_height:
                        pixels[px, py] = 0

    # Draw grid lines
    for gy in range(height + 1):
        for px in range(img_width):
            py_coord = min(gy * cell_size, img_height - 1)
            if pixels[px, py_coord] != 0:
                pixels[px, py_coord] = 200

    for gx in range(width + 1):
        for py in range(img_height):
            px_coord = min(gx * cell_size, img_width - 1)
            if pixels[px_coord, py] != 0:
                pixels[px_coord, py] = 200

    # Draw piece borders
    for p in placements:
        x, y = p['x'], p['y']
        w, h = p['width'], p['height']

        for px in range(x * cell_size, (x + w) * cell_size):
            if 0 <= px < img_width:
                if y * cell_size < img_height:
                    pixels[px, y * cell_size] = 100
                if (y + h) * cell_size - 1 < img_height:
                    pixels[px, (y + h) * cell_size - 1] = 100

        for py in range(y * cell_size, (y + h) * cell_size):
            if 0 <= py < img_height:
                if x * cell_size < img_width:
                    pixels[x * cell_size, py] = 100
                if (x + w) * cell_size - 1 < img_width:
                    pixels[(x + w) * cell_size - 1, py] = 100

    return preview


def generate_colored_preview(grid, placements, cell_size=20):
    """Generate a COLORED preview for piece identification"""
    height, width = grid.shape
    img_width = width * cell_size
    img_height = height * cell_size

    preview = Image.new('RGB', (img_width, img_height), (240, 240, 240))
    pixels = preview.load()

    # Background
    for y in range(height):
        for x in range(width):
            color = (255, 255, 255) if grid[y, x] == 255 else (220, 220, 220)
            for py in range(y * cell_size, (y + 1) * cell_size):
                for px in range(x * cell_size, (x + 1) * cell_size):
                    pixels[px, py] = color

    # Piece colors
    piece_colors = {
        '1x1': (255, 120, 120),
        '1x2': (120, 255, 120),
        '1x3': (120, 200, 255),
        '1x4': (255, 200, 120),
        '1x6': (200, 120, 255),
        '1x8': (255, 255, 120),
        '2x2': (120, 255, 200),
        '2x3': (255, 150, 200),
        '2x4': (150, 200, 255),
        'round_1x1': (255, 180, 180),
        'quarter_1x1': (180, 255, 180),
        'half_1x2': (180, 180, 255),
        'macaroni_2x2': (255, 220, 150),
        'macaroni_3x3': (150, 255, 220),
        'macaroni_4x4': (220, 150, 255),
    }

    for p in placements:
        x, y = p['x'], p['y']
        w, h = p['width'], p['height']
        color = piece_colors.get(p['piece'], (180, 180, 180))
        shape = p.get('shape', 'rect')
        corner = p.get('corner', 'tl')

        if shape == 'macaroni':
            size = w
            for py_off in range(size * cell_size):
                for px_off in range(size * cell_size):
                    if corner == 'tl':
                        dist = (px_off ** 2 + py_off ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    elif corner == 'tr':
                        dist = ((size * cell_size - 1 - px_off) ** 2 + py_off ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    elif corner == 'bl':
                        dist = (px_off ** 2 + (size * cell_size - 1 - py_off) ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    elif corner == 'br':
                        dist = ((size * cell_size - 1 - px_off) ** 2 +
                                (size * cell_size - 1 - py_off) ** 2) ** 0.5
                        in_circle = dist <= size * cell_size
                    else:
                        in_circle = True

                    if in_circle:
                        abs_x = x * cell_size + px_off
                        abs_y = y * cell_size + py_off
                        if 0 <= abs_x < img_width and 0 <= abs_y < img_height:
                            pixels[abs_x, abs_y] = color
        else:
            for py in range(y * cell_size + 1, (y + h) * cell_size - 1):
                for px in range(x * cell_size + 1, (x + w) * cell_size - 1):
                    if 0 <= px < img_width and 0 <= py < img_height:
                        pixels[px, py] = color

            # Border
            border = tuple(max(0, c - 50) for c in color)
            for px in range(x * cell_size, (x + w) * cell_size):
                if 0 <= px < img_width:
                    if y * cell_size < img_height:
                        pixels[px, y * cell_size] = border
                    if (y + h) * cell_size - 1 < img_height:
                        pixels[px, (y + h) * cell_size - 1] = border
            for py in range(y * cell_size, (y + h) * cell_size):
                if 0 <= py < img_height:
                    if x * cell_size < img_width:
                        pixels[x * cell_size, py] = border
                    if (x + w) * cell_size - 1 < img_width:
                        pixels[(x + w) * cell_size - 1, py] = border

    return preview


@app.route('/')
def index():
    return render_template('index.html', pieces=LEGO_PIECES)


@app.route('/preview_threshold', methods=['POST'])
def preview_threshold():
    """Live threshold preview endpoint"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image'}), 400

        image_file = request.files['image']
        image_data = image_file.read()
        threshold = int(request.form.get('threshold', 128))
        invert = request.form.get('invert', 'false') == 'true'

        preview = apply_threshold_only(image_data, threshold, invert)

        return jsonify({
            'success': True,
            'preview_image': image_to_base64(preview)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process', methods=['POST'])
def process():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        image_data = image_file.read()

        threshold = int(request.form.get('threshold', 128))
        grid_width = int(request.form.get('grid_width', 48))
        grid_height = int(request.form.get('grid_height', 48))
        invert = request.form.get('invert', 'false') == 'true'
        selected_pieces = request.form.getlist('pieces')
        show_colors = request.form.get('show_colors', 'false') == 'true'
        use_curves = request.form.get('use_curves', 'true') == 'true'

        if not selected_pieces:
            selected_pieces = ['1x1', '1x2', '2x2']

        binary_grid = process_image(image_data, threshold, grid_width, grid_height, invert)
        placements, piece_counts = greedy_tile_placement(
            binary_grid, selected_pieces, fill_white=True, use_curves=use_curves
        )

        preview_img = generate_preview_image(binary_grid, placements)
        colored_img = generate_colored_preview(binary_grid, placements) if show_colors else None
        binary_img = Image.fromarray(binary_grid)

        total_white = np.sum(binary_grid == 255)
        covered = sum(p['width'] * p['height'] for p in placements)
        coverage = (covered / total_white * 100) if total_white > 0 else 0

        response = {
            'success': True,
            'binary_image': image_to_base64(binary_img),
            'preview_image': image_to_base64(preview_img),
            'piece_counts': piece_counts,
            'total_pieces': sum(piece_counts.values()),
            'grid_size': {'width': grid_width, 'height': grid_height},
            'coverage': round(coverage, 1),
            'placements': placements,
            'piece_info': {k: {'name': v['name'], 'part_num': v['part_num']}
                          for k, v in LEGO_PIECES.items() if k in piece_counts}
        }

        if colored_img:
            response['colored_image'] = image_to_base64(colored_img)

        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/export', methods=['POST'])
def export():
    """Export placement data as JSON"""
    try:
        data = request.json
        placements = data.get('placements', [])
        piece_counts = data.get('piece_counts', {})
        grid_size = data.get('grid_size', {})

        pieces_detail = {}
        for piece_id, count in piece_counts.items():
            info = LEGO_PIECES.get(piece_id, {})
            pieces_detail[piece_id] = {
                'name': info.get('name', piece_id),
                'lego_part_number': info.get('part_num', 'N/A'),
                'quantity': count,
                'size': f"{info.get('width', '?')}x{info.get('height', '?')}"
            }

        export_data = {
            'grid_width': grid_size.get('width', 0),
            'grid_height': grid_size.get('height', 0),
            'pieces_needed': pieces_detail,
            'total_pieces': sum(piece_counts.values()),
            'placements': placements
        }

        return jsonify(export_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
