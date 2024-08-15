import pygame, sys
import math
import random
from os.path import join
import json

# Add song change system?
# Add better visuals?
# be able to enter user name
# xp?
# just catagories no hints

# Setup display
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1400, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
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

# Button variables
user_login = False
game_saved = False
loaded = False
is_movies = False
is_animals = False
is_cities = False
hint_status = False
hint_status2 = False
hint_status3 = False
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

# fonts
HANGMAN_FONT = pygame.font.SysFont('timesnewroman', 70)
LETTER_FONT = pygame.font.SysFont('comicsans', 35, True)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 50)
HINT_FONT = pygame.font.SysFont('comicsans', 30)
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

# sound setup
RIGHT_LETTER_SOUND = pygame.mixer.Sound(join("assets", "sound", "mixkit-modern-technology-select-3124.wav"))
WRONG_LETTER_SOUND = pygame.mixer.Sound(join("assets", "sound", "mixkit-on-or-off-light-switch-tap-2585.wav"))
COINS_ADD_SOUND = pygame.mixer.Sound(join("assets", "sound", "coins.mp3"))
NEED_COINS_SOUND = pygame.mixer.Sound(join("assets", "sound", "coin-bag.mp3"))
LOST_SOUND = pygame.mixer.Sound(join("assets", "sound", "wronganswer.mp3"))
VICTORY_SOUND = pygame.mixer.Sound(join("assets", "sound", "rightanswer.mp3"))
# set channel to prevent the music playing over itself and becoming distorted
# music
pygame.mixer.music.load(join("assets", "sound", "GentleWavesOfSound.mp3"))
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)
pygame.mixer.music.set_volume(0.2)

# game variables
hangman_status = 0

movies = [["matrix", "1999", "Action, Sci-fi", "Keanu Reeves"], ["alien", "1979", "Horror, Sci-fi", "Sigourney Weaver"], 
        ["titanic", "1997", "Historical Drama, Romance", "Leonardo DiCaprio"], ["gladiator", "2000", "Action, Fantasy", "Russell Crowe"],
        ["robocop", "1987", "Action, Sci-Fi", "Peter Weller"], ["jaws", "1975", "Thriller", "Roy Scheider"],
        ["grease", "1978", "Musical, Romance", "John Trevolta"], ["rambo", "1982", "Action, Thriller", "Sylvester Stallone"],
        ["heat", "1995", "Crime Thriller", "Robert De Niro"], ["predator", "1987", "Action, Horror", "Arnold Schwarzenegger"],
        ["aladdin", "1992", "Animation, Romance", "Robin Williams"], ["shrek", "2000", "Animation, Fantasy", "Mike Myers"],
        ["aliens", "1986", "Action, Sci-Fi", "Sigourney Weaver"], ["ghost", "1990", "Romance, Supernatural", "Demi Moore"],
        ["speed", "1994", "Action, Thriller", "Keanu Reeves"], ["inception", "2000", "Sci-Fi, Drama", "Leonardo DiCaprio"],
        ["halloween", "1978", "Horror, Slasher", "Jamie Lee Curtis"], ["bambi", "1942", "Animation, Drama", "Donnie Dunagan"],
        ["poltergeist", "1982", "Horror, Fantasy", "Zelda Rubinstein"], ["goldfinger", "1964", "Action, Spy", "Sean Connery"],
        ["midsommer", "2019", "Drama, Thriller", "!"], ["while you were sleeping", "1995", "Comedy, Romance", "Sandra Bullock"],
        ["the lord of the rings", "2001 - 2003", "Adventure, Fantasy", "Elijah Wood"], ["up", "2009", "Animation, Comedy", "Edward Asner"],
        ["blade runner", "1982", "Action, Sci-Fi", "Harrison Ford"], ["blade", "1998", "Action, Horror", "Wesley Snipes"],
        ["the mummy", "1994", "Action, Adventure", "Brendan Fraser"], ["godzilla", "2014", "Sci-Fi, Thriller", "Bryan Cranston"]]

