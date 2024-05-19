import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import random
import time
import os
from typing import List, Dict


class Audio:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def play(self, file: str, loops: int = 0):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops)

    def stop(self):
        pygame.mixer.music.stop()

    def volchange(self, volume: float):
        pygame.mixer.music.set_volume(volume)  # The set_volume range is from 0.00 to 1.00 (every 0.01)


# game constants
IMGAGE_SCALING = (5,5)
NUM_FOLDER_X_TRIALS = [2,1,1,1]
NUM_TRIALS = sum(NUM_FOLDER_X_TRIALS)
ALLOW_DUPLICATES = False

# font constants
DARK_TEAL = (21, 102, 105)
PINK = (255, 153, 153)
GRAY = (128, 128, 128)
FONT_SIZE = 132

# stats
accuracy = 0
trials_completed = 0
average_reaction_time = 0

# global game variables
key_mapping: Dict[int, int] = {}
screen: pygame.Surface
screen_size: tuple = (int, int)
img_1: pygame.Surface
img_2: pygame.Surface
img_3: pygame.Surface
img_4: pygame.Surface
trial_directory: str
all_trials: List[Dict[str, List[str]]] = []
selected_trials: List[tuple] = []
audio_player = Audio()


def initialize():
    """
    run initialization for game.
    """
    # load global variables
    global key_mapping
    global screen
    global screen_size
    global img_1, img_2, img_3, img_4
    global trial_directory
    global all_trials
    global selected_trials

    pygame.init()

    # configure keys
    key_mapping = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4}

    # set up screen
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Audio-Visual Experiment")
    screen_size = pygame.display.get_window_size()
    screen.fill((255,255,255))

    # create number fonts to go under images
    font_1 = pygame.font.SysFont('1', FONT_SIZE)
    img_1 = font_1.render('1', True, DARK_TEAL)

    font_2 = pygame.font.SysFont('2', FONT_SIZE)
    img_2 = font_2.render('2', True, DARK_TEAL)

    font_3 = pygame.font.SysFont('3', FONT_SIZE)
    img_3 = font_3.render('3', True, DARK_TEAL)

    font_4 = pygame.font.SysFont('4', FONT_SIZE)
    img_4 = font_4.render('4', True, DARK_TEAL)

    # get directory
    game_directory = os.path.dirname(os.path.realpath(__file__))

    # load trials
    trial_directory = game_directory + "\\trials"
    trial_folders = os.listdir(trial_directory)

    for folder in trial_folders:
        trial_dict: Dict[str, List[str]] = {}
        trial_dict[folder] = os.listdir(trial_directory + f"\\{folder}")
        all_trials.append(trial_dict)

    # generate list of trials to run
    for folder_num, num_trials in enumerate(NUM_FOLDER_X_TRIALS):
        folder_dict = all_trials[folder_num]
        break_dict = list(folder_dict.items())[0]
        folder_name = break_dict[0]
        folder_trials = break_dict[1]

        # check if program is asking for more trials than are available
        if not ALLOW_DUPLICATES:
            if num_trials > len(folder_trials):
                print(f"Program does not allow duplicates. Asking for {num_trials} trials when there are {len(folder_trials)} available in {folder_name}")
                exit(10)
        
        # pull random trials from folder
        for _ in range(num_trials):
            if not ALLOW_DUPLICATES:
                temp_trial = random.choice(folder_trials)
                folder_trials.remove(temp_trial)
            else:
                temp_trial = random.choice(folder_trials)
            
            selected_trials.append((folder_name, temp_trial))

    print(selected_trials)
            

def thank_you():
    """
    display the thank you screen and wait for user to press space.
    """
    # load global variables
    global screen

    # display thank you screen
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = font.render('Thank You', True, PINK)
    text_rect = text.get_rect(center=(screen_size[0]/2, screen_size[1]/2))

    font2 = pygame.font.SysFont(None, int(FONT_SIZE/2))
    text2 = font2.render('Press Space to continue', True, GRAY)
    text2_rect = text2.get_rect(center=(screen_size[0]/2, 5*screen_size[1]/6))
    
    screen.fill((255,255,255))
    screen.blit(text, text_rect)
    screen.blit(text2, text2_rect)
    pygame.display.update()

    # wait for user to press space
    response = None
    while response != pygame.K_SPACE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                response = event.key

    # clear screen
    screen.fill((255,255,255))


def audio_tuning():
    """
    screen where users can adjust audio levels before starting.
    press space to continue to next screen.
    """
    # load global variables
    global screen
    global audio_player

    # configure audio tuning screen
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = font.render('Audio Tuning', True, PINK)
    text_rect = text.get_rect(center=(screen_size[0]/2, screen_size[1]/3))

    font2 = pygame.font.SysFont(None, int(FONT_SIZE/2))
    text2 = font2.render('Press Space to continue', True, GRAY)
    text2_rect = text2.get_rect(center=(screen_size[0]/2, 5*screen_size[1]/6))

    slider = Slider(screen,
                    screen_size[0]/2 - screen_size[0]/6,
                    int(4*screen_size[1]/7),
                    screen_size[0]/3,
                    40,
                    min=0,
                    max=100,
                    step=1)
    output = TextBox(screen,
                     int(screen_size[0]/2) - 25,
                     int(4.5*screen_size[1]/7),
                     50,
                     50,
                     fontSize=30)
    output.disable()  # Act as label instead of textbox

    # loop audio sounds
    audio_player.play('sampleaudio.wav', -1)

    # wait for user to press space
    response = None
    while response != pygame.K_SPACE:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                response = event.key

        screen.fill((255,255,255))
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)

        output.setText(slider.getValue())
        audio_player.volchange(slider.getValue()/100)
        pygame_widgets.update(events)
        pygame.display.update()

    # clear screen
    screen.fill((255,255,255))
    audio_player.stop()


