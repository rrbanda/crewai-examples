import yaml
import os
import pygame
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ✅ Go one level up
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")  # ✅ New location!
TASKS_PATH = os.path.join(BASE_DIR, "src", "tasks.yaml")
AGENTS_PATH = os.path.join(BASE_DIR, "src", "agents.yaml")

def load_yaml(file_path):
    """Loads a YAML file and returns its content as a dictionary."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Config file not found: {file_path}")

    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def load_config():
    return load_yaml(CONFIG_PATH)  # ✅ Load config from config folder

def load_tasks():
    return load_yaml(TASKS_PATH)

def load_agents():
    return load_yaml(AGENTS_PATH)

### ✅ Fix: Add `show_animation` function ###
class CartoonAnimation:
    """Class to show a looping animation while waiting for a process."""
    def __init__(self, image_path):
        self.image_path = image_path
        self.running = False
        self.thread = None

    def _run_animation(self):
        pygame.init()
        screen = pygame.display.set_mode((500, 300))  # ✅ Adjust width/height as needed
        pygame.display.set_caption("Loading...")
        clock = pygame.time.Clock()
        animation = pygame.image.load(self.image_path)

        while self.running:
            screen.fill((255, 255, 255))
            screen.blit(animation, (50, 50))  # ✅ Adjust positioning
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(30)  # ✅ Control frame rate

        pygame.quit()

    def start(self):
        """Start the animation in a separate thread."""
        if self.thread and self.thread.is_alive():
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_animation)
        self.thread.start()

    def stop(self):
        """Stop the animation."""
        self.running = False
        if self.thread:
            self.thread.join()

# ✅ Function to be used in LLM calls
def show_animation():
    animation = CartoonAnimation("assets/tom_and_jerry.gif")
    animation.start()
    return animation  # ✅ Return instance so we can stop it later