animals = [["cat", "Domestic", "Feline", "The owner of the house"], ["dog", "Domestic", "Canine", "Man's best friend"], 
        ["siberian tiger", "Siberia", "Feline", "The Largest"], ["wolf", "North America", "Canine", "Mate for life"],
        ["lion", "Africa", "Feline", "Only felines that live in a group"], ["red panda", "Himalayas, China", "Ailuridae", "Not related to the Giant Panda"],
        ["polar bear", "Artic", "Marine Mammal", "Largest carnivore on land"], ["capybara", "South America", "semiaquatic mammal", "Other animals use them as furniture"],
        ["elephant", "Africa", "Amarula", "Largest land animal"], ["leopard", "Africa", "Feline", "Spots are called Rosettes"],
        ["rhino", "Africa", "Mammal", "Over 3 tons"], ["platypus", "Australia", "Semiaquatic Mammal", "Venomous"],
        ["cape buffalo", "Africa", "Mammal", "Unpredictable and aggressive"], ["fish eagle", "Africa", "Large bird of prey", "Related to the North American Bald Eagle"],
        ["meerkat", "Africa", "Mongoose", "Immune to venom"], ["hippopotamus", "Sub-Saharan Africa", "Semiaquatic Mammal", "Third largest animal in the world"],
        ["beaver", "North America", "Semiaquatic Mammal", "Teeth are orange"], ["camel","Desert", "North Africa", "Only mammal that can drink salt water"],
        ["sea otter", "Coast of North Pacific Ocean", "Semiaquatic Mammal", "They'll steal your heart"], ["cheetah", "Africa", "Speedy", "Only males are social"],
        ["narwhal", "Artic", "Monodon monoceros", "Change color with age"], ["sloth", "Central America", "Slow poke", "Good at swimming"],
        ["great white shark", "Ocean", "Largest predatory fish", "Has toxic blood"], ["Orca", "Ocean", "Killer of the sea", "Sleeps with one eye open"],
        ["blue whale", "Ocean", "The Biggest", "One of the loudest voices on earth"], ["sperm whale", "Ocean", "Deep Diver", "Largest brain on the planet"],
        ["dolphins", "Ocean", "Scary", "Very chatty"], ["godzilla", "Japan", "Hollow Earth", "King of the Monsters"]]

cities = [["johannesburg", "Gauteng", "RSA", "Financial Capital"], ["East London", "Eastern Cape", "RSA", "The only river port"], 
        ["new york city", "NY", "USA", "More than 800 languages are spoken throughout the city"], ["los angeles", "California", "USA", "Hollywood"],
        ["olympia", "Washington", "USA", "Medal of Honor Memorial"], ["paris", "EU", "FR", "Notre-Dame Cathedral"],
        ["nice", "EU", "FR", "Fontaine du Soleil"], ["Barcelona", "EU", "Spain", "La Casa Batllo"],
        ["madrid", "EU", "Spain", "Puerta de Alcalá"], ["Berlin", "EU", "GER", "The Brandenburg Gate"],
        ["Hamburg", "EU", "GER", "St. Michaelis Church"], ["stuttgart", "EU", "GER", "Bismarck Tower"],
        ["london", "ENG", "U.K.", "Buckingham Palace"], ["manchester", "ENG", "U.K.", "Albert Memorial"],
        ["birmingham", "ENG", "U.K.", "Weoley Castle"], ["edinburgh", "SCT", "U.K.", "Scott Monument"],
        ["glasgow", "SCT", "U.K.", "Nelson Monument"], ["perth", "SCT", "U.K.", "Inchaffray Abbey"],
        ["sydney", "AUS", "Oceania", "The Vaucluse House"], ["melbourne", "AUS", "Oceania", "Shrine of Remembrance"],
        ["adelaide", "AUS", "Oceania", "The Mall's Balls Statue"], ["pretoria", "Gauteng", "RSA", "Voortrekker Monument"],
        ["cape town", "WC", "RSA", "Rhodes Memorial"], ["kuruman", "NW", "RSA", "The Eye"],
        ["kimberly", "NC", "RSA", "The Big Hole"], ["bloemfontein", "VS", "RSA", "The National Women's Monument"],
        ["dubai", "EoD", "UAE", "Burj Khalifa"], ["mexico city", "mexico", "NA", "Was built over water"]]

# Songs
songs = ["wish you a merry chrismas"]
random_word_songs = random.choice(songs)
word_songs = random_word_songs.upper()

# Random Movies
random_movie = random.choice(movies)
random_word_movies = random_movie[0]
word_movies = random_word_movies.upper()
movie_hint1 = random_movie[1]
movie_hint2 = random_movie[2]
movie_hint3 = random_movie[3]

