"""Chess agent. Team 06.

Course material used:
    Session 2     PEAS / multi-agent adversarial environment
    Session 14    game trees, minimax
    Session 15    evaluation functions, alpha-beta, depth cutoff, move ordering
    Session 16    (optional) ideas we borrow lightly: iterative deepening as
                  anytime search under a clock
"""

import chess
import time

# ============================================================
# 0. SETTINGS
# ============================================================

STRATEGY = "improved"   # "baseline" = material-only 1-ply; kept for comparison
SAFETY_MARGIN_S = 0.5   # Colab reserve (handbook)
MAX_DEPTH = 6           # iterative deepening ceiling when time allows
MATE_SCORE = 100_000

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

# Piece-square tables, from White's view (rank 1 → index 0..7). Session 15:
# a linear evaluation = material + weighted positional features.
_PST_PAWN = (
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
   10, 10, 20, 30, 30, 20, 10, 10,
   50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0,
)
_PST_KNIGHT = (
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50,
)
_PST_BISHOP = (
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -20,-10,-10,-10,-10,-10,-10,-20,
)
_PST_ROOK = (
    0,  0,  0,  5,  5,  0,  0,  0,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0,
)
_PST_QUEEN = (
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5,
   -10,  5,  5,  5,  5,  5,  0,-10,
   -10,  0,  5,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20,
)
_PST_KING_MG = (
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
   -10,-20,-20,-20,-20,-20,-20,-10,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
)
_PST_KING_EG = (
     0, 10, 20, 30, 30, 20, 10,  0,
    10, 20, 30, 40, 40, 30, 20, 10,
    20, 30, 40, 50, 50, 40, 30, 20,
    30, 40, 50, 60, 60, 50, 40, 30,
    30, 40, 50, 60, 60, 50, 40, 30,
    20, 30, 40, 50, 50, 40, 30, 20,
    10, 20, 30, 40, 40, 30, 20, 10,
     0, 10, 20, 30, 30, 20, 10,  0,
)

_PST = {
    chess.PAWN: _PST_PAWN,
    chess.KNIGHT: _PST_KNIGHT,
    chess.BISHOP: _PST_BISHOP,
    chess.ROOK: _PST_ROOK,
    chess.QUEEN: _PST_QUEEN,
}

# Transposition table for the playing agent only (Session 15 optional extension).
# Cleared each game when act sees ply == 0 / new process — process is already
# fresh per game, so we clear on each act when the table grows too large.
_TT = {}
_TT_LIMIT = 200_000
_EXACT, _LOWER, _UPPER = 0, 1, 2


# ============================================================
# 1. EVALUATION (Session 15)
# ============================================================
#
# Features (White-positive):
#   material, piece-square tables, bishop pair, castling rights,
#   pawn structure (doubled / isolated / passed), king safety (pawn shield),
#   mobility (cheap: legal move count for side to move only, scaled small).
# ============================================================

def _pst_value(piece_type, square, color, endgame):
    if piece_type == chess.KING:
        table = _PST_KING_EG if endgame else _PST_KING_MG
    else:
        table = _PST[piece_type]
    idx = square if color == chess.WHITE else chess.square_mirror(square)
    return table[idx]


def _pawn_files(board, color):
    files = [0] * 8
    for sq in board.pieces(chess.PAWN, color):
        files[chess.square_file(sq)] += 1
    return files


def _is_passed(board, square, color):
    """No enemy pawn on this file or adjacent files ahead of this pawn."""
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    enemy = not color
    for f in (file - 1, file, file + 1):
        if not 0 <= f <= 7:
            continue
        for r in (range(rank + 1, 8) if color == chess.WHITE else range(rank - 1, -1, -1)):
            piece = board.piece_at(chess.square(f, r))
            if piece is not None and piece.piece_type == chess.PAWN and piece.color == enemy:
                return False
    return True


