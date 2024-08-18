from settings import *
import math
import random
from os.path import join
import json
from movies import movies_dict
from animals import animals_dict
from cities import cities_dict
from songs import songs_dict
from actors import actors_dict
from riddles import riddles

# Setup display
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Riddle Me Hangman")
FPS = 60
CLOCK = pygame.time.Clock()

# Statistics
coins_available = 0
coins_played = 0
won_total = 0
lost_total = 0
hints_used = 0
longest_streak = 0
points = 0

# States
user_login = False
is_movies = False
is_animals = False
is_cities = False
is_songs = False
is_actors = False
guessed = []
choose = []
streak = 0

# Button Variables
RADIUS = 35
GAP = 25
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
HANGMAN_FONT = pygame.font.SysFont('timesnewroman', 70)
LETTER_FONT = pygame.font.SysFont('Corbel', 35, True)
WORD_FONT = pygame.font.SysFont('timesnewroman', 40)
TITLE_FONT = pygame.font.SysFont('timesnewroman', 50)
HINT_FONT = pygame.font.SysFont('timesnewroman', 30)
SMALLFONT = pygame.font.SysFont('Corbel', 35, True)
LOGINFONT = pygame.font.SysFont('Corbel', 60, True)
USERFONT = pygame.font.SysFont('Corbel', 40, True)
user_text = ""
user_name = []

# Hangman background
images = []
for i in range(7):
    image = pygame.image.load(join("assets", "images", "hangman" + str(i) + ".png"))
    images.append(image)

# Sound Setup
RIGHT_LETTER_SOUND = pygame.mixer.Sound(join("assets", "sound", "mixkit-modern-technology-select-3124.wav"))
WRONG_LETTER_SOUND = pygame.mixer.Sound(join("assets", "sound", "mixkit-on-or-off-light-switch-tap-2585.wav"))
COINS_ADD_SOUND = pygame.mixer.Sound(join("assets", "sound", "coins.mp3"))
NEED_COINS_SOUND = pygame.mixer.Sound(join("assets", "sound", "coin-bag.mp3"))
LOST_SOUND = pygame.mixer.Sound(join("assets", "sound", "wronganswer.mp3"))
VICTORY_SOUND = pygame.mixer.Sound(join("assets", "sound", "rightanswer.mp3"))
# set channel to prevent the music playing over itself and becoming distorted
# Music
pygame.mixer.music.load(join("assets", "sound", "GentleWavesOfSound.mp3"))
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
pygame.mixer.music.set_volume(0.2)

# Game Variables
hangman_status = 0

# Random Movies
random_movie = random.choice(list(movies_dict))
word_movies = random_movie.upper()
movie_title = movies_dict[random_movie]

# Random Animals
random_animal = random.choice(list(animals_dict))
word_animal = random_animal.upper()
animal_title = animals_dict[random_animal]

# Random Cities
random_city = random.choice(list(cities_dict))
word_city = random_city.upper()
city_title = cities_dict[random_city]

# Random Songs
random_song = random.choice(list(songs_dict))
word_song = random_song.upper()
song_title = songs_dict[random_song]

# Random Actors
random_actor = random.choice(list(actors_dict))
word_actor = random_actor.upper()
actor_title = actors_dict[random_actor]

# Set up fonts
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