# Random Animals
random_animal = random.choice(animals)
random_word_animals = random_animal[0]
word_animals = random_word_animals.upper()
animal_hint1 = random_animal[1]
animal_hint2 = random_animal[2]
animal_hint3 = random_animal[3]

# Random Cities
random_city = random.choice(cities)
random_word_cities = random_city[0]
word_cities = random_word_cities.upper()
cities_hint1 = random_city[1]
cities_hint2 = random_city[2]
cities_hint3 = random_city[3]

guessed = []
choose = []
streak = 0

# colors
random_red = random.randint(0, 255)
random_blue = random.randint(0, 255)
random_green = random.randint(0, 255)
RAINBOW = ((random_red), (random_blue), (random_green))
LIGHT_BLUE = (150, 150, 200)
BLACK = (0, 0, 0)
DARK_BLUE = (100, 0, 200)
COLOR_DARK = (50, 50, 50)
COLOR_LIGHT = (100, 100, 100)
COLOR = (255, 255, 255)
GOLD = ("gold")

# Something
def something():
    running = True
    while running:
        ...

def play():
    global user_login
    try:
        f = open("save.json")
    except FileNotFoundError:
        login()
    else:
        load()
        main_menu()

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
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_BACKSPACE and len(user_text) >= 1:
                user_text = user_text[:-1]
            if ev.type == pygame.KEYDOWN:
                user_text += ev.unicode
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN and len(user_text) >= 1 and not len(user_text) > 20:
                user_name.append(user_text[:-1])
                user_login = True
                save()
                main_menu()

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
        # quit
        win.blit(text_quit, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))

        text_welcome = TITLE_FONT.render(f"Enter Your Name", 1, BLACK)
        win.blit(text_welcome, (WIDTH/2 - text_welcome.get_width()/2, 50))

        pygame.display.update()

