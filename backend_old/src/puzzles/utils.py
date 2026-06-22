from typing import List


def generate_clues(solution_grid: List[List[int]]):
    row_clues = []
    col_clues = []

    for row in solution_grid:
        count = 0
        clues = []
        for cell in row:
            if cell == 1:
                count += 1
            else:
                if count > 0:
                    clues.append(count)
                    count = 0
        if count > 0:
            clues.append(count)
        row_clues.append(clues)

    for col in range(len(solution_grid[0])):
        count = 0
        clues = []
        for row in range(len(solution_grid)):
            if solution_grid[row][col] == 1:
                count += 1
            else:
                if count > 0:
                    clues.append(count)
                    count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues)

    return row_clues, col_clues

def calculate_difficulty(solution_grid):
    total = len(solution_grid) * len(solution_grid[0])
    filled = sum(cell for row in solution_grid for cell in row)
    density = filled / total

    if density < 0.3:
        return "hard"
    elif density < 0.45:
        return "medium"
    else:
        return "easy"