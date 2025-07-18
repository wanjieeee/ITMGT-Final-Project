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