# Save Func
def save():
    game_state = {
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
        user_login = game_state["user_login"]
        user_name = game_state["user_name"]
        streak = game_state["player_streak"]
        longest_streak = game_state["player_longest_streak"]
        coins_available = game_state["coins_available"]
        coins_played = game_state["coins_played"]
        won_total = game_state["won_total"]
        lost_total = game_state["lost_total"]
        hints_used = game_state["hints_used"]

# Cal longest streak
def streak_add():
    global longest_streak
    if streak > longest_streak:
            longest_streak = streak

# Draw function
def draw():
    win.fill(LIGHT_BLUE)
    global hint_status
    global hint_status2
    global hint_status3
    global coins_available
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in choose:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ " if not letter.isspace() else "  "

    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Add Hint button to show or hide hints
    # Draw Hints
    if hint_status == True and is_movies == True:
        text_hint1 = HINT_FONT.render("Hint 1: " + movie_hint1, 1, BLACK)
        win.blit(text_hint1, (WIDTH/2 - text_hint1.get_width()/2-20, HEIGHT/2+180))
    elif hint_status == True and is_animals == True:
        text_hint1 = HINT_FONT.render("Hint 1: " + animal_hint1, 1, BLACK)
        win.blit(text_hint1, (WIDTH/2 - text_hint1.get_width()/2-20, HEIGHT/2+180))
    elif hint_status == True and is_cities == True:
        text_hint1 = HINT_FONT.render("Hint 1: " + cities_hint1, 1, BLACK)
        win.blit(text_hint1, (WIDTH/2 - text_hint1.get_width()/2-20, HEIGHT/2+180))
    else:
        text_hint1 = HINT_FONT.render("Hint 1", 1, BLACK)
        win.blit(text_hint1, (WIDTH/2 - text_hint1.get_width()/2-20, HEIGHT/2+180))

    if hint_status2 == True and is_movies == True:
        text_hint2 = HINT_FONT.render("Hint 2: " + movie_hint2, 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+230))
    elif hint_status2 == True and is_animals == True:
        text_hint2 = HINT_FONT.render("Hint 2: " + animal_hint2, 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+230))
    elif hint_status2 == True and is_cities == True:
        text_hint2 = HINT_FONT.render("Hint 2: " + cities_hint2, 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+230))
    else:
        text_hint2 = HINT_FONT.render("Hint 2", 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+230))

    if hint_status3 == True and is_movies == True:
        text_hint2 = HINT_FONT.render("Hint 3: " + movie_hint3, 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+280))
    elif hint_status3 == True and is_animals == True:
        text_hint2 = HINT_FONT.render("Hint 3: " + animal_hint3, 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+280))
    elif hint_status3 == True and is_cities == True:
        text_hint2 = HINT_FONT.render("Hint 3: " + cities_hint3, 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+280))
    else:
        text_hint2 = HINT_FONT.render("Hint 3", 1, BLACK)
        win.blit(text_hint2, (WIDTH/2 - text_hint2.get_width()/2-20, HEIGHT/2+280))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        m_x, m_y = pygame.mouse.get_pos()
        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
        if visible and dis < RADIUS:
            pygame.draw.circle(win, DARK_BLUE, (x, y), RADIUS, 7)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
        if visible and not dis < RADIUS:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 7)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    # draw back button
    mouse = pygame.mouse.get_pos()
    text_back = SMALLFONT.render('Back', True, COLOR)
    hint_text = SMALLFONT.render('Hint', True, COLOR)

    # Back
    if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
        pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
    else: 
        pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)
    # Hint 1
    if WIDTH/3*2.64-110 <= mouse[0] <= WIDTH/3*2.64-20 and HEIGHT/3*2.55-60 <= mouse[1] <= HEIGHT/3*2.55-20 and coins_available >= 10: 
        pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64-110, HEIGHT/3*2.55-60, 90, 40], 0, 10, 10, 10, 10)
    else: 
        pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64-110, HEIGHT/3*2.55-60, 90, 40], 0, 10, 10, 10, 10)
    # Hint 2
    if WIDTH/3*2.64-110 <= mouse[0] <= WIDTH/3*2.64-20 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25 and coins_available >= 10: 
        pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64-110, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
    else: 
        pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64-110, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)
    # Hint 3
    if WIDTH/3*2.64-110 <= mouse[0] <= WIDTH/3*2.64-20 and HEIGHT/3*2.55+30 <= mouse[1] <= HEIGHT/3*2.55+70 and coins_available >= 10: 
        pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64-110, HEIGHT/3*2.55+30, 90, 40], 0, 10, 10, 10, 10) 
    else: 
        pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64-110, HEIGHT/3*2.55+30, 90, 40], 0, 10, 10, 10, 10)

    # Back
    win.blit(text_back, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))
    # hint 1
    win.blit(hint_text, (WIDTH/3*2.64-97, HEIGHT/3*2.55-55))
    # hint 2
    win.blit(hint_text, (WIDTH/3*2.64-97, HEIGHT/3*2.55-10))
    # hint 3
    win.blit(hint_text, (WIDTH/3*2.64-97, HEIGHT/3*2.55+35))
    # streak
    streak_text = HINT_FONT.render(f"Streak: {streak}", True, BLACK)
    win.blit(streak_text, (25, 25))
    # Available Coins
    text_total_coins = HINT_FONT.render(f"Your Coins: {coins_available}", 1, GOLD)
    win.blit(text_total_coins, (WIDTH/2+400, HEIGHT/2-335))
    
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

        pygame.display.update()

