import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1500, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar system simulation")

FONT = pygame.font.SysFont("New Times Roman", 27)

yellow = (255,215, 0)
dark_grey = (110, 110, 110)
pale_yellow = (238, 220, 130)
blue_greenbrown = (30, 144, 255)
reddish_brown = (178, 34, 34)
orange_whitebands = (210, 163, 96)
pale_gold = (244, 164, 96)
pale_cyan = (175, 238, 238)
deep_blue = (65, 105, 225)
class planets:

    AU = 149.6e6 * 1000
    G = 6.67428e-11
    Scale = 20/ AU
    Timestep = 86400

    def __init__(self, x, y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.DistanceToSun = 0

        self.x_velocity = 0
        self.y_velocity = 0
    
    def draw(self, win):
        x = self.x * self.Scale + WIDTH / 2
        y = self.y * self.Scale + HEIGHT / 2
        if len(self.orbit) > 2:
            update_points = []
            for point in self.orbit:
                x, y = point 
                x = self.x * self.Scale + WIDTH / 2
                y = self.y * self.Scale + HEIGHT / 2
                update_points.append((x,y))

            pygame.draw.lines(win, self.colour, False, update_points, 2)
        
        pygame.draw.circle(win, self.colour, (x,y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f'{round(self.DistanceToSun/1000, 1)}km', 1, pale_cyan)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x , other_y = other.x , other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.DistanceToSun = distance

        force = (self.G * self.mass * other.mass)/distance**2
        angle = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(angle)
        force_y = force * math.sin(angle)

        return force_x, force_y

    def updated_position(self, plan):
        total_fx = total_fy = 0
        for planet in plan:
            if self == planet:
                continue

            fx , fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += (total_fx * self.Timestep )/ self.mass
        self.y_velocity += (total_fy * self.Timestep )/ self.mass

        self.x += self.x_velocity * self.Timestep
        self.y += self.y_velocity * self.Timestep
        self.orbit.append((self.x, self.y))

def main():

    run = True
    paused = False
    clock = pygame.time.Clock()

    sun = planets(0, 0, 30, yellow, 1.98892 * 10** 30)
    sun.sun = True

    earth = planets(1 * planets.AU, 0, 7, blue_greenbrown, 5.9742 * 10 **24)
    earth.y_velocity = 29.783 * 1000
    
    mars = planets(-1.524 * planets.AU, 0, 4, reddish_brown, 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    mercury = planets(0.387 * planets.AU, 0, 3, dark_grey, 3.30 * 10**23)
    mercury.y_velocity = -47.4 * 1000
    
    venus = planets(0.723 * planets.AU, 0, 7, pale_yellow, 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

    jupiter = planets(5.2 *planets.AU, 0, 20, orange_whitebands, 1.898 * 10**27)
    jupiter.y_velocity = 13.07 * 1000

    saturn = planets(9.58 *planets.AU, 0, 18, pale_gold, 5.68 * 10 **26)
    saturn.y_velocity = 9.69 * 1000

    uranus = planets(19.22 *planets.AU, 0, 12, pale_cyan, 8.68 * 10 ** 25)
    uranus.y_velocity = 6.81 * 1000

    neptune = planets(30.05 *planets.AU, 0, 10, deep_blue, 1.024 * 10 ** 26)
    neptune.y_velocity = 5.43 * 1000

    planet_list = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune]
    while run:
        
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    planets.Scale *= 1.1
                elif event.y < 0:
                    planets.Scale /= 1.1


        if not paused:
            for planet in planet_list:
                planet.updated_position(planet_list)
        
        for planet in planet_list:
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
