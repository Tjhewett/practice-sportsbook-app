# database models for the tables in MySQL

from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    currency = db.Column(db.Integer, default=200, nullable=False)


class snapshots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP)

class field_goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    FGM = db.Column(db.Integer)
    Att = db.Column(db.Integer)
    FG_percent = db.Column(db.Float)
    Lng = db.Column(db.Integer)
    FG_Blk = db.Column(db.Integer)

class interceptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    INT = db.Column(db.Integer)
    INT_TD = db.Column(db.Integer)
    INT_Yds = db.Column(db.Integer)
    Lng = db.Column(db.Integer)

class passing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Pass_Yds = db.Column(db.Integer)
    Att = db.Column(db.Integer)
    Cmp = db.Column(db.Integer)
    Cmp_percent = db.Column(db.Float)
    TD = db.Column(db.Integer)
    INT = db.Column(db.Integer)
    Rate = db.Column(db.Float)
    Sck = db.Column(db.Integer)

class receiving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Rec = db.Column(db.Integer)
    Yds = db.Column(db.Integer)
    TD = db.Column(db.Integer)
    LNG = db.Column(db.Integer)
    Rec_FUM = db.Column(db.Integer)
    Tgts = db.Column(db.Integer)

class rushing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Rush_Yds = db.Column(db.Integer)
    Att = db.Column(db.Integer)
    TD = db.Column(db.Integer)
    Lng = db.Column(db.Integer)
    Rush_FUM = db.Column(db.Integer)

class tackles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Comb = db.Column(db.Integer)
    Asst = db.Column(db.Integer)
    Solo = db.Column(db.Integer)
    Sck = db.Column(db.Integer)

class team_passing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    Att = db.Column(db.Integer)
    Cmp = db.Column(db.Integer)
    Cmp_percent = db.Column(db.Float)
    Pass_Yds = db.Column(db.Integer)
    TD = db.Column(db.Integer)
    INT = db.Column(db.Integer)
    Rate = db.Column(db.Float)
    Sck = db.Column(db.Integer)    
    SckY = db.Column(db.Integer)

class team_rushing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    Att = db.Column(db.Integer)
    Rush_Yds = db.Column(db.Integer)
    YPC = db.Column(db.Float)
    TD = db.Column(db.Integer)
    Rush_FUM = db.Column(db.Integer)

class team_receiving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    Rec = db.Column(db.Integer)
    Yds = db.Column(db.Integer)
    TD = db.Column(db.Integer)
    Rec_FUM = db.Column(db.Integer)

class team_defense_passing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    Att = db.Column(db.Integer)
    Cmp = db.Column(db.Integer)
    Cmp_percent = db.Column(db.Float)
    Yds = db.Column(db.Integer)
    TD = db.Column(db.Integer)
    INT = db.Column(db.Integer)
    Rate = db.Column(db.Float)
    Sck = db.Column(db.Integer) 

class team_defense_rushing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    Att = db.Column(db.Integer)
    Rush_Yds = db.Column(db.Integer)
    YPC = db.Column(db.Float)
    TD = db.Column(db.Integer)
    Rush_FUM = db.Column(db.Integer)  

class team_defense_receiving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    Rec = db.Column(db.Integer)
    Yds = db.Column(db.Integer)
    TD = db.Column(db.Integer)
    Rec_FUM = db.Column(db.Integer)
    PDef = db.Column(db.Integer)  

class draft_odds_pick1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Odds = db.Column(db.String(100))
    is_drafted = db.Column(db.Boolean)
    pick_number = db.Column(db.Integer, nullable=False)

class draft_odds_pick2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Odds = db.Column(db.String(100))
    is_drafted = db.Column(db.Boolean)
    pick_number = db.Column(db.Integer, nullable=False)

class draft_odds_pick3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Odds = db.Column(db.String(100))
    is_drafted = db.Column(db.Boolean)
    pick_number = db.Column(db.Integer, nullable=False)

class draft_odds_pick4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Odds = db.Column(db.String(100))
    is_drafted = db.Column(db.Boolean)
    pick_number = db.Column(db.Integer, nullable=False)