# Put game while loop in its own function
def main():
    global hangman_status # so the function can access it within this loop
    global streak
    global hint_status
    global hint_status2
    global hint_status3
    global coins_played
    global coins_available
    global won_total
    global lost_total
    global hints_used
    # setup game loop
    run = True

    while run:
        CLOCK.tick(FPS)
        # Check for events and enable the quit function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Check for mouse press
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Back
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64 + 90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                        reset_game()
                # Hint 3
                if WIDTH/3*2.64-110 <= mouse[0] <= WIDTH/3*2.64-20 and HEIGHT/3*2.55+30 <= mouse[1] <= HEIGHT/3*2.55+70:
                    if coins_available >= 10:
                        coins_available -= 10
                        coins_played += 10
                        hint_status3 = True
                        hints_used += 1
                    else:
                        NEED_COINS_SOUND.play()

                # Hint 2
                if WIDTH/3*2.64-110 <= mouse[0] <= WIDTH/3*2.64-20 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+30:
                    if coins_available >= 10:
                        coins_available -= 10
                        coins_played += 10
                        hint_status2 = True
                        hints_used += 1
                    else:
                        NEED_COINS_SOUND.play()

                # Hint 1
                if WIDTH/3*2.64-110 <= mouse[0] <= WIDTH/3*2.64-20 and HEIGHT/3*2.55-60 <= mouse[1] <= HEIGHT/3*2.55-20:
                    if coins_available >= 10:
                        coins_available -= 10
                        coins_played += 10
                        hint_status = True
                        hints_used += 1
                    else:
                        NEED_COINS_SOUND.play()
                
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - mouse[0])**2 + (y - mouse[1])**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr in choose:
                                RIGHT_LETTER_SOUND.play()

                            if ltr not in choose:
                                WRONG_LETTER_SOUND.play()
                                hangman_status += 1
        # call draw function
        draw()

        # Check end condition
        won = True
        for letter in choose:
            if letter not in guessed and not letter.isspace():
                won = False
                break
        
        # Won end screen
        if won:
            VICTORY_SOUND.play()
            won_total += 1
            streak += 1
            coins_available += 10
            COINS_ADD_SOUND.play()
            display_message(f"YOU WON! Your streak is {streak} and got 10 Coins!")
            break
        
        # Lost end screen
        if hangman_status == 6:
            LOST_SOUND.play()
            lost_total += 1
            streak = 0
            display_message(f"You lost. The word was {choose}.")
            break
    
    streak_add()
    save()
    reset_game()

# reset letters, guessed list, random word
def reset_game():
    global choose
    global hangman_status
    global hint_status
    global hint_status2
    global hint_status3
    # Movies
    global random_movie
    global word_movies
    global movie_hint1
    global movie_hint2
    # Animals
    global random_animal
    global word_animals
    global animal_hint1
    global animal_hint2
    # Cities
    global random_city
    global word_cities
    global cities_hint1
    global cities_hint2
    # Songs
    global word_songs
    global random_word_songs

    global is_movies
    global is_animals
    global is_cities

    global game_saved
    global loaded
    global guessed
    global letters
    global i
    global x
    global y
    hangman_status = 0
    # Movies
    random_movie = random.choice(movies)
    random_word_movies = random_movie[0]
    word_movies = random_word_movies.upper()
    movie_hint1 = random_movie[1]
    movie_hint2 = random_movie[2]
    # Animals
    random_animal = random.choice(animals)
    random_word_animals = random_animal[0]
    word_animals = random_word_animals.upper()
    animal_hint1 = random_animal[1]
    animal_hint2 = random_animal[2]
    # Cities
    random_city = random.choice(cities)
    random_word_cities = random_city[0]
    word_cities = random_word_cities.upper()
    cities_hint1 = random_city[1]
    cities_hint2 = random_city[2]
    # Songs
    random_word_songs = random.choice(songs)
    word_songs = random_word_songs

    is_movies = False
    is_animals = False
    is_cities = False

    # Hint
    hint_status = False
    hint_status2 = False
    hint_status3 = False

    game_saved = False
    loaded = False

    choose = []
    guessed = []
    letters = []
    
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])
    main_menu()