def _king_pawn_shield(board, color):
    """Bonus for friendly pawns on the three files in front of the king."""
    king = board.king(color)
    if king is None:
        return 0
    kf = chess.square_file(king)
    kr = chess.square_rank(king)
    ahead = 1 if color == chess.WHITE else -1
    score = 0
    for f in (kf - 1, kf, kf + 1):
        if not 0 <= f <= 7:
            continue
        for dist in (1, 2):
            r = kr + ahead * dist
            if not 0 <= r <= 7:
                continue
            piece = board.piece_at(chess.square(f, r))
            if piece is not None and piece.piece_type == chess.PAWN and piece.color == color:
                score += 12 if dist == 1 else 6
                break
    return score


def _evaluate_board(board, rich=True):
    """White-centric score. rich=False is the material-only baseline eval."""
    if board.is_checkmate():
        # Side to move is mated.
        return (-MATE_SCORE + board.ply()) if board.turn == chess.WHITE else (MATE_SCORE - board.ply())
    if board.is_game_over(claim_draw=False):
        return 0.0

    # Endgame once both sides have little non-pawn material.
    npm = 0
    for pt in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
        npm += len(board.pieces(pt, chess.WHITE)) * PIECE_VALUES[pt]
        npm += len(board.pieces(pt, chess.BLACK)) * PIECE_VALUES[pt]
    endgame = npm <= 1600

    score = 0
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]
        if rich:
            value += _pst_value(piece.piece_type, square, piece.color, endgame)
        score += value if piece.color == chess.WHITE else -value

    if not rich:
        return float(score)

    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 30
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 30

    if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
        score += 20
    if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
        score -= 20

    # Pawn structure
    for color, sign in ((chess.WHITE, 1), (chess.BLACK, -1)):
        files = _pawn_files(board, color)
        for f, count in enumerate(files):
            if count > 1:
                score += sign * (-15 * (count - 1))  # doubled
            if count >= 1:
                isolated = (f == 0 or files[f - 1] == 0) and (f == 7 or files[f + 1] == 0)
                if isolated:
                    score += sign * (-12)
        for sq in board.pieces(chess.PAWN, color):
            if _is_passed(board, sq, color):
                adv = chess.square_rank(sq) if color == chess.WHITE else 7 - chess.square_rank(sq)
                score += sign * (20 + 10 * adv)

    score += _king_pawn_shield(board, chess.WHITE) - _king_pawn_shield(board, chess.BLACK)

    # Small mobility term (side to move). Kept tiny so material ranking stays clear.
    mobility = board.legal_moves.count()
    score += mobility if board.turn == chess.WHITE else -mobility

    return float(score)


def evaluate(fen):
    """Heuristic score of a position, from White's point of view."""
    return _evaluate_board(chess.Board(fen), rich=True)


def evaluate_baseline(fen):
    """Material-only evaluation used by the baseline agent."""
    return _evaluate_board(chess.Board(fen), rich=False)


# ============================================================
# 2. MOVE ORDERING (Session 15: better order → more pruning)
# ============================================================

def _ordered_moves(board, tt_move=None, check_bonus=True):
    moves = list(board.legal_moves)

    def priority(move):
        if tt_move is not None and move == tt_move:
            return 50_000
        score = 0
        if board.is_capture(move):
            captured = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            # En passant: captured pawn is not on to_square.
            if captured is None and board.is_en_passant(move):
                captured_value = PIECE_VALUES[chess.PAWN]
            else:
                captured_value = PIECE_VALUES[captured.piece_type] if captured else 0
            attacker_value = PIECE_VALUES[attacker.piece_type] if attacker else 0
            score += 10_000 + 10 * captured_value - attacker_value
        if move.promotion:
            score += 8_000 + PIECE_VALUES[move.promotion]
        if check_bonus:
            board.push(move)
            if board.is_check():
                score += 5_000
            board.pop()
        return score

    moves.sort(key=priority, reverse=True)
    return moves


# ============================================================
# 3. REQUIRED SEARCH: MINIMAX AND ALPHA-BETA (Sessions 14–15)
# ============================================================

def minimax(fen, depth):
    board = chess.Board(fen)
    nodes = 0

    def search(position, remaining):
        nonlocal nodes
        nodes += 1
        if remaining == 0 or position.is_game_over(claim_draw=False):
            return _evaluate_board(position, rich=True)

        if position.turn == chess.WHITE:
            value = -float("inf")
            for move in position.legal_moves:
                position.push(move)
                value = max(value, search(position, remaining - 1))
                position.pop()
            return value

        value = float("inf")
        for move in position.legal_moves:
            position.push(move)
            value = min(value, search(position, remaining - 1))
            position.pop()
        return value

    return {"value": search(board, depth), "nodes": nodes}


def alphabeta(fen, depth):
    board = chess.Board(fen)
    nodes = 0

    def search(position, remaining, alpha, beta):
        nonlocal nodes
        nodes += 1
        if remaining == 0 or position.is_game_over(claim_draw=False):
            return _evaluate_board(position, rich=True)

        if position.turn == chess.WHITE:
            value = -float("inf")
            for move in _ordered_moves(position):
                position.push(move)
                value = max(value, search(position, remaining - 1, alpha, beta))
                position.pop()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        value = float("inf")
        for move in _ordered_moves(position):
            position.push(move)
            value = min(value, search(position, remaining - 1, alpha, beta))
            position.pop()
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    return {"value": search(board, depth, -float("inf"), float("inf")), "nodes": nodes}


# ============================================================
# 4. PLAYING SEARCH: ID + αβ + TT + quiescence
# ============================================================

def _tt_key(board):
    return board._transposition_key()


def _quiescence(board, alpha, beta, deadline, maximizing, qply=0):
    """Capture/promotion-only search at the leaves so we do not stop mid-exchange."""
    if time.perf_counter() >= deadline:
        return None

    stand = _evaluate_board(board, rich=True)
    if maximizing:
        if stand >= beta:
            return stand
        alpha = max(alpha, stand)
    else:
        if stand <= alpha:
            return stand
        beta = min(beta, stand)

    if qply >= 4:
        return stand

    moves = [m for m in _ordered_moves(board, check_bonus=False)
             if board.is_capture(m) or m.promotion]
    for move in moves:
        if time.perf_counter() >= deadline:
            return None
        board.push(move)
        value = _quiescence(board, alpha, beta, deadline, not maximizing, qply + 1)
        board.pop()
        if value is None:
            return None
        if maximizing:
            if value > stand:
                stand = value
            alpha = max(alpha, stand)
            if alpha >= beta:
                break
        else:
            if value < stand:
                stand = value
            beta = min(beta, stand)
            if alpha >= beta:
                break
    return stand


def _search_alpha_beta(board, remaining, alpha, beta, deadline, ply=0):
    if time.perf_counter() >= deadline:
        return None

    if board.is_game_over(claim_draw=False):
        return _evaluate_board(board, rich=True)

    if remaining == 0:
        return _quiescence(board, alpha, beta, deadline, board.turn == chess.WHITE)

    key = _tt_key(board)
    entry = _TT.get(key)
    tt_move = None
    if entry is not None and entry[1] >= remaining:
        score, _depth, flag, tt_move = entry
        if flag == _EXACT:
            return score
        if flag == _LOWER:
            alpha = max(alpha, score)
        elif flag == _UPPER:
            beta = min(beta, score)
        if alpha >= beta:
            return score

    maximizing = board.turn == chess.WHITE
    best_move = None
    original_alpha = alpha

    if maximizing:
        value = -float("inf")
        for move in _ordered_moves(board, tt_move):
            board.push(move)
            child = _search_alpha_beta(board, remaining - 1, alpha, beta, deadline, ply + 1)
            board.pop()
            if child is None:
                return None
            if child > value:
                value = child
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = float("inf")
        for move in _ordered_moves(board, tt_move):
            board.push(move)
            child = _search_alpha_beta(board, remaining - 1, alpha, beta, deadline, ply + 1)
            board.pop()
            if child is None:
                return None
            if child < value:
                value = child
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break

    if len(_TT) > _TT_LIMIT:
        _TT.clear()
    if value <= original_alpha:
        flag = _UPPER
    elif value >= beta:
        flag = _LOWER
    else:
        flag = _EXACT
    _TT[key] = (value, remaining, flag, best_move)
    return value


def _search_root(board, depth, deadline):
    maximizing = board.turn == chess.WHITE
    best_move = None
    best_value = -float("inf") if maximizing else float("inf")
    alpha = -float("inf")
    beta = float("inf")

    key = _tt_key(board)
    tt_move = _TT[key][3] if key in _TT else None

    for move in _ordered_moves(board, tt_move):
        if time.perf_counter() >= deadline:
            return best_move, best_value, True
        board.push(move)
        value = _search_alpha_beta(board, depth - 1, alpha, beta, deadline)
        board.pop()
        if value is None:
            return best_move, best_value, True

        if (maximizing and value > best_value) or (not maximizing and value < best_value):
            best_value = value
            best_move = move
        if maximizing:
            alpha = max(alpha, best_value)
        else:
            beta = min(beta, best_value)

    if best_move is not None:
        _TT[key] = (best_value, depth, _EXACT, best_move)
    return best_move, best_value, False


# ============================================================
# 5. AGENT
# ============================================================

def _budget_s(remaining):
    """How long this move may think. Never exceeds the clock the judge still has."""
    # Always leave a few tens of ms to serialise the answer.
    overhead = 0.03
    if remaining <= overhead + 0.02:
        return 0.0
    reserve = min(SAFETY_MARGIN_S, max(0.05, remaining * 0.25))
    usable = max(0.0, remaining - reserve - overhead)
    if usable <= 0.0:
        return 0.0
    # Spend a slice of the remaining clock; cap so early moves do not burn it.
    return min(0.85, max(0.08, usable * 0.16), usable)


def _act_baseline(observation):
    """FIRST STRATEGY: material-only one-ply lookahead (Session 14, depth 1)."""
    board = chess.Board(observation["fen"])
    me_is_white = board.turn == chess.WHITE
    best_moves, best_score = [], None
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            score = MATE_SCORE
        else:
            score = _evaluate_board(board, rich=False)
            if not me_is_white:
                score = -score
        board.pop()
        if best_score is None or score > best_score:
            best_moves, best_score = [move], score
        elif score == best_score:
            best_moves.append(move)
    return {"move": best_moves[0].uci()}


def _act_improved(observation):
    """IMPROVED: iterative deepening αβ + TT + quiescence + rich eval."""
    board = chess.Board(observation["fen"])
    legal = list(board.legal_moves)
    if not legal:
        return {"move": "resign"}
    if len(legal) == 1:
        return {"move": legal[0].uci()}

    remaining = float(observation.get("time_remaining_s") or 5.0)
    budget = _budget_s(remaining)
    best_move = _ordered_moves(board, check_bonus=False)[0]

    # Flag fall: return a legal capture/check-biased move with no search.
    if budget <= 0.0:
        return {"move": best_move.uci()}

    deadline = time.perf_counter() + budget

    for depth in range(1, MAX_DEPTH + 1):
        move, _value, timed_out = _search_root(board, depth, deadline)
        if timed_out:
            break
        if move is not None:
            best_move = move
        if time.perf_counter() >= deadline - 0.015:
            break

    return {"move": best_move.uci()}


def act(observation):
    """Called once per move. Module-level variables survive within a game.

    observation["fen"]                        the position
    observation["color"]                      "white" or "black"
    observation["legal_moves"]                legal moves in UCI
    observation["history"]                    every move so far in UCI
    observation["ply"], ["is_check"]
    observation["game_number"], ["games_total"]
    observation["time_remaining_s"]
    observation["opponent_time_remaining_s"]

    Return {"move": "e2e4"}, or {"move": "resign"}.
    """
    if observation.get("ply", 0) == 0:
        _TT.clear()

    if STRATEGY == "baseline":
        return _act_baseline(observation)
    return _act_improved(observation)