class draft_odds_pick5(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Player = db.Column(db.String(100))
    Odds = db.Column(db.String(100))
    is_drafted = db.Column(db.Boolean)
    pick_number = db.Column(db.Integer, nullable=False)

class week1_odds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Home = db.Column(db.String(45))
    Away = db.Column(db.String(45))
    Home_spread = db.Column(db.String(10))
    Home_spread_odds = db.Column(db.String(10))
    Home_ml = db.Column(db.String(10))
    Away_spread = db.Column(db.String(10))
    Away_spread_odds = db.Column(db.String(10))
    Away_ml = db.Column(db.String(10))
    game_total = db.Column(db.Float)
    game_total_odds = db.Column(db.String(10))

class superbowl_odds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    snapshot_id = db.Column(db.Integer, db.ForeignKey('snapshots.id'))
    Team = db.Column(db.String(100))
    odds = db.Column(db.String(10))
    is_champion = db.Column(db.Boolean)

class bets_draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('draft_odds_pick1.id'), nullable=False)
    pick_number = db.Column(db.Integer, nullable=False)
    odds = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    potential_payout = db.Column(db.Float)
    placed_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_won = db.Column(db.Boolean, default=False)
    is_evaluated = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('bets_draft', lazy=True))

    def __init__(self, user_id, player, pick_number, odds, amount):
        self.user_id = user_id
        self.player_id = player
        self.pick_number = pick_number
        self.odds = odds
        self.amount = amount

        if odds.startswith('-'):
            positive_odds = abs(int(odds))
            self.potential_payout = ((100 / positive_odds) * self.amount) + self.amount
        elif odds.startswith('+'):
            positive_odds = int(odds[1:])
            self.potential_payout = ((positive_odds / 100) * self.amount) + self.amount
        else:
            positive_odds = int(odds)
            self.potential_payout = ((positive_odds / 100) * self.amount) + self.amount

    def __repr__(self):
        return f'<Betting {self.id} - User {self.user_id} bet {self.amount} on player {self.player_id} with potential payout {self.potential_payout}>'

class bets_week1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('week1_odds.id'), nullable=False)
    bet_type = db.Column(db.String(100), nullable=False)
    odds = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    potential_payout = db.Column(db.Float)
    placed_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_won = db.Column(db.Boolean, default=False)
    is_evaluated = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('bets_week1', lazy=True))

    def __init__(self, user_id, game_id, bet_type, odds, amount):
        self.user_id = user_id
        self.game_id = game_id
        self.bet_type = bet_type
        self.odds = odds
        self.amount = amount
        self.potential_payout = self.calculate_payout()

    def calculate_payout(self):
        if self.odds.startswith('-'):
            positive_odds = abs(int(self.odds))
            return (100 / positive_odds) * self.amount + self.amount
        elif self.odds.startswith('+'):
            positive_odds = int(self.odds[1:])
            return (positive_odds / 100) * self.amount + self.amount
        else:
            positive_odds = int(self.odds)
            return (positive_odds / 100) * self.amount + self.amount

    def __repr__(self):
        return f'<BetsWeek1 {self.id} - User {self.user_id} bet {self.amount} on game {self.game_id} with potential payout {self.potential_payout}>'

class bets_superbowl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Team = db.Column(db.String(100), nullable=False)
    odds = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    potential_payout = db.Column(db.Float)
    placed_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_won = db.Column(db.Boolean, default=False)
    is_evaluated = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('bets_superbowl', lazy=True))

    def __init__(self, user_id, Team, odds, amount):
        self.user_id = user_id
        self.Team = Team
        self.odds = odds
        self.amount = amount
        self.potential_payout = self.calculate_payout()

    def calculate_payout(self):
        if self.odds.startswith('-'):
            positive_odds = abs(int(self.odds))
            return (100 / positive_odds) * self.amount + self.amount
        elif self.odds.startswith('+'):
            positive_odds = int(self.odds[1:])
            return (positive_odds / 100) * self.amount + self.amount
        else:
            positive_odds = int(self.odds)
            return (positive_odds / 100) * self.amount + self.amount

    def __repr__(self):
        return f'<BetsSuperBowl {self.id} - User {self.user_id} bet {self.amount} on Team {self.Team} with potential payout {self.potential_payout}>'
 