# Main menu loop
def main_menu():

    while True:
        CLOCK.tick(FPS)
        load()
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
        global game_saved
        global loaded

        win.fill(LIGHT_BLUE)

        # font
        signfont = pygame.font.SysFont('Corbel', 20, True)
        boldfont = pygame.font.SysFont('Comicsans', 40, True)
        text_quit = SMALLFONT.render('Quit', True, COLOR)
        text_movies = SMALLFONT.render('Movies', True, COLOR)
        text_animals = SMALLFONT.render('Animals', True, COLOR)
        text_cities = SMALLFONT.render('Cities', True, COLOR)
        text_streak = boldfont.render('Your Streak: ' + str(streak), True, BLACK)
        text_save = SMALLFONT.render('Save', True, COLOR)
        text_saved = SMALLFONT.render('Game Saved', True, BLACK)
        text_load = SMALLFONT.render('Load', True, COLOR)
        text_loaded = SMALLFONT.render('Game Loaded', True, BLACK)
        text_stats = SMALLFONT.render('STATS', True, COLOR)
        signed = signfont.render('Game by GJ Vlok', True, RAINBOW)
        
        # Main Menu Text
        text_welcome = TITLE_FONT.render(f"Welcome, {user_name[0]} to", 1, BLACK)
        win.blit(text_welcome, (WIDTH/2 - text_welcome.get_width()/2, 50))

        text_hangman = HANGMAN_FONT.render("RIDDLE ME HANGMAN", 1, LIGHT_BLUE)
        
        text_choose = TITLE_FONT.render('Choose a catagory', 1, BLACK)
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
                    choose = word_songs
                    main()
                # Save
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-115 <= mouse[1] <= HEIGHT/3*2.55-85:
                    game_saved = True
                    save()
                # Load
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-65 <= mouse[1] <= HEIGHT/3*2.55-25:
                    loaded = True
                    load()
                # Quit
                if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25:
                    save()
                    pygame.quit()
                # Movies
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5 <= mouse[1] <= HEIGHT/3*1.5+40:
                    choose = word_movies
                    is_movies = True
                    main()
                # Animals
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+50 <= mouse[1] <= HEIGHT/3*1.5+90:
                    choose = word_animals
                    is_animals = True
                    main()
                # Cities
                if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+100 <= mouse[1] <= HEIGHT/3*1.5+140:
                    choose = word_cities
                    is_cities = True
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
        # Save button
        if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-115 <= mouse[1] <= HEIGHT/3*2.55-85: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-115, 90, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-115, 90, 40], 0, 10, 10, 10, 10)
        # Load
        if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-65 <= mouse[1] <= HEIGHT/3*2.55-25: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-65, 90, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-65, 90, 40], 0, 10, 10, 10, 10)
        # Quit button
        if WIDTH/3*2.64 <= mouse[0] <= WIDTH/3*2.64+90 and HEIGHT/3*2.55-15 <= mouse[1] <= HEIGHT/3*2.55+25: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*2.64, HEIGHT/3*2.55-15, 90, 40], 0, 10, 10, 10, 10)
        # Catagory Movies
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5 <= mouse[1] <= HEIGHT/3*1.5+40: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5, 140, 40], 0, 10, 10, 10, 10)
        # Catagory Animals
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+50 <= mouse[1] <= HEIGHT/3*1.5+90: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5+50, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5+50, 140, 40], 0, 10, 10, 10, 10)
        # Catagory Cities
        if WIDTH/3*1.3 <= mouse[0] <= WIDTH/3*1.3+140 and HEIGHT/3*1.5+100 <= mouse[1] <= HEIGHT/3*1.5+140: 
            pygame.draw.rect(win, COLOR_LIGHT, [WIDTH/3*1.3, HEIGHT/3*1.5+100, 140, 40], 0, 10, 10, 10, 10) 
        else: 
            pygame.draw.rect(win, COLOR_DARK, [WIDTH/3*1.3, HEIGHT/3*1.5+100, 140, 40], 0, 10, 10, 10, 10)

        # Somthing
        win.blit(text_hangman, (WIDTH/3*0.67+10, HEIGHT/3*0.6-5))
        # Save
        win.blit(text_save, (WIDTH/3*2.64+10, HEIGHT/3*2.55-110))
        # Load
        win.blit(text_load, (WIDTH/3*2.64+8, HEIGHT/3*2.55-60))
        # quit
        win.blit(text_quit, (WIDTH/3*2.64+10, HEIGHT/3*2.55-10))
        # movies
        win.blit(text_movies, (WIDTH/3*1.3+20, HEIGHT/3*1.5+5))
        # animals
        win.blit(text_animals, (WIDTH/3*1.3+10, HEIGHT/3*1.5+55))
        # cities
        win.blit(text_cities, (WIDTH/3*1.3+30, HEIGHT/3*1.5+105))
        # streak
        win.blit(text_streak, (WIDTH/3*1.08, HEIGHT/3*2.55))
        # STATS
        win.blit(text_stats, (WIDTH/3*0.2, HEIGHT/3*0.2+10))
        # Available Coins
        text_total_coins = HINT_FONT.render(f"Your Coins: {coins_available}", 1, GOLD)
        win.blit(text_total_coins, (WIDTH/2+400, HEIGHT/2-335))

        if game_saved == True:
            win.blit(text_saved, (WIDTH/3*2.64-220, HEIGHT/3*2.55-112))
        if loaded == True:
            win.blit(text_loaded, (WIDTH/3*2.64-220, HEIGHT/3*2.55-62))
        
        win.blit(signed, (WIDTH/2*0.88, HEIGHT/2*0.01))

        pygame.display.update()


if __name__ == "__main__": 
    play()
