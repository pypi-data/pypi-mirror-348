"""
SmartCalculator: A minimalistic, themed, one-line calculator using Pygame.

Features:
- Keyboard-only input
- Tokyo Night dark/light themes
- Variable assignment and accumulation (>, >>)
- Right-aligned formatted results
- Auto-scaling font size
- Command history recall with ↑/↓
"""

import ast
import locale
import pygame

from pathlib import Path

# --- Constants ---
WIDTH, HEIGHT = 800, 300
LEFT_PADDING = 40
TOP_INPUT_OFFSET = 100
CENTER_Y = HEIGHT // 2
RESULT_TOP_OFFSET = 20
RESULT_RIGHT_PADDING = 40
MAX_TEXT_WIDTH = WIDTH - 2 * LEFT_PADDING
FPS = 30

# --- Themes ---
DARK_THEME = {
    "bg": (26, 27, 38),         # Dark Navy Blue
    "text": (192, 202, 245),    # Soft Lavender
    "input": (122, 162, 247),   # Blue Accent
    "error": (255, 85, 85),     # Red Error
    "line": (59, 66, 82),       # Steel Gray
}

LIGHT_THEME = {
    "bg": (244, 240, 222),      # Warm Paper Beige
    "text": (30, 30, 30),       # Deep Gray
    "input": (80, 60, 20),      # Brown Accent
    "error": (170, 0, 0),       # Wine Red
    "line": (160, 140, 100),    # Sepia Brown
}

# --- State ---
theme = DARK_THEME
history: list[str] = []
history_index: int | None = None
last_raw_result = None
last_result = ""
user_input = ""
variables: dict[str, float] = {}

pygame.init()
locale.setlocale(locale.LC_NUMERIC, '')  # Format floats nicely
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Calculator")
clock = pygame.time.Clock()

# --- Font Loading ---
def load_font(size: int) -> pygame.font.Font:
    """Load the bundled FiraCode Nerd Font, fallback to system default."""
    font_path = Path("fonts/FiraCodeNerdFont-Regular.ttf")
    if font_path.exists():
        return pygame.font.Font(str(font_path), size)
    return pygame.font.Font(None, size)

# --- Helpers ---
def format_number(value: float) -> str:
    """Format number with underscores."""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    try:
        return f"{value:,}".replace(",", "_")
    except Exception:
        return str(value)

def evaluate(expr: str) -> str:
    """Evaluate expression with post-assignment support."""
    global variables, last_result, last_raw_result

    if isinstance(last_raw_result, (int, float)):
        variables['_'] = last_raw_result

    if ">>" in expr:
        value_part, var_part = expr.split(">>")
        var = var_part.strip()
        value = value_part.strip()
        if var not in variables:
            expr = f"{var} = {value}"
        else:
            expr = f"{var} = {var} + ({value})"

    elif ">" in expr:
        value_part, var_part = expr.split(">")
        expr = f"{var_part.strip()} = {value_part.strip()}"

    try:
        tree = ast.parse(expr, mode='exec')
        node = tree.body[0]

        if isinstance(node, ast.Assign):
            var = node.targets[0].id
            val = eval_expr(node.value)
            variables[var] = val
            last_raw_result = val
            return format_number(val)

        elif isinstance(node, ast.Expr):
            val = eval_expr(node.value)
            last_raw_result = val
            return format_number(val)

    except Exception as e:
        return f"Error: {e}"

    return "Invalid input"

def eval_expr(node):
    """Safely evaluate math expressions from AST nodes."""
    if isinstance(node, ast.BinOp):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        match type(node.op):
            case ast.Add: return left + right
            case ast.Sub: return left - right
            case ast.Mult: return left * right
            case ast.Div: return left / right
            case ast.Pow: return left ** right
            case ast.Mod: return left % right
    elif isinstance(node, ast.UnaryOp):
        operand = eval_expr(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
    elif isinstance(node, ast.Name):
        return variables.get(node.id, 0)
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    raise ValueError("Unsupported expression")

def render_text(text: str, color: tuple[int], max_width: int) -> pygame.Surface:
    """Render text with auto-scaling font size to fit."""
    size = 64
    while size > 20:
        font = load_font(size)
        surface = font.render(text, True, color)
        if surface.get_width() < max_width:
            return surface
        size -= 2
    return font.render(text, True, color)

def navigate_history(up: bool) -> None:
    global history_index, user_input
    if not history:
        return
    if up:
        if history_index is None:
            history_index = len(history) - 1
        elif history_index > 0:
            history_index -= 1
    else:
        if history_index is not None:
            history_index += 1
            if history_index >= len(history):
                history_index = None
                user_input = ""
                return
    if history_index is not None:
        user_input = history[history_index]

def handle_key(event: pygame.event.Event) -> None:
    """Action keys: get answer, history input, correct input, theme change"""
    global user_input, last_result, theme, history, history_index

    if event.key == pygame.K_RETURN:
        history.append(user_input)
        history_index = None
        last_result = evaluate(user_input.strip())
        user_input = ""

    elif event.key == pygame.K_UP:
        navigate_history(up=True)
    elif event.key == pygame.K_DOWN:
        navigate_history(up=False)

    elif event.key == pygame.K_BACKSPACE:
        user_input = user_input[:-1]

    elif event.unicode == "T":
        theme = LIGHT_THEME if theme == DARK_THEME else DARK_THEME

    else:
        user_input += event.unicode

def main():
    """Run the SmartCalculator app loop."""
    running = True
    while running:
        screen.fill(theme["bg"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_key(event)

        # Render input line
        input_surface = render_text(
            user_input,
            theme["input"],
            MAX_TEXT_WIDTH
        )
        screen.blit(
            input_surface,
            (LEFT_PADDING, CENTER_Y - TOP_INPUT_OFFSET)
        )

        # Draw separator line
        pygame.draw.line(
            screen,
            theme["line"],
            (LEFT_PADDING, CENTER_Y),
            (WIDTH - LEFT_PADDING, CENTER_Y),
            2
        )

        # Render result (right-aligned)
        color = (
            theme["error"]
            if last_result.startswith("Error")
            else theme["text"]
        )
        result_surface = render_text(last_result, color, MAX_TEXT_WIDTH)
        result_rect = result_surface.get_rect()
        result_rect.top = CENTER_Y + RESULT_TOP_OFFSET
        result_rect.right = WIDTH - RESULT_RIGHT_PADDING
        screen.blit(result_surface, result_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

