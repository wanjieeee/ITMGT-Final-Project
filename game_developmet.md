# Our Process
When we first built our chess game based on an online tutorial, we quickly realized there was a big difference between code that works and code that creates a playable experience. Today, we’ll show how we transformed a buggy prototype into a fully functional game through python.

The original version had three fundamental problems:
1. Buggy movement: pieces sometimes could eat their own teammates or move in invalid ways
2. Game didn’t end properly. Even if the king was in check (or was already eaten), the game allowed other pieces to still keep moving.
3. Poor user experience

## How we tackled these issues
### A. Movement 

We discovered such pieces could do illegal moves, completely breaking chess rules. Here’s how we fixed it:
	
1. Created dedicated valid_move() methods for each piece class to be able to internally limit a piece’s movement
2. Implemented path checking with straightline_moves() helper
3. We had each piece check whether a square has it’s teammate or the other color’s piece

While making the game, one of the first issues we noticed was the pieces being able to capture ally pieces. This meant that if the player really wanted to, they could make a queen for example, capture all her pawns. The issue here was that the function for the piece movement mistakenly had (.has_team_piece) tagged instead of (.has_enemy_piece) when considering valid moves. This meant that not only was the piece mistakenly targeting teammates, it was also effectively ignoring enemy pieces. This was a relatively simple fix after finding it, all we had to do was change the tags and it worked as intended.

Another issue discovered later on was the game not properly ending upon a checkmate. When capturing a piece that would trigger a checkmate, the game would continue as normal, allowing the king piece to make illegal moves that would normally not be allowed due to chess’ rules. The fix here was a bit trickier and took a decent amount of rereading the code to figure out. What was happening was the checkmate flag was triggering before the code line to switch turns. This meant that the checkmate WOULD trigger, but wouldn’t show up because the turn order would switch. This issue was resolved by moving the entire code block below the line while making sure to keep it in proper indentation. While fixed initially, this issue re-appeared in another form later on. After the game had been rewritten, the checkmate would once again not trigger upon a successful checkmate. The solution here was to add a function in the piece class that would not only check if the king is being threatened, but send a checkmate flag when it can't make any more moves. 

One last issue was with only the two pawns in the middle being able to move. No other piece was able to do anything except for the two pawns. This bug… was really weird. The solution was even weirder. It turns out that the code to move by row and column was mixed. This somehow resulted in only two pieces being able to move. We still don’t know why that is, or how it happened, but changing the label on the code seemed to fix the entire problem. Personally, our theory is that since the row and column were mixed up, only the central pieces worked because they were mediums in coordinate and didn’t break.

### B. Time Visualization
When we first added the chess clock, we initially created two functions: update_timers() and draw_timers(). Firstly, update_timers() was in charge of making the clock work, like doing an actual countdown. It used Python’s time module, checking the difference between the current moment and the last recorded update, then subtracting that from the active player’s time. The draw_timers(), on the other hand, handled the visuals, turning the remaining seconds into a readable “minutes:seconds” format and displaying them on the screen with Pygame’s text rendering. After the time was running in the program, we placed Black’s clock at the top right and White’s at the bottom right to place their position like actual chess clocks.

At first, the countdown worked, but it drained time far too quickly. We discovered that update_timers() was being called more often than it should because we didn’t factor in how often the game loop refreshed. Each loop was essentially chopping off more time than intended, like the clock runs faster than a second. We fixed this by calculating delta_time, the exact number of seconds since the last loop, and subtracting only that. Once we added this correction, the clocks ticked naturally, dropping second by second just like they would in a real chess match.

Finally, we made sure that the clock actually played its role in the game. We added logic inside update_timers() so that if a player’s time hit zero, self.winner was set to the opponent. At first, the game would reset immediately, skipping the win screen, but after reworking the flow, we somehow got it to pause and display “White Wins” or “Black Wins” until the players chose to start again. Looking back, writing update_timers() and draw_timers() seemed simple, but getting them to work smoothly without breaking the rest of the game took plenty of trial and error.

### C. Reorganization

In the original version, logic were spread across multiple files with unclear separation of concerns. For instance, dragging behavior, board rendering, configuration settings, and gameplay logic were divided across modules like dragger.py, config.py, and color.py, which often have overlapping responsibilities too. To add, variables like const.TILESIZE was also hardcoded in const.py (which we were able to incorporate into game.py along with other interface codes). Even the color themes were isolated in color.py, but not fully integrated. All of this made it very scattered and confusing to navigate.

In our version, we structured the code into more purposeful and concise modules, which helped make each file easier to understand and maintain:

game.py: handles the flow, running the main game loop, checking for quitting or restarting, and drawing the game board
chess.py: is where the main game codes are. This includes all piece movements, turn logic, win conditions, and possible moves.
piece.py : loads and renders chess piece icons
utils.py: handles the general-purpose functions like mouse input
sound.py: plays audio cues for moves and captures

For the main game’s lines of codes, which we centralized in Chess class in chess.py. This class is responsible for tracking all essential elements of the game flow:
self.piece_location - a nested dictionary that stores the identity, selection status, and screen coordinates of each piece
self.turn  - a dictionary indicating which player’s turn it is
self.moves - a list of valid moves for a selected piece
self.winner - a string that stores the name of the winning player once the king is captured 
self.captured - a list that keeps track of all captured pieces

By consolidating these elements within a single class, we created a consistent and manageable way to update, reset, and reference the current state of the game.

We also replaced many ambiguous variable and function names with clearer, more descriptive alternatives. For example:
draggable.square was replaced with piece_location to more accurately reflect its purpose
Selection flags and position tracking were unified within each piece’s dictionary entry in piece_location
Functions such as possible_moves() determine valid moves for each piece type, while move_piece() and validate_move() enforce movement rules and capture logic

The game.py file now serves as the main control point for the game. It manages displaying the game menu and end screen, running the core game loop ( start_game() ), resetting the board through self.chess.reset(), and calling visual updates such as draw_pieces() and play_turn().

By keeping the game loop free of core logic (which is in chess.py), the application remains clean and modular. This approach also made it easier to introduce new features such as the timer, turn display text at the top of the screen, and the exit button.

In the end, we gained a lot from this project as it allowed us to apply the concepts and ideas we learned in class into actual practice. Throughout the process, we were challenged to apply our knowledge, think critically, and actually come up with solutions to problems we have encountered along the way. Through cooperation, we deepened our understanding of the topics in python programming, turned such theories into working code, and saw how what we studied could be used to create something functional. This experience solidified our learning, improved our problem-solving skills, and gave us a stronger grasp of how to approach real-world tasks using what we know.


## References
Tutorial we used: https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&si=9RfoV5YvS8OQJiEo
