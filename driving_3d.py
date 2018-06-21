import pygame, sys, math

pygame.init()

w,h = 400, 400; cx,cy = w//2, h//2
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()


class PerspectiveCamera:
    def __init__(self, position=(0,0,0), rotation=(0, 0)):
        self.position = list(position)
        self.rotation = list(rotation)


class Cube:
    def __init__(self, n=1):
        self.n = n
        self.vertices = self.__generate_vertices()
        self.connections = self.__generate_edge_connections()

    def update(self, dt, key):
        s = dt * 10
        if key[pygame.K_LEFT]:
            lst = []
            for item in self.vertices:
                lst.append((item[0] - s, item[1], item[2]))
            self.vertices = lst
        if key[pygame.K_RIGHT]:
            lst = []
            for item in self.vertices:
                lst.append((item[0] + s, item[1], item[2]))
            self.vertices = lst

    def __generate_vertices(self):
        vertices = []
        for i in [0, 4, 6, 2, 1, 5, 7, 3]:
            s = "%03d" % int(str(bin(i))[2:])
            new_tuple = ()
            for char in s:
                multiplier = 1 * self.n if char is '1' else -1 * self.n
                new_tuple += (multiplier,)
            vertices += (new_tuple,)
        return vertices

    @staticmethod
    def __generate_edge_connections():
        out = []
        for i in range(4):
            out.append((i % 4, (i + 1) % 4))
        for i in range(4):
            out.append((i % 4 + 4, (i + 1) % 4 + 4))
        for i in range(0, 4):
            out.append((out[i][0], out[i + 4][0]))
        for item in out:
            print(item)
        return out


n = Cube()
cam = PerspectiveCamera((9, -5, -5))

print(n.vertices)
print(n.connections)
while True:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    screen.fill((255, 255, 255))

    for x,y,z in n.vertices:
        z += 5
        f = 200 / z

        x,y = x*f,y*f

    for connection in n.connections:
        point_a = n.vertices[connection[0]]
        point_b = n.vertices[connection[1]]

        points = []
        for x,y,z in (point_a, point_b):
            x -= cam.position[0]
            y -= cam.position[1]
            z -= cam.position[2]

            z += 13
            f = 200 / z
            x = x * f
            y = y * f
            points += [(cx + int(x), cy + int(y))]
        pygame.draw.line(screen, (127,0,127), points[0], points[1], 1)

    pygame.display.flip()
    key = pygame.key.get_pressed()
    n.update(dt, key)