def instructions():
    """
    display instructions for how to play game.
    press space to continue to next screen.
    """
    # load global variables
    global screen

    # display instructions screen
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = font.render('Instructions', True, PINK)
    text_rect = text.get_rect(center=(screen_size[0]/2, screen_size[1]/2))

    font2 = pygame.font.SysFont(None, int(FONT_SIZE/2))
    text2 = font2.render('Press Space to continue', True, GRAY)
    text2_rect = text2.get_rect(center=(screen_size[0]/2, 4*screen_size[1]/5))
    
    screen.fill((255,255,255))
    screen.blit(text, text_rect)
    screen.blit(text2, text2_rect)
    pygame.display.update()

    # wait for user to press space
    response = None
    while response != pygame.K_SPACE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                response = event.key

    # clear screen
    screen.fill((255,255,255))


def run_trials():
    """
    """
    # load global variables
    global key_mapping
    global screen
    global screen_size
    global img_1, img_2, img_3, img_4
    global trial_directory
    global selected_trials
    global accuracy
    global trials_completed
    global average_reaction_time
    global audio_player

    ## loop for NUM_TRIALS
    for trial_num in range(NUM_TRIALS):
        # get next trial in list
        trial = selected_trials[trial_num]

        # load trial data
        trial_data = os.listdir(trial_directory + f"\\{trial[0]}\\{trial[1]}")
        images: List[str] = []
        audio: List[str] = []
        other: List[str] = []
        for file in trial_data:
            if file.endswith('.jpg') or file.endswith('.png'):
                images.append(file)
            elif file.endswith('.wav'):
                audio.append(file)
            else:
                other.append(file)

        # randomize image array
        random.shuffle(images)

        # determine correct image
        correct_key = -1
        for image in images:
            if image.__contains__("1"):
                correct_key = images.index(image) + 1

        # place images on screen
        converted_images = []
        for image in images:
            img = pygame.image.load(trial_directory + f"\\{trial[0]}\\{trial[1]}\\{image}")
            img = pygame.transform.scale(img, (screen_size[0]/IMGAGE_SCALING[0], screen_size[1]/IMGAGE_SCALING[1]))
            img.convert()
            converted_images.append(img)

        screen.blit(converted_images[0], (screen_size[0]/25, screen_size[1]/3))
        screen.blit(converted_images[1], (7*screen_size[0]/25, screen_size[1]/3))
        screen.blit(converted_images[2], (13*screen_size[0]/25, screen_size[1]/3))
        screen.blit(converted_images[3], (19*screen_size[0]/25, screen_size[1]/3))

        screen.blit(img_1, (3.3*screen_size[0]/25, 1.75*screen_size[1]/3))
        screen.blit(img_2, (9.3*screen_size[0]/25, 1.75*screen_size[1]/3))
        screen.blit(img_3, (15.3*screen_size[0]/25, 1.75*screen_size[1]/3))
        screen.blit(img_4, (21.3*screen_size[0]/25, 1.75*screen_size[1]/3))

        # display screen
        pygame.display.update()

        # play audio file
        audio_player.play(trial_directory + f"\\{trial[0]}\\{trial[1]}\\{audio[0]}")

        # Record start time
        start_time = time.time()

        # wait for user input
        response = None
        while response not in key_mapping:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    response = event.key

        # record reaction time
        reaction_time = time.time() - start_time
        average_reaction_time += reaction_time

        # check for correct selection
        selected_image = key_mapping.get(response)
        if selected_image == correct_key:
            answer = "correct"
            accuracy += 1
        else:
            answer = "incorrect"
            accuracy += 0
        trials_completed += 1

        # display feedback
        print(f"Trial {trial} - Reaction Time: {reaction_time:.2f}s, {answer}")

        # stop audio if still playing
        audio_player.stop()

## end loop for NUM_TRIALS


def clean_up():
    """
    
    """
    # load global constants
    global average_reaction_time
    global accuracy
    global trials_completed

    # display game stats
    average_reaction_time /= NUM_TRIALS
    print(f"Stats - Average Reaction Time: {average_reaction_time:.2f}s, Accuracy: {accuracy}/{trials_completed}")
    
    # kill pygame
    pygame.quit()


def main():
    """
    overall structure for game.
    """
    initialize()
    #thank_you()
    #audio_tuning()
    #instructions()
    #run_trials()
    clean_up()


if __name__ == "__main__":
    main()