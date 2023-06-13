import tkinter as tk
from PIL import Image, ImageTk

# Define the chessboard size
BOARD_SIZE = 8

# Initialize the tkinter window
window = tk.Tk()
window.title("Chess App")

# Create a canvas to display the chessboard
canvas = tk.Canvas(window, width=600, height=600)
canvas.pack()

# Load chess piece images
piece_images = {
    "wK": ImageTk.PhotoImage(Image.open("images/white_king.png")),
    "wQ": ImageTk.PhotoImage(Image.open("images/white_queen.png")),
    "wR": ImageTk.PhotoImage(Image.open("images/white_rook.png")),
    "wB": ImageTk.PhotoImage(Image.open("images/white_bishop.png")),
    "wN": ImageTk.PhotoImage(Image.open("images/white_knight.png")),
    "wp": ImageTk.PhotoImage(Image.open("images/white_pawn.png")),
    "bK": ImageTk.PhotoImage(Image.open("images/black_king.png")),
    "bQ": ImageTk.PhotoImage(Image.open("images/black_queen.png")),
    "bR": ImageTk.PhotoImage(Image.open("images/black_rook.png")),
    "bB": ImageTk.PhotoImage(Image.open("images/black_bishop.png")),
    "bN": ImageTk.PhotoImage(Image.open("images/black_knight.png")),
    "bp": ImageTk.PhotoImage(Image.open("images/black_pawn.png")),
}

# Create a chessboard
chessboard = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Initialize the chessboard with pieces
for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
        if row == 0:
            if col == 0 or col == 7:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["bR"]
                )
            elif col == 1 or col == 6:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["bN"]
                )
            elif col == 2 or col == 5:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["bB"]
                )
            elif col == 3:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["bQ"]
                )
            elif col == 4:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["bK"]
                )
        elif row == 1:
            chessboard[row][col] = canvas.create_image(
                col * 75 + 37.5, row * 75 + 37.5, image=piece_images["bp"]
            )
        elif row == 6:
            chessboard[row][col] = canvas.create_image(
                col * 75 + 37.5, row * 75 + 37.5, image=piece_images["wp"]
            )
        elif row == 7:
            if col == 0 or col == 7:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["wR"]
                )
            elif col == 1 or col == 6:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["wN"]
                )
            elif col == 2 or col == 5:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["wB"]
                )
            elif col == 3:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["wQ"]
                )
            elif col == 4:
                chessboard[row][col] = canvas.create_image(
                    col * 75 + 37.5, row * 75 + 37.5, image=piece_images["wK"]
                )

# Function to handle piece movement
def move_piece(event):
    x = event.x
    y = event.y

    # Find the row and column of the clicked position
    col = x // 75
    row = y // 75

    # Get the piece at the clicked position
    piece = chessboard[row][col]

    # If a piece is clicked, initiate dragging
    if piece is not None:
        canvas.bind("<B1-Motion>", drag_piece)
        canvas.bind("<ButtonRelease-1>", release_piece)
        canvas.lift(piece)

        # Store the initial position of the piece
        piece_start_x = x
        piece_start_y = y
        piece_start_col = col
        piece_start_row = row

# Function to handle dragging of the piece
def drag_piece(event):
    # Move the piece with the mouse cursor
    x = event.x
    y = event.y
    canvas.coords(
        chessboard[piece_start_row][piece_start_col],
        x,
        y,
    )

# Function to handle release of the piece
def release_piece(event):
    x = event.x
    y = event.y

    # Find the row and column where the piece is released
    col = x // 75
    row = y // 75

    # If the release position is valid, move the piece
    if (
        row >= 0
        and row < BOARD_SIZE
        and col >= 0
        and col < BOARD_SIZE
        and (row, col) != (piece_start_row, piece_start_col)
        and chessboard[row][col] is None
    ):
        chessboard[row][col] = chessboard[piece_start_row][piece_start_col]
        chessboard[piece_start_row][piece_start_col] = None
        canvas.coords(
            chessboard[row][col],
            col * 75 + 37.5,
            row * 75 + 37.5,
        )

    # Reset the piece position
    else:
        canvas.coords(
            chessboard[piece_start_row][piece_start_col],
            piece_start_col * 75 + 37.5,
            piece_start_row * 75 + 37.5,
        )

    # Unbind the drag and release events
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

# Bind the mouse click event to the move_piece function
canvas.bind("<Button-1>", move_piece)

# Start the tkinter event loop
window.mainloop()