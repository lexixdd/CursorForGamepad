import pygame
import pyautogui
import sys

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        sys.exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    cursor_mode = False
    screen_w, screen_h = pyautogui.size()

    # --- Settings ---
    MOUSE_SENSITIVITY = 12
    MOUSE_DEADZONE = 0.12
    MOUSE_CURVE = 1.8

    SCROLL_SENSITIVITY = 8
    SCROLL_DEADZONE = 0.15
    SCROLL_CURVE = 1.5

    SELECT_BUTTON = 6   # Select/View
    A_BUTTON = 0        # Left click
    B_BUTTON = 1        # Right click
    LB_BUTTON = 4       # Hold to select text (drag)

    current_x, current_y = pyautogui.position()
    float_x, float_y = float(current_x), float(current_y)

    scroll_accumulator = 0.0
    is_dragging = False

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == SELECT_BUTTON:
                    cursor_mode = not cursor_mode
                    if cursor_mode:
                        cx, cy = pyautogui.position()
                        float_x, float_y = float(cx), float(cy)

                if event.button == LB_BUTTON and cursor_mode:
                    pyautogui.mouseDown(button='left')
                    is_dragging = True

                if event.button == B_BUTTON and cursor_mode and not is_dragging:
                    pyautogui.click(button='right')

            if event.type == pygame.JOYBUTTONUP:
                if event.button == LB_BUTTON and is_dragging:
                    pyautogui.mouseUp(button='left')
                    is_dragging = False

        if cursor_mode:
            # --- Left stick: cursor movement ---
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)

            x_val = apply_deadzone_curve(x_axis, MOUSE_DEADZONE, MOUSE_CURVE)
            y_val = apply_deadzone_curve(y_axis, MOUSE_DEADZONE, MOUSE_CURVE)

            if x_val != 0 or y_val != 0:
                float_x += x_val * MOUSE_SENSITIVITY
                float_y += y_val * MOUSE_SENSITIVITY

                float_x = max(0, min(screen_w - 1, float_x))
                float_y = max(0, min(screen_h - 1, float_y))

                pyautogui.moveTo(int(float_x), int(float_y))

            # --- Right stick: scrolling ---
            if not is_dragging:
                right_y = joystick.get_axis(3)
                scroll_val = apply_deadzone_curve(-right_y, SCROLL_DEADZONE, SCROLL_CURVE)

                if scroll_val != 0:
                    scroll_accumulator += scroll_val * SCROLL_SENSITIVITY
                    scroll_amount = int(scroll_accumulator)
                    if scroll_amount != 0:
                        pyautogui.scroll(scroll_amount)
                        scroll_accumulator -= scroll_amount

            # --- A button: left click (disabled while dragging) ---
            if joystick.get_button(A_BUTTON) and not is_dragging:
                pyautogui.click()
                pygame.time.wait(200)

        clock.tick(120)

    if is_dragging:
        pyautogui.mouseUp(button='left')

    pygame.quit()


def apply_deadzone_curve(value, deadzone, curve):
    if abs(value) < deadzone:
        return 0.0

    sign = 1 if value > 0 else -1
    normalized = (abs(value) - deadzone) / (1 - deadzone)
    normalized = min(1.0, normalized)
    curved = normalized ** curve

    return sign * curved


if __name__ == "__main__":
    main()