# Function to render text
def render_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Riddles?
def riddle_me():
    # Game variables
    current_riddle = 0
    user_text = ''
    input_box = pygame.Rect(50, 500, 700, 40)
    input_box_active = False
    submit_button_rect = pygame.Rect(50, 550, 120, 40)
    back_button_rect = pygame.Rect(WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40)
    feedback = ''

    # Main game loop
    running = True
    while running:
        win.fill(LIGHT_BLUE)
        
        # Display the current riddle
        render_text(riddles[current_riddle]["riddle"], font, TEXT_COLOR, win, WIDTH // 2, HEIGHT // 2 - 50)
        
        # Draw input box
        pygame.draw.rect(win, INPUT_BOX_COLOR, input_box, 2)
        if input_box_active:
            txt_surface = font.render(user_text, True, TEXT_COLOR)
        else:
            txt_surface = font.render(user_text, True, TEXT_COLOR)
        win.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        
        # Draw submit button
        pygame.draw.rect(win, COLOR_DARK, submit_button_rect)
        render_text("Submit", button_font, WHITE, win, submit_button_rect.centerx, submit_button_rect.centery)

        # Draw Back Button
        pygame.draw.rect(win, COLOR_DARK, back_button_rect)
        render_text("Back", button_font, WHITE, win, back_button_rect.centerx, back_button_rect.centery)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_box_active = True
                else:
                    input_box_active = False
                if back_button_rect.collidepoint(event.pos):
                    reset_game()
                    
                if submit_button_rect.collidepoint(event.pos):
                    if user_text.lower() == riddles[current_riddle]["answer"]:
                        feedback = "Correct!"
                        current_riddle = (current_riddle + 1) % len(riddles)
                        user_text = ''
                    else:
                        feedback = "Incorrect. Try again!"
            
            if event.type == pygame.KEYDOWN:
                if input_box_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_text.lower() == riddles[current_riddle]["answer"]:
                            feedback = "Correct!"
                            current_riddle = (current_riddle + 1) % len(riddles)
                            user_text = ''
                        else:
                            feedback = "Incorrect. Try again!"
                    else:
                        user_text += event.unicode
        
        # Display feedback
        render_text(feedback, font, TEXT_COLOR, win, WIDTH // 2, HEIGHT // 2 + 50)

        # Update the display
        pygame.display.flip()

# Workaround to create a save file if there is none
def play():
    global user_login
    try:
        f = open("save.json")
    except FileNotFoundError:
        login()
    else:
        load()
        main_menu()

# Login
def login():
    while True:
        global user_text
        global user_login
        global user_name
        win.fill(LIGHT_BLUE)
        input_rect = pygame.Rect(350,300,700,70)
        color = pygame.Color('lightskyblue3')

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            mouse = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    # Remove the last character from the text if there's any
                    user_text = user_text[:-1]
                elif ev.key == pygame.K_RETURN:
                    # Optionally handle Enter key
                    user_name.append(user_text)
                    user_login = True
                    save()
                    main_menu()
                else:
                    # Append character to user_text
                    if ev.key == pygame.K_SPACE:
                        user_text += ' '
                    elif len(ev.unicode) == 1 and len(user_text) <= 26:  # Check if it's a printable character
                        user_text += ev.unicode

        pygame.draw.rect(win,color,input_rect,0)

        text_surface = LOGINFONT.render(user_text, True, BLACK)
        win.blit(text_surface, (input_rect.x + 5,input_rect.y + 5))

        input_rect.w = max(200,text_surface.get_width()+10)

        text_quit = SMALLFONT.render('Quit', True, COLOR)
        # MAIN Menu
        if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)
        # Quit
        win.blit(text_quit, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))

        text_welcome = TITLE_FONT.render(f"Enter Your Name", 1, BLACK)
        win.blit(text_welcome, (WIDTH/2 - text_welcome.get_width()/2, 50))

        pygame.display.update()

# Save Func
def save():
    game_state = {
        "points": points,
        "user_login": user_login,
        "user_name": user_name,
        "player_streak": streak,
        "player_longest_streak": longest_streak,
        "coins_available": coins_available,
        "coins_played": coins_played,
        "won_total": won_total,
        "lost_total": lost_total,
        "hints_used": hints_used
    }

    with open("save.json", "w") as f:
        json.dump(game_state, f)

# Load Func
def load():
    global points
    global streak
    global longest_streak
    global coins_available
    global coins_played
    global won_total
    global lost_total
    global hints_used
    global user_login
    global user_name
    with open("save.json", "r") as f:
        game_state = json.load(f)
        points = game_state["points"]
        user_login = game_state["user_login"]
        user_name = game_state["user_name"]
        streak = game_state["player_streak"]
        longest_streak = game_state["player_longest_streak"]
        coins_available = game_state["coins_available"]
        coins_played = game_state["coins_played"]
        won_total = game_state["won_total"]
        lost_total = game_state["lost_total"]
        hints_used = game_state["hints_used"]

# Calculate Longest Streak
def streak_add():
    global longest_streak
    if streak > longest_streak:
            longest_streak = streak

# Draw Function
def draw():
    win.fill(LIGHT_BLUE)
    global points
    global coins_available

    # Draw Title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # Draw Word
    display_word = ""
    for letter in choose:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ " if not letter.isspace() else "  "

    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Catagorie
    if is_movies == True:
        text_catagorie = HINT_FONT.render(f"'{movie_title}'", 1, BLACK)
        win.blit(text_catagorie, (WIDTH/2 - text_catagorie.get_width()/2-20, HEIGHT/2-250))
    if is_animals == True:
        text_catagorie = HINT_FONT.render(f"'{animal_title}'", 1, BLACK)
        win.blit(text_catagorie, (WIDTH/2 - text_catagorie.get_width()/2-20, HEIGHT/2-250))
    if is_cities == True:
        text_catagorie = HINT_FONT.render(f"'{city_title}'", 1, BLACK)
        win.blit(text_catagorie, (WIDTH/2 - text_catagorie.get_width()/2-20, HEIGHT/2-250))
    if is_songs == True:
        text_catagorie = HINT_FONT.render(f"'{song_title}'", 1, BLACK)
        win.blit(text_catagorie, (WIDTH/2 - text_catagorie.get_width()/2-20, HEIGHT/2-250))
    if is_actors == True:
        text_catagorie = HINT_FONT.render(f"'{actor_title}'", 1, BLACK)
        win.blit(text_catagorie, (WIDTH/2 - text_catagorie.get_width()/2-20, HEIGHT/2-250))

    # Draw Alphabet Buttons
    for letter in letters:
        x, y, ltr, visible = letter
        m_x, m_y = pygame.mouse.get_pos()
        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
        if visible and dis < RADIUS:
            pygame.draw.circle(win, DARK_BLUE, (x, y), RADIUS, 0)
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
        if visible and not dis < RADIUS:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 0)
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    # Draw Back and Reveal Buttons
    mouse = pygame.mouse.get_pos()
    text_back = SMALLFONT.render('Back', True, COLOR)
    text_hint = SMALLFONT.render('Hint', True, COLOR)

    # Back Button
    if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
        pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
    else: 
        pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)

    # Random Letter Reveal Button
    if WIDTH/3*2.64-150 <= mouse[0] <= WIDTH/3*2.64-60 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
        pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64-150, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
    else: 
        pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64-150, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)

    # Back Text
    win.blit(text_back, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))
    # Reveal Letter Text
    win.blit(text_hint, (WIDTH/3*2.64-137, HEIGHT/3*2.55-10))
    # Streak Text
    streak_text = HINT_FONT.render(f"Streak: {streak}", True, BLACK)
    win.blit(streak_text, (25, 25))
    # Available Coins Text
    text_total_coins = HINT_FONT.render(f"Your Coins: {coins_available}", 1, GOLD)
    win.blit(text_total_coins, (WIDTH/2+400, HEIGHT/2-335))
    # Points Text
    text_total_coins = HINT_FONT.render(f"Your Points: {points}", 1, BLACK)
    win.blit(text_total_coins, (WIDTH/2+400, HEIGHT/2-300))
    # Hangman Background
    win.blit(images[hangman_status], (150, 100))

    pygame.display.update()

# End display function
def display_message(message):
    pygame.time.delay(1000)
    win.fill(LIGHT_BLUE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)

# Stats Menu
def stats_menu():
    while True:

        win.fill(LIGHT_BLUE)
        text_stats_back = SMALLFONT.render('Back', True, COLOR)
        text_stats_longest_streak = SMALLFONT.render(f'Longest Streak:         {longest_streak}', True, BLACK)
        text_stats_won_total = SMALLFONT.render(f'Total Games Won:    {won_total}', True, BLACK)
        text_stats_lost_total = SMALLFONT.render(f'Total Games Lost:    {lost_total}', True, BLACK)
        text_stats_coins_used = SMALLFONT.render(f'Total Coins Used:     {coins_played}', True, BLACK)
        text_stats_hints_used = SMALLFONT.render(f'Total Hints Used:     {hints_used}', True, BLACK)
        text_stats_points = SMALLFONT.render(f'Total points:         {points}', True, BLACK)

        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64 + 90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                    main_menu()
        
        # Back
        if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)
        
        # Longest Streak
        win.blit(text_stats_longest_streak, (WIDTH/2-500, HEIGHT/2-250))
        # Won Total
        win.blit(text_stats_won_total, (WIDTH/2-500, HEIGHT/2-200))
        # Lost Total
        win.blit(text_stats_lost_total, (WIDTH/2-500, HEIGHT/2-150))
        # Coins Used
        win.blit(text_stats_coins_used, (WIDTH/2-500, HEIGHT/2-100))
        # Hints Used
        win.blit(text_stats_hints_used, (WIDTH/2-500, HEIGHT/2-50))
        # Back
        win.blit(text_stats_back, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))
        # Points
        win.blit(text_stats_points, (WIDTH/2-500, HEIGHT/2))

        pygame.display.update()

# Put game while loop in its own function
def main():
    global hangman_status
    global streak
    global points
    global coins_played
    global coins_available
    global won_total
    global lost_total
    global hints_used

    # Setup Game Loop
    run = True

    while run:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Back Button
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64 + 90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                        reset_game()
                # Reveal Button
                if WIDTH/3*2.64-150 <= mouse[0] <= WIDTH/3*2.64-60 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                    ...
                
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - mouse[0])**2 + (y - mouse[1])**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr in choose:
                                RIGHT_LETTER_SOUND.play()
                                if points <= 1000000000:
                                    points += 50

                            if ltr not in choose:
                                WRONG_LETTER_SOUND.play()
                                hangman_status += 1
                                points -= 20
        # Call Draw Function
        draw()

        # Check End Condition
        won = True
        for letter in choose:
            if letter not in guessed and not letter.isspace():
                won = False
                break
        
        # Won End Screen
        if won:
            VICTORY_SOUND.play()
            won_total += 1
            streak += 1
            coins_available += 10
            COINS_ADD_SOUND.play()
            display_message(f"YOU WON! Your streak is {streak} and got 10 Coins!")
            break
        
        # Lost End Screen
        if hangman_status == 6:
            LOST_SOUND.play()
            lost_total += 1
            streak = 0
            display_message(f"You lost. The word was {choose}.")
            break
    
    streak_add()
    save()
    reset_game()

# Reset Letters, Guessed List, Random Word
def reset_game():
    global choose
    global hangman_status
    # Movies
    global random_movie
    global word_movies
    global movie_title
    # Animals
    global random_animal
    global word_animal
    global animal_title
    # Cities
    global random_city
    global word_city
    global city_title
    # Songs
    global random_song
    global word_song
    global song_title
    # Actors
    global random_actor
    global word_actor
    global actor_title

    global is_movies
    global is_animals
    global is_cities
    global is_songs
    global is_actors

    global guessed
    global letters
    global i
    global x
    global y
    hangman_status = 0
    # Movies
    random_movie = random.choice(list(movies_dict))
    word_movies = random_movie.upper()
    movie_title = movies_dict[random_movie]
    # Animals
    random_animal = random.choice(list(animals_dict))
    word_animal = random_animal.upper()
    animal_title = animals_dict[random_animal]
    # Cities
    random_city = random.choice(list(cities_dict))
    word_city = random_city.upper()
    city_title = cities_dict[random_city]
    # Songs
    random_song = random.choice(list(songs_dict))
    word_song = random_song.upper()
    song_title = songs_dict[random_song]
    # Actors
    random_actor = random.choice(list(actors_dict))
    word_actor = random_actor.upper()
    actor_title = actors_dict[random_actor]

    is_movies = False
    is_animals = False
    is_cities = False
    is_songs = False
    is_actors = False

    choose = []
    guessed = []
    letters = []
    
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])
    main_menu()

# Main Menu Loop
def main_menu():

    while True:
        load()
        global points
        global streak
        global longest_streak
        global won_total
        global lost_total
        global coins_played
        global coins_available
        global hints_used
        global choose
        global is_movies
        global is_animals
        global is_cities
        global is_songs
        global is_actors

        win.fill(LIGHT_BLUE)

        # Font
        signfont = pygame.font.SysFont('Corbel', 20, True)
        text_quit = SMALLFONT.render('Quit', True, COLOR)
        text_movies = SMALLFONT.render('Movies', True, COLOR)
        text_animals = SMALLFONT.render('Animals', True, COLOR)
        text_cities = SMALLFONT.render('Cities', True, COLOR)
        text_songs = SMALLFONT.render('Songs', True, COLOR)
        text_actors = SMALLFONT.render('Actors', True, COLOR)
        text_streak = SMALLFONT.render('Your Streak: ' + str(streak), True, BLACK)
        text_stats = SMALLFONT.render('STATS', True, COLOR)
        text_total_coins = HINT_FONT.render(f"Your Coins: {coins_available}", 1, GOLD)
        text_points = HINT_FONT.render(f"Your Points: {points}", 1, BLACK)
        signed = signfont.render("Game by GJ Vlok", True, RAINBOW)
        
        # Main Menu Text
        text_welcome = TITLE_FONT.render(f"Welcome, {user_name[0]} to", 1, BLACK)
        win.blit(text_welcome, (WIDTH/2 - text_welcome.get_width()/2, 50))

        text_hangman = HANGMAN_FONT.render("RIDDLE ME HANGMAN", 1, LIGHT_BLUE)
        
        text_choose = TITLE_FONT.render("Choose a category", 1, BLACK)
        win.blit(text_choose, (WIDTH/2 - text_choose.get_width()/2, 250))

        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                save()
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # Something
                if WIDTH/3*0.67 <= mouse[0] <= WIDTH/3*0.67+780 and HEIGHT/3*0.6 <= mouse[1] <= HEIGHT/3*0.6+70:
                    riddle_me()
                # Quit
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                    save()
                    pygame.quit()
                    sys.exit()
                # Movies
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5 <= mouse[1] <= HEIGHT/3*1.5+40:
                    choose = word_movies
                    is_movies = True
                    main()
                # Animals
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+50 <= mouse[1] <= HEIGHT/3*1.5+90:
                    choose = word_animal
                    is_animals = True
                    main()
                # Cities
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+100 <= mouse[1] <= HEIGHT/3*1.5+140:
                    choose = word_city
                    is_cities = True
                    main()
                # Songs
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+150 <= mouse[1] <= HEIGHT/3*1.5+190:
                    choose = word_song
                    is_songs = True
                    main()
                # Actors
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+200 <= mouse[1] <= HEIGHT/3*1.5+240:
                    choose = word_actor
                    is_actors = True
                    main()
                # Stats
                if WIDTH/3*0.2 <= mouse[0] <= WIDTH/3*0.2+100 and HEIGHT/3*0.2 <= mouse[1] <= HEIGHT/3*0.2+50:
                    stats_menu()
        # Buttons
        # Something button
        if WIDTH/3*0.67 <= mouse[0] <= WIDTH/3*0.67+780 and HEIGHT/3*0.6 <= mouse[1] <= HEIGHT/3*0.6+70:
            pygame.draw.rect(win, RAINBOW, [WIDTH/3*0.67, HEIGHT/3*0.6, 780, 70], 0, 10, 10, 10, 10)
        else:
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*0.67, HEIGHT/3*0.6, 780, 70], 0, 10, 10, 10, 10)
        # Stats
        if WIDTH/3*0.2 <= mouse[0] <= WIDTH/3*0.2+100 and HEIGHT/3*0.2 <= mouse[1] <= HEIGHT/3*0.2+50: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*0.2, HEIGHT/3*0.2, 100, 50], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*0.2, HEIGHT/3*0.2, 100, 50], 0, 10, 10, 10, 10)
        # Quit button
        if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)
        # Category Movies
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5 <= mouse[1] <= HEIGHT/3*1.5+40: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5, 140, 40], 0, 10, 10, 10, 10)
        # Category Animals
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+50 <= mouse[1] <= HEIGHT/3*1.5+90: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5+50, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5+50, 140, 40], 0, 10, 10, 10, 10)
        # Category Cities
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+100 <= mouse[1] <= HEIGHT/3*1.5+140: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5+100, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5+100, 140, 40], 0, 10, 10, 10, 10)
        # Category Songs
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+150 <= mouse[1] <= HEIGHT/3*1.5+190: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5+150, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5+150, 140, 40], 0, 10, 10, 10, 10)
        # Category Actors
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+200 <= mouse[1] <= HEIGHT/3*1.5+240: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5+200, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5+200, 140, 40], 0, 10, 10, 10, 10)

        # Something
        win.blit(text_hangman, (WIDTH/3*0.67+10, HEIGHT/3*0.6-5))
        # Quit
        win.blit(text_quit, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))
        # Movies
        win.blit(text_movies, (WIDTH/3*1.3+20, HEIGHT/3*1.5+5))
        # Animals
        win.blit(text_animals, (WIDTH/3*1.3+10, HEIGHT/3*1.5+55))
        # Cities
        win.blit(text_cities, (WIDTH/3*1.3+30, HEIGHT/3*1.5+105))
        # Songs
        win.blit(text_songs, (WIDTH/3*1.3+25, HEIGHT/3*1.5+155))
        # Actors
        win.blit(text_actors, (WIDTH/3*1.3+20, HEIGHT/3*1.5+205))
        # Streak
        win.blit(text_streak, (WIDTH/3*1.08, HEIGHT/3*2.55+25))
        # STATS
        win.blit(text_stats, (WIDTH/3*0.2, HEIGHT/3*0.2+10))
        # Available Coins
        win.blit(text_total_coins, (WIDTH/2+400, HEIGHT/2-335))
        # Points
        win.blit(text_points, (WIDTH/2+400, HEIGHT/2-300))
        # Signed
        win.blit(signed, (WIDTH/2*0.88, HEIGHT/2*0.01))

        pygame.display.update()


if __name__ == "__main__": 
    play()
