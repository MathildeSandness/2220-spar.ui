import pygame
import sys
from loader import load_all_lists

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spar Collection UI")

FONT = pygame.font.SysFont("arial", 24)
SMALL = pygame.font.SysFont("arial", 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 200)

ONLINE = True

# Load all lists
list_queue = load_all_lists()
shopping_list = list_queue.pop(0) if list_queue else None

confirm_deliver = False


# -----------------------------
# Triangle drawing
# -----------------------------
def draw_triangle_up(x, y):
    points = [(x, y+20), (x+20, y+20), (x+10, y)]
    pygame.draw.polygon(screen, BLACK, points)
    return pygame.Rect(x, y, 20, 20)


def draw_triangle_down(x, y):
    points = [(x, y), (x+20, y), (x+10, y+20)]
    pygame.draw.polygon(screen, BLACK, points)
    return pygame.Rect(x, y, 20, 20)


# -----------------------------
# Header (always visible)
# -----------------------------
def draw_header(worker_id, list_id):
    # Online/offline indicator on RIGHT side
    color = GREEN if ONLINE else RED
    pygame.draw.rect(screen, color, (540, 20, 40, 40))
    pygame.draw.rect(screen, BLACK, (540, 20, 40, 40), 2)

    worker = FONT.render(f"Worker ID: {worker_id}", True, BLACK)
    screen.blit(worker, (20, 25))

    listid = FONT.render(f"List ID: {list_id}", True, BLACK)
    screen.blit(listid, (20, 65))


# -----------------------------
# Items
# -----------------------------
def draw_items(shopping_list):
    y = 120
    for item in shopping_list.items:
        pygame.draw.rect(screen, LIGHT_GRAY, (20, y, 560, 60))
        pygame.draw.rect(screen, BLACK, (20, y, 560, 60), 2)

        qty = SMALL.render(str(item.requested), True, BLACK)
        screen.blit(qty, (40, y + 20))

        name = SMALL.render(item.name, True, BLACK)
        screen.blit(name, (120, y + 20))

        avail = SMALL.render(f"Available: {item.available}", True, BLACK)
        screen.blit(avail, (300, y + 20))

        item.up_button = draw_triangle_up(450, y + 5)
        item.down_button = draw_triangle_down(450, y + 30)

        y += 70


# -----------------------------
# Deliver button
# -----------------------------
def draw_deliver_button():
    pygame.draw.rect(screen, BLUE, (150, 700, 300, 60))
    pygame.draw.rect(screen, BLACK, (150, 700, 300, 60), 2)
    text = FONT.render("DELIVER", True, WHITE)
    screen.blit(text, (230, 715))


# -----------------------------
# Confirm dialog
# -----------------------------
def draw_confirm_dialog():
    pygame.draw.rect(screen, WHITE, (50, 250, 500, 200))
    pygame.draw.rect(screen, BLACK, (50, 250, 500, 200), 3)

    msg = FONT.render("Are you sure you want to deliver?", True, BLACK)
    screen.blit(msg, (70, 280))

    yes_rect = pygame.Rect(100, 350, 150, 50)
    no_rect = pygame.Rect(350, 350, 150, 50)

    pygame.draw.rect(screen, GREEN, yes_rect)
    pygame.draw.rect(screen, BLACK, yes_rect, 2)
    pygame.draw.rect(screen, RED, no_rect)
    pygame.draw.rect(screen, BLACK, no_rect, 2)

    screen.blit(FONT.render("YES", True, WHITE), (140, 360))
    screen.blit(FONT.render("NO", True, WHITE), (400, 360))

    return yes_rect, no_rect


# -----------------------------
# Quantity update
# -----------------------------
def update_item_quantity(item, direction):
    if direction == "up" and item.available < item.requested:
        item.available += 1
    elif direction == "down" and item.available > 0:
        item.available -= 1


# -----------------------------
# Main UI loop
# -----------------------------
def ui_loop():
    global confirm_deliver, shopping_list

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        # -----------------------------
        # Handle events FIRST
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                # Confirm dialog
                if confirm_deliver:
                    if yes_rect.collidepoint(pos):
                        # Load next list if available
                        if list_queue:
                            shopping_list = list_queue.pop(0)
                        else:
                            shopping_list = None
                        confirm_deliver = False
                    elif no_rect.collidepoint(pos):
                        confirm_deliver = False
                    continue

                # Deliver button
                if pygame.Rect(150, 700, 300, 60).collidepoint(pos):
                    confirm_deliver = True
                    continue

                # Item buttons
                if shopping_list is not None:
                    for item in shopping_list.items:
                        if item.up_button.collidepoint(pos):
                            update_item_quantity(item, "up")
                        if item.down_button.collidepoint(pos):
                            update_item_quantity(item, "down")

        # -----------------------------
        # Drawing
        # -----------------------------
        screen.fill(WHITE)

        # Header ALWAYS visible
        worker_id = shopping_list.worker_id if shopping_list else "WORKER-001"
        list_id = shopping_list.list_id if shopping_list else "NO LIST"
        draw_header(worker_id, list_id)

        # If no list found
        if shopping_list is None:
            msg = FONT.render("No list found", True, BLACK)
            screen.blit(msg, (200, 350))
            pygame.display.flip()
            continue

        # Draw items + deliver button
        draw_items(shopping_list)
        draw_deliver_button()

        # Confirm dialog
        if confirm_deliver:
            yes_rect, no_rect = draw_confirm_dialog()
            draw_header(worker_id, list_id)  # redraw header on top

        pygame.display.flip()


