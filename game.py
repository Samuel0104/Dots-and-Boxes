import pygame,colors as c
from squares import Box
from players import Player
from buttons import Button
from time import time

# =============================================================================
# Initialization

players = []
backgr = c.light
square = c.lightSquare
theme = Button()
fullScr = Button()

# =============================================================================
# Definition

"""
Screen 1
"""
def menu():
    global screen, ev, setting
    
    setting = Button()
    
    while True:
        width, height = screen.get_size()
        # Start
        start = Button(screen.get_rect().centerx - width//8,        # x-position
                       screen.get_rect().centery - 7*(height//28),  # y-position
                       width//4, height//14, c.menu)                # width, height, color
        # How To Play
        howTo = Button(screen.get_rect().centerx - width//8,
                       screen.get_rect().centery - 3*(height//28),
                       width//4, height//14, c.menu)
        # Credits
        creds = Button(screen.get_rect().centerx - width//8,
                       screen.get_rect().centery + (height//28),
                       width//4, height//14, c.menu)
        # Exit Game
        exits = Button(screen.get_rect().centerx - width//8,
                       screen.get_rect().centery + 5*(height//28),
                       width//4, height//14, c.menu)
        # Settings
        setting = Button(width - 70, height - 70, 50, 50, c.white, setting.selected)
        
        buttons = [start, howTo, creds, exits]
        
        # =============================================================================
        # Events
        
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            pygame.quit()
            return

        pos = pygame.mouse.get_pos()
        
        if not setting.selected:
            if any(b.collidepoint(pos) for b in buttons) or setting.collidepoint(pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if not setting.selected:
                if start.collidepoint(pos):
                    return colorSelect()
                if exits.collidepoint(pos):
                    pygame.quit()
                    return
            if setting.collidepoint(pos):
                setting.selected = not setting.selected
                
        # =============================================================================
        # Drawing objects
                
        screen.fill(backgr)
        
        # Start
        start.draw(screen, pos)
        f = font.render("START", True, c.white)
        fpos = f.get_rect()
        fpos.centerx = start.centerx
        fpos.centery = start.centery
        screen.blit(f, fpos)
        
        # How To Play
        howTo.draw(screen, pos)
        f = font.render("HOW TO PLAY", True, c.white)
        fpos = f.get_rect()
        fpos.centerx = howTo.centerx
        fpos.centery = howTo.centery
        screen.blit(f, fpos)
        
        # Credits
        creds.draw(screen, pos)
        f = font.render("CREDITS", True, c.white)
        fpos = f.get_rect()
        fpos.centerx = creds.centerx
        fpos.centery = creds.centery
        screen.blit(f, fpos)
        
        # Exit Game
        exits.draw(screen, pos)
        f = font.render("EXIT GAME", True, c.white)
        fpos = f.get_rect()
        fpos.centerx = exits.centerx
        fpos.centery = exits.centery
        screen.blit(f, fpos)
        
        # Settings
        setting.draw(screen, pos)
        if setting.selected:
            settings()
            
        pygame.display.flip()


"""
Screen 2
"""
def colorSelect():
    global ev, size, setting
    
    players.clear()
    size = 5
    cButtons = [Button(color=c) for c in c.colors]
    up = Button()
    down = Button()
    setting = Button()
    
    while True:
        width, height = screen.get_size()
        
        # Player Colors
        cButtons = [Button((width//4 - width//30) + (width//6 + width//30)*(i%3),   # x-position
                   100 + (height//6 + width//30)*(i//3),                            # y-position
                   width//6, height//6, b.color, b.selected)                        # width, height, color
                   for i, b in enumerate(cButtons)]
        # Play
        start = Button(7*width//12,
                       120 + height//3 + width//8,
                       width//6, height//18, c.play)
        # Back
        back = Button(width//4,
                      120 + height//3 + width//8,
                      width//6, height//18, c.back)
        # Increase Size
        up = Button(screen.get_rect().centerx - height//36,
                    108 + 5*(height//18) + width//8,
                    height//18, height//18, c.white, up.selected)
        # Decrease Size
        down = Button(screen.get_rect().centerx - height//36,
                      108 + 8*(height//18) + width//8,
                      height//18, height//18, c.white, down.selected)
        # Settings
        setting = Button(width - 70, height - 70, 50, 50, c.white, setting.selected)
        
        buttons = [start, back, up, down] + cButtons
        
        # =============================================================================
        # Events
        
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            pygame.quit()
            return
        
        pos = pygame.mouse.get_pos()
        
        if not setting.selected:
            if any(b.collidepoint(pos) for b in buttons) or setting.collidepoint(pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if not setting.selected: # Selecting or removing a player
                for b in cButtons:
                    if b.collidepoint(pos):
                        b.selected = not b.selected
                        if b.selected:
                            players.append(Player(b.color))
                        else:
                            for p in players:
                                if p.color == b.color:
                                    players.remove(p)
                                    
                if start.collidepoint(pos) and len(players) > 0:
                    return game()
                
                if back.collidepoint(pos):
                    return menu()
                
                if up.collidepoint(pos):
                    up.selected = True
                    size += 1 if size < 25 else 0 # Increase size up to 25x25
                    t1 = time()
                    
                if down.collidepoint(pos):
                    down.selected = True
                    size -= 1 if size > 3 else 0 # Decrease size up to 3x3
                    t2 = time()
                    
            if setting.collidepoint(pos):
                setting.selected = not setting.selected
                
        if up.selected and time() - t1 > 0.03:
            up.selected = False
        if down.selected and time() - t2 > 0.03:
            down.selected = False
            
        # =============================================================================
        # Drawing objects
            
        screen.fill(backgr)
        
        # Board Size
        f = font.render(f"{size}x{size}", True, c.gray)
        fpos = f.get_rect()
        fpos.centerx = screen.get_rect().centerx
        screen.blit(f, (fpos[0], 88 + 7*(height//18) + width//8))
        
        # Player Colors
        for b in cButtons:
            b.draw(screen, pos)
            
        # Play
        start.draw(screen, pos)
        f = font.render("PLAY", True, c.white)
        fpos = f.get_rect()
        fpos.centerx = start.centerx
        fpos.centery = start.centery
        screen.blit(f, fpos)
        
        # Back
        back.draw(screen, pos)
        f = font.render("BACK", True, c.white)
        fpos = f.get_rect()
        fpos.centerx = back.centerx
        fpos.centery = back.centery
        screen.blit(f, fpos)
        
        # Increase Size
        up.draw(screen, pos)
        if up.selected: # For the triangle/arrow
            pygame.draw.polygon(screen, c.node,
                                [(up.centerx, up.y + 13),
                                 (up.x + 6, up.y + up.height + 1),
                                 (up.x + up.width - 6, up.y + up.height + 1)])
        else:
            pygame.draw.polygon(screen, c.node,
                                [(up.centerx, up.y + 6),
                                 (up.x + 6, up.y + up.height - 6),
                                 (up.x + up.width - 6, up.y + up.height - 6)])

        # Decrease Size
        down.draw(screen, pos) # For the triangle/arrow
        if down.selected:
            pygame.draw.polygon(screen, c.node,
                                [(up.centerx, down.y + up.height + 1),
                                 (up.x + 6, down.y + 13),
                                 (up.x + up.width - 6, down.y + 13)])
        else:
            pygame.draw.polygon(screen, c.node,
                                [(up.centerx, down.y + up.height - 6),
                                 (up.x + 6, down.y + 6),
                                 (up.x + up.width - 6, down.y + 6)])

        # Settings
        setting.draw(screen, pos)
        if setting.selected:
            settings()
        pygame.display.flip()


"""
Screen 3
"""
def game():
    global ev, setting
    
    turn = 0
    boxes = [Box() for i in range(size**2)]
    setting = Button()
    
    while True:
        width, height = screen.get_size()
        m = (height - 40)//size
        setting = Button(width - 70, height - 70, 50, 50, c.white, setting.selected)
        for i, b in enumerate(boxes):
            b.adjust(m, size, i, square if b.color not in c.colors else b.color)
        player = players[turn%len(players)]
        
        ev = pygame.event.wait()        
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            pygame.quit()
            return
        
        pos = pygame.mouse.get_pos()
        
        if not setting.selected:
            if any(s.collidepoint(pos) and s.color == backgr for b in boxes for s in b.sides) or setting.collidepoint(pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if not setting.selected:
                bCounter = sCounter = 0
                for b in boxes:
                    for side in b.sides:
                        if side.collidepoint(pos) and side.color == backgr:
                            sCounter += 1
                            side.color = player.color
                            b.count += 1
                            if b.count == 4:
                                bCounter += 1
                                player.score += 1
                                b.color = player.color
                                turn -= 1 if bCounter == 1 else 0
                            turn += 1 if sCounter == 1 else 0
                            
            if setting.collidepoint(pos):
                setting.selected = not setting.selected
                
        screen.fill(backgr)
        
        for b in boxes:
            pygame.draw.rect(screen, b.color, b)
            for s in b.sides:
                if s.color not in c.colors:
                    s.color = backgr
                pygame.draw.rect(screen, s.color, s)
                
        for x in range(size + 1):
            for y in range(size + 1):
                pygame.draw.circle(screen, c.node, (m*x + 22, m*y + 22), 7 if size < 20 else 6)
                
        for i, p in enumerate(players):
            f = font.render(f"Player {i+1}    {p.score}", True, p.color)
            screen.blit(f, (m*size + 50, 40*i + 40))
            
        setting.draw(screen, pos)
        if setting.selected:
            settings()
        pygame.display.flip()


"""
Settings Box
"""
def settings():
    global backgr, square, screen, theme, fullScr, t3, t4
    
    width, height = screen.get_size()
    
    options = pygame.Rect(screen.get_rect().centerx - width//6, 100, width//3, height - 200)
    # Light/dark Mode
    theme = Button(options.centerx - width//12,
                   options.y + height//6,
                   width//6, height//14, c.settings, theme.selected)
    # Windowed/full Screen
    fullScr = Button(options.centerx - width//12,
                     options.centery - height//28,
                     width//6, height//14, c.settings, fullScr.selected)
    # Return To Main Menu
    main = Button(options.centerx - width//12,
                  options.y + options.height - height//6 - height//14,
                  width//6, height//14, c.settings)
    
    buttons = [theme, fullScr, main]
    
    # =============================================================================
    # Events
    
    pos = pygame.mouse.get_pos()
    
    if any(b.collidepoint(pos) for b in buttons) or setting.collidepoint(pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    if ev.type == pygame.MOUSEBUTTONDOWN:
        if theme.collidepoint(pos):
            theme.selected = True
            backgr = c.dark if backgr == c.light else c.light
            square = c.darkSquare if square == c.lightSquare else c.lightSquare
            t3 = time()
        
        if fullScr.collidepoint(pos):
            fullScr.selected = True
            pygame.time.delay(250)
            pygame.display.quit()
            if (width, height) == (780, 576):
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((780, 576))
            t4 = time()
            
        if main.collidepoint(pos):
            return menu()
        
    if theme.selected and time() - t3 > 0.03:
        theme.selected = False
    if fullScr.selected and time() - t4 > 0.03:
        fullScr.selected = False
            
    # =============================================================================
    # Drawing objects
        
    # Settings Box
    pygame.draw.rect(screen, c.gray, (options.centerx - width//6 - 5, 95, width//3 + 10, height - 190))
    pygame.draw.rect(screen, c.darkGray, options)
    
    # Light/dark Mode
    theme.draw(screen, pos)
    f = font.render("DARK" if backgr == c.dark else "LIGHT", True, c.white)
    fpos = f.get_rect()
    fpos.centerx = theme.centerx
    fpos.centery = theme.centery + (7 if theme.selected else 0)
    screen.blit(f, fpos)
    
    # Windowed/full Screen
    fullScr.draw(screen, pos)
    f = font.render("FULL SCREEN" if (width, height) != (780, 576) else "WINDOW", True, c.white)
    fpos = f.get_rect()
    fpos.centerx = fullScr.centerx
    fpos.centery = fullScr.centery + (7 if fullScr.selected else 0)
    screen.blit(f, fpos)
    
    # Return To Main Menu
    main.draw(screen, pos)
    f = font.render("MENU", True, c.white)
    fpos = f.get_rect()
    fpos.centerx = main.centerx
    fpos.centery = main.centery
    screen.blit(f, fpos)

# =============================================================================
# Execution

pygame.init()
screen = pygame.display.set_mode((780, 576))
pygame.display.set_caption("Dots&Boxes")
font = pygame.font.Font("impact.ttf", 34)
menu()