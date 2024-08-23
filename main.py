import pygame
import math 
import heapq
from queue import PriorityQueue
import random

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE  = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self,row,col,width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row,self.col

    def is_open(self):
        return self.colour == GREEN

    def is_closed(self):
        return self.colour == RED
    
    def is_barrier(self):
        return self.colour == BLACK
    
    def is_start(self):
        return self.colour == ORANGE
    
    def is_end(self):
        return self.colour == TURQUOISE
    
    def make_reset(self):
        self.colour = WHITE
    
    def make_open(self):
        self.colour = GREEN

    def make_closed(self):
        self.colour = RED

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def neigh(self, grid):
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbours.append(grid[self.row+1][self.col])
        if self.col< self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbours.append(grid[self.row][self.col+1])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbours.append(grid[self.row-1][self.col])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbours.append(grid[self.row][self.col-1])
        
        # if self.row < self.total_rows-1 and self.col < self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier():
        #     self.neighbours.append(grid[self.row+1][self.col+1])
        # if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_barrier():
        #     self.neighbours.append(grid[self.row-1][self.col-1])
        # if self.row < self.total_rows-1 and self.col >0 and not grid[self.row+1][self.col-1].is_barrier():
        #     self.neighbours.append(grid[self.row+1][self.col-1])
        # if self.row > 0 and self.col < self.total_rows-1 and not grid[self.row-1][self.col+1].is_barrier():
        #     self.neighbours.append(grid[self.row-1][self.col+1])


    def __lt__(self,other):
        return False

def grid_maker(rows, width):
    gap = width // rows
    grid = []

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)
    return grid

def line_maker(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap,0), (j*gap,width))

def draw(win, grid,rows, width):
    win.fill(WHITE)

    for row in grid:
        for spots in row:
            spots.draw(win)
    
    line_maker(win,rows,width)
    pygame.display.update()

def clicked_pos(pos, width, rows):
    gap = width // rows
    x,y = pos

    return [x // gap, y // gap]

def displacementCalc(dst, n, m):
    end_x, end_y = dst.get_pos()
    hashMap = {}
    for r in range(n):
        for c in range(m):
            hashMap[(r,c)] = abs(r-end_x) + abs(c-end_y)
    return hashMap


def algorithm(draw, grid, st, ed, n,m):
    displacement = displacementCalc(ed, n,m)
    heap = PriorityQueue()
    start_x, start_y = st.get_pos()
    
    heap.put((displacement[(start_x, start_y)], 0, (0,st,None))) #(displacment, (current vertex, toal weight, parent))
    parent = {}
    flag = 0
    count = 0
    while not heap.empty():
        dis, ct, other = heap.get()
        pathWeight, nd, part = other
        nd.make_closed()
        if nd == ed:
            parent[nd] = part
            flag = 1
            break
        else:
            parent[nd] = part
            nd.neigh(grid)
            for ngh in nd.neighbours:
                if not ngh.is_closed() and not ngh.is_open():
                    count+=1
                    ngh.make_open()
                    neigh_x, neigh_y = ngh.get_pos()
                    heap.put((pathWeight + 1+ displacement[(neigh_x,neigh_y)], count, (pathWeight + 1,ngh, nd)))
        draw()
    if flag:
        path = []
        curr = ed
        while curr:
            curr_x, curr_y = curr.get_pos()
            curr.make_path()
            path.append((curr_x,curr_y))
            curr = parent[curr]
        return path
    
def main(win, width):
    rows = 50
    grid = grid_maker(rows, width)

    start = None
    end = None

    started = False
    run = True
    
    while run:
        draw(win,grid,rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = clicked_pos(pos,width,rows)
                spot = grid[row][col]
                if not start:
                    start = spot
                    start.make_start()
                elif not end:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = clicked_pos(pos,width,rows)
                spot = grid[row][col]
                spot.make_reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and not started:
                    started = True
                    path = algorithm(lambda:draw(win,grid,rows,width), grid, start,end, rows,rows)


    
    pygame.quit()

main(WIN, WIDTH)