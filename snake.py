import pygame
import sys
import random
pygame.init()
clock = pygame.time.Clock()

# variables
gameOver = False
score = 0

toolBarSize = 60
nodeSize = 30
cols = 10
rows = 14
winHeight = (nodeSize * rows) + toolBarSize
winWidth = nodeSize * cols


# Colors
bgColor = (235, 235, 235)
foodColor = (203, 15, 255)
snakeHeadColor = (22, 247, 97)
snakeBodyColor = (52, 217, 107)


screen = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption('Snake Game')


class Snake:
    def __init__(self):
        self.nodes = [[0, 0]]
        self.direction = 'RIGHT'

    def addNode(self, newNode):
        self.nodes.append(newNode)

    def move(self):
        newNode = [0, 0]
        newNode[1] = self.nodes[-1][1]
        newNode[0] = self.nodes[-1][0]

        if self.direction == "RIGHT":
            newNode[0] += 1
        if self.direction == "LEFT":
            newNode[0] -= 1
        if self.direction == "DOWN":
            newNode[1] += 1
        if self.direction == "UP":
            newNode[1] -= 1

        self.nodes.append(newNode)
        self.nodes.remove(self.nodes[0])

    def show(self):
        head = self.nodes[-1]
        for node in self.nodes:
            if node == head:
                nodeObj(node[0], node[1], snakeHeadColor)
            else:
                nodeObj(node[0], node[1], snakeBodyColor)

    def changeDirection(self):
        if self.direction == "RIGHT":
            self.direction = "DOWN"

        elif self.direction == "DOWN":
            self.direction = "LEFT"

        elif self.direction == "LEFT":
            self.direction = "UP"

        elif self.direction == "UP":
            self.direction = "RIGHT"


class Food:
    def __init__(self):
        self.newFood()

    def show(self):
        nodeObj(self.position[0], self.position[1], foodColor)

    def newFood(self):
        x = int(random.random() * cols - 1)
        y = int(random.random() * rows - 1)
        position = [x, y]
        for node in snake.nodes:
            if position == node:
                self.newFood()
        self.position = position


snake = Snake()
food = Food()


def check():
    global gameOver, score
    nodes = snake.nodes
    # check for eating food
    if snake.nodes[-1] == food.position:
        snake.addNode(food.position)
        food.newFood()
        score += 1

    # check for geting outside from the window
    if nodes[-1][0] > cols-1 or nodes[-1][0] < 0 or nodes[-1][1] > rows-1 or nodes[-1][1] < 0:
        # game over
        gameOver = True

    # Check if the snake eat's it's won tell
    for node in nodes[:-3]:
        if nodes[-1] == node:
            gameOver = True


def nodeObj(x, y, color):
    pygame.draw.rect(
        screen, color, [x * nodeSize, y * nodeSize, nodeSize, nodeSize]
    )
    pygame.draw.rect(
        screen, (255, 255, 255),
        [x * nodeSize, y * nodeSize, nodeSize, nodeSize], 4
    )


def setGrid():
    i = 0
    while i < rows:
        j = 0
        while j < cols:
            nodeObj(j, i, (255, 255, 255))
            j += 1
        i += 1


def showScore():
    pygame.draw.rect(screen, bgColor, [
                     0, winHeight-toolBarSize, winWidth, toolBarSize])
    font = pygame.font.SysFont('sans-serif', 30)
    scoreText = font.render(f"Score: {score}", True, (50, 50, 50))
    screen.blit(scoreText, ((winWidth/2) - int(scoreText.get_width()/2),
                            (winHeight - toolBarSize/2 - scoreText.get_height()/2)))


def showGameOver():
    font = pygame.font.SysFont('sans-serif', 60)
    gameOverText = font.render(f"Game Over", True, (255, 20, 20))
    screen.blit(gameOverText, ((winWidth/2) - int(gameOverText.get_width()/2),
                               ((winHeight-toolBarSize)/2) - (gameOverText.get_height()/2)))

    font = pygame.font.SysFont('sans-serif', 40)
    scoreText = font.render(f"Score: {score}", True, (255, 208, 15))
    screen.blit(scoreText, ((winWidth/2) - int(scoreText.get_width()/2),
                            ((winHeight-toolBarSize)/2) + (scoreText.get_height())))


while True:
    # Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                snake.changeDirection()
        pygame.display.update()

    screen.fill(bgColor)
    setGrid()

    snake.show()
    food.show()
    showScore()
    check()

    if gameOver != True:
        snake.move()
    else:
        showGameOver()

    pygame.display.flip()
    clock.tick(8)
