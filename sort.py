import pygame
import random
import time
import sys

pygame.init()


class DrawAttributes:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    PINK = 255, 182, 193
    BACKGROUND_COLOR = BLACK #WHITE

    """GRADIENT = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]"""

    GRADIENT = [
        (255, 192, 203),
        (255, 105, 180),
        (255, 20, 147)
    ]
    SMALL_FONT = pygame.font.SysFont('Helvetica', 15)
    FONT = pygame.font.SysFont('Helvetica', 25)
    LARGE_FONT = pygame.font.SysFont('Helvetica', 40)
    SIDE_PAD = 100  # padding for both left and right sides, combined
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithms Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = (self.width - self.SIDE_PAD) // len(lst)
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

    def draw(self, algo_name, ascending, s_times):
        self.window.fill(self.BACKGROUND_COLOR)

        title = self.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
                                       True, self.PINK)
        self.window.blit(title, (self.width / 2 - title.get_width() / 2, 5))

        controls = self.FONT.render("N - New | R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",
                                    True,
                                    self.PINK)
        self.window.blit(controls, (self.width / 2 - controls.get_width() / 2, 50))

        algorithms = self.FONT.render("I - Insertion Sort | H - Heap Sort | B - Bubble Sort", True, self.PINK)
        self.window.blit(algorithms, (self.width / 2 - algorithms.get_width() / 2, 80))

        self.draw_list()
        self.draw_times(s_times)
        pygame.display.update()

    def draw_list(self, color_position=None, clear_bg=False):
        if color_position is None:
            color_position = {}
        lst = self.lst

        if clear_bg:
            clear_rect = (self.SIDE_PAD // 2, self.TOP_PAD, self.width - self.SIDE_PAD,
                          self.height - self.TOP_PAD)
            pygame.draw.rect(self.window, self.BACKGROUND_COLOR, clear_rect)

        for i, val in enumerate(lst):
            x = self.start_x + i * self.block_width
            y = self.height - (val - self.min_val) * self.block_height

            color = self.GRADIENT[i % 3]

            if i in color_position:
                color = color_position[i]

            pygame.draw.rect(self.window, color, (x, y, self.block_width, self.height))

        if clear_bg:
            pygame.display.update()

    def draw_times(self, s_times=None):

        time_blit = self.SMALL_FONT.render(f"{s_times.insertion}{'s' if s_times.insertion else ''} | "
                                           f"{s_times.heap}{'s' if s_times.heap else ''} | "
                                           f"{s_times.bubble}{'s' if s_times.bubble else ''}"
                                           , True, self.PINK)
        self.window.blit(time_blit, (self.width / 2 - time_blit.get_width() / 2, 110))


class SortingTimes:
    bubble = None
    heap = None
    insertion = None

    def clear(self):
        self.bubble = None
        self.heap = None
        self.insertion = None


def generate_starting_list(n, min_val, max_val, same_sid=False, seed=None):
    if not same_sid:
        seed = random.randrange(sys.maxsize)

    random.seed(seed)
    lst = random.sample(range(min_val, max_val), n)

    return lst, seed


def insertion_sort(draw_attr, s_times, ascending=True):
    start = time.perf_counter()
    lst = draw_attr.lst

    for i in range(1, len(lst)):
        curr = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > curr and ascending
            descending_sort = i > 0 and lst[i - 1] < curr and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = curr
            draw_attr.draw_list({i: draw_attr.GREEN, i - 1: draw_attr.RED}, True)
            yield True

    s_times.insertion = round(time.perf_counter() - start, 2)
    draw_attr.draw_times(s_times)


def heapify(draw_attr, n, i, ascending):
    lst = draw_attr.lst

    curr = i
    left = 2 * i + 1
    right = 2 * i + 2

    if ascending:
        if left < n and lst[curr] < lst[left]:
            curr = left

        if right < n and lst[curr] < lst[right]:
            curr = right

    if not ascending:
        if left < n and lst[left] < lst[curr]:
            curr = left

        if right < n and lst[right] < lst[curr]:
            curr = right

    if curr != i:
        (lst[i], lst[curr]) = (lst[curr], lst[i])
        draw_attr.draw_list({i: draw_attr.GREEN, curr: draw_attr.RED}, True)
        heapify(draw_attr, n, curr, ascending)


def heap_sort(draw_attr, s_times, ascending=True):
    start = time.perf_counter()
    lst = draw_attr.lst

    n = len(lst)
    for i in range(n // 2 - 1, -1, -1):
        heapify(draw_attr, n, i, ascending)

    for i in range(n - 1, 0, -1):
        (lst[i], lst[0]) = (lst[0], lst[i])
        draw_attr.draw_list({i: draw_attr.GREEN, 0: draw_attr.RED}, True)
        heapify(draw_attr, i, 0, ascending)
        yield True

    s_times.heap = round(time.perf_counter() - start, 2)
    draw_attr.draw_times(s_times)


def bubble_sort(draw_attr, s_times, ascending=True):
    start = time.perf_counter()
    lst = draw_attr.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_attr.draw_list({j: draw_attr.GREEN, j + 1: draw_attr.RED}, True)
                yield True

    s_times.bubble = round(time.perf_counter() - start, 2)
    draw_attr.draw_times(s_times)


def main():
    run = True
    n = 100
    min_val = 0
    max_val = 100

    lst, seed = generate_starting_list(n, min_val, max_val)
    draw_attr = DrawAttributes(800, 600, lst)

    sorting = False
    ascending = True

    sorting_algorithm = insertion_sort
    sorting_algorithm_name = "Insertion Sort"
    sorting_algorithm_generator = None

    s_times = SortingTimes()

    while run:
        pygame.time.Clock().tick(30)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw_attr.draw(sorting_algorithm_name, ascending, s_times)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_n:  # new list
                lst, seed = generate_starting_list(n, min_val, max_val)
                draw_attr.set_list(lst)
                s_times.clear()
                sorting = False

            elif event.key == pygame.K_r:  # reset list
                lst, seed = generate_starting_list(n, min_val, max_val, True, seed)
                draw_attr.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_attr, s_times, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"

            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algorithm_name = "Heap Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
    pygame.quit()


if __name__ == "__main__":
    main()
