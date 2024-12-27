#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid_size = 4
        self.score = 0

        self.main_grid = tk.Frame(self.master, bg="gray", bd=3, width=400, height=400)
        self.main_grid.grid(pady=(100, 0))
        self.cells = []

        self.create_grid()
        self.start_game()

        self.master.bind("<Key>", self.handle_keypress)

    def create_grid(self):
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg="lightgray",
                    width=100,
                    height=100
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(cell_frame, bg="lightgray", font=("Helvetica", 24), width=4, height=2)
                cell_number.grid()
                row.append(cell_number)
            self.cells.append(row)

    def start_game(self):
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                number = self.matrix[i][j]
                if number == 0:
                    self.cells[i][j].config(text="", bg="lightgray")
                else:
                    self.cells[i][j].config(text=str(number), bg=self.get_color(number))

    def get_color(self, number):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(number, "#cdc1b4")

    def handle_keypress(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            if self.move_tiles(key):
                self.add_new_tile()
                self.update_grid()
                if self.check_game_over():
                    self.show_game_over()

    def move_tiles(self, direction):
        moved = False
        if direction == "Up":
            for j in range(self.grid_size):
                column = [self.matrix[i][j] for i in range(self.grid_size)]
                new_column, has_changed = self.compress_and_merge(column)
                for i in range(self.grid_size):
                    if self.matrix[i][j] != new_column[i]:
                        moved = True
                    self.matrix[i][j] = new_column[i]

        elif direction == "Down":
            for j in range(self.grid_size):
                column = [self.matrix[i][j] for i in range(self.grid_size)][::-1]
                new_column, has_changed = self.compress_and_merge(column)
                new_column.reverse()
                for i in range(self.grid_size):
                    if self.matrix[i][j] != new_column[i]:
                        moved = True
                    self.matrix[i][j] = new_column[i]

        elif direction == "Left":
            for i in range(self.grid_size):
                row = self.matrix[i]
                new_row, has_changed = self.compress_and_merge(row)
                if self.matrix[i] != new_row:
                    moved = True
                self.matrix[i] = new_row

        elif direction == "Right":
            for i in range(self.grid_size):
                row = self.matrix[i][::-1]
                new_row, has_changed = self.compress_and_merge(row)
                new_row.reverse()
                if self.matrix[i] != new_row:
                    moved = True
                self.matrix[i] = new_row

        return moved

    def compress_and_merge(self, line):
        # Step 1: Remove all zeros
        line = [num for num in line if num != 0]

        # Step 2: Merge adjacent equal numbers
        merged = []
        skip = False
        for i in range(len(line)):
            if skip:
                skip = False
                continue
            if i + 1 < len(line) and line[i] == line[i + 1]:
                merged.append(line[i] * 2)
                self.score += line[i] * 2  # Update the score
                skip = True
            else:
                merged.append(line[i])

        # Step 3: Add zeros back to fill the line
        while len(merged) < self.grid_size:
            merged.append(0)

        return merged, merged != line  # Return the new line and whether any change occurred

    def check_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.matrix[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
        return True

    def show_game_over(self):
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            game_over_frame,
            text="Game Over",
            bg="black",
            fg="white",
            font=("Helvetica", 24)
        ).pack()

if __name__ == "__main__":
    root = tk.Tk()
    Game2048(root)
    root.mainloop()


# In[ ]:




