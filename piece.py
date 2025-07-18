import pygame

class Piece(pygame.sprite.Sprite):
    # Class-level constant (moved outside __init__)
    PIECES_MAP = {
        "white_pawn": 5,
        "white_knight": 3,
        "white_bishop": 2,
        "white_rook": 4,
        "white_king": 0,
        "white_queen": 1,
        "black_pawn": 11,
        "black_knight": 9,
        "black_bishop": 8,
        "black_rook": 10,
        "black_king": 6,
        "black_queen": 7
    }

    def __init__(self, filename, cols, rows, scale=1.0):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.scale = scale
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        original_cell_width = self.rect.width // cols
        original_cell_height = self.rect.height // rows
        
        # Calculate cell dimensions after scaling
        self.cell_width = int(original_cell_width * scale)
        self.cell_height = int(original_cell_height * scale)
        
        # Create cell rectangles
        self.cells = [
            (
                (i % cols) * original_cell_width,
                (i // cols) * original_cell_height,
                original_cell_width,
                original_cell_height
            )
            for i in range(self.cell_count)
        ]

    def draw(self, surface, piece_name, coords):
        piece_index = self.PIECES_MAP[piece_name]
        surface.blit(self.spritesheet, coords, self.cells[piece_index])