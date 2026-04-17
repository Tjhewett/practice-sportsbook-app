# API endpoints GET/POST to move data between MySQL and React 

from app import db, bcrypt
from app.models import User, snapshots, field_goals, interceptions, passing, receiving, rushing, tackles, team_passing, team_rushing, team_receiving, team_defense_passing, team_defense_rushing, team_defense_receiving, draft_odds_pick1, draft_odds_pick2, draft_odds_pick3, draft_odds_pick4, draft_odds_pick5, week1_odds, superbowl_odds, bets_draft, bets_week1, bets_superbowl
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint instance
views_bp = Blueprint('views_bp', __name__)


################################
#### User management Routes ####
################################

@views_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    location = data.get('location')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if user already exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    # Create a new user
    new_user = User(email=email, password=hashed_password, username=username, location=location)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@views_bp.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email_or_username = data.get('emailOrUsername')
    password = data.get('password')

    # Find user by email or username
    user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Incorrect email/username or password'}), 401

@views_bp.route('/api/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')

    # Check if user already exists
    user_exists = User.query.filter((User.email == email) | (User.username == username)).first() is not None

    return jsonify({'exists': user_exists})

@views_bp.route('/api/account', methods=['GET'])
@jwt_required()
def get_account_info():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id, description="No user found with this ID.")
        
        
        user_info = {
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.strftime('%Y-%m-%d'),
            "currency": user.currency
        }
        
        return jsonify(user_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#################################
#### Statistical Data Routes #### 
#################################

@views_bp.route('/api/snapshots', methods=['GET'])
def get_snapshots():
    all_snapshots = snapshots.query.all()
    return jsonify([{'id': s.id, 'timestamp': s.timestamp} for s in all_snapshots])


@views_bp.route('/api/field_goals', methods=['GET'])
def get_field_goals():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    paginated_field_goals = field_goals.query.filter_by(snapshot_id=most_recent_snapshot.id).paginate(page=page, per_page=per_page, error_out=False)
    items = [{
        'Player': fg.Player,
        'FGM': fg.FGM,
        'Att': fg.Att,
        'FG_percent': fg.FG_percent,
        'Lng': fg.Lng,
        'FG_Blk': fg.FG_Blk
    } for fg in paginated_field_goals.items]
    return jsonify({
        'items': items,
        'total': paginated_field_goals.total,
        'pages': paginated_field_goals.pages,
        'page': paginated_field_goals.page
    })

@views_bp.route('/api/interceptions', methods=['GET'])
def get_interceptions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    paginated_interceptions = interceptions.query.filter_by(snapshot_id=most_recent_snapshot.id).paginate(page=page, per_page=per_page, error_out=False)
    items = [{
        'Player': i.Player,
        'INT': i.INT,
        'INT_TD': i.INT_TD,
        'INT_Yds': i.INT_Yds,
        'Lng': i.Lng
    } for i in paginated_interceptions.items]
    return jsonify({
        'items': items,
        'total': paginated_interceptions.total,
        'pages': paginated_interceptions.pages,
        'page': paginated_interceptions.page
    })

@views_bp.route('/api/passing', methods=['GET'])
def get_passing():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    paginated_passing = passing.query.filter_by(snapshot_id=most_recent_snapshot.id).paginate(page=page, per_page=per_page, error_out=False)
    items = [{
        'Player': p.Player,
        'Pass_Yds': p.Pass_Yds,
        'Att': p.Att,
        'Cmp': p.Cmp,
        'TD': p.TD,
        'INT': p.INT,
        'Rate': p.Rate,
        'Sck': p.Sck
    } for p in paginated_passing.items]
    return jsonify({
        'items': items,
        'total': paginated_passing.total,
        'pages': paginated_passing.pages,
        'page': paginated_passing.page
    })

@views_bp.route('/api/receiving', methods=['GET'])
def get_receiving():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    paginated_receiving = receiving.query.filter_by(snapshot_id=most_recent_snapshot.id).paginate(page=page, per_page=per_page, error_out=False)
    items = [{
        'Player': r.Player,
        'Rec': r.Rec,
        'Yds': r.Yds,
        'TD': r.TD,
        'LNG': r.LNG,
        'Rec_FUM': r.Rec_FUM,
        'Tgts': r.Tgts
    } for r in paginated_receiving.items]
    return jsonify({
        'items': items,
        'total': paginated_receiving.total,
        'pages': paginated_receiving.pages,
        'page': paginated_receiving.page
    })

@views_bp.route('/api/rushing', methods=['GET'])
def get_rushing():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    paginated_rushing = rushing.query.filter_by(snapshot_id=most_recent_snapshot.id).paginate(page=page, per_page=per_page, error_out=False)
    items = [{
        'Player': r.Player,
        'Rush_Yds': r.Rush_Yds,
        'Att': r.Att,
        'TD': r.TD,
        'Lng': r.Lng,
        'Rush_FUM': r.Rush_FUM
    } for r in paginated_rushing.items]
    return jsonify({
        'items': items,
        'total': paginated_rushing.total,
        'pages': paginated_rushing.pages,
        'page': paginated_rushing.page
    })

@views_bp.route('/api/tackles', methods=['GET'])
def get_tackles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    paginated_tackles = tackles.query.filter_by(snapshot_id=most_recent_snapshot.id).paginate(page=page, per_page=per_page, error_out=False)
    items = [{
        'Player': t.Player,
        'Comb': t.Comb,
        'Asst': t.Asst,
        'Solo': t.Solo,
        'Sck': t.Sck
    } for t in paginated_tackles.items]
    return jsonify({
        'items': items,
        'total': paginated_tackles.total,
        'pages': paginated_tackles.pages,
        'page': paginated_tackles.page
    })

@views_bp.route('/api/team_passing', methods=['GET'])
def get_team_passing():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    team_passing_data = team_passing.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': tp.Team,
        'Att': tp.Att,
        'Cmp': tp.Cmp,
        'Cmp_percent': tp.Cmp_percent,
        'Pass_Yds': tp.Pass_Yds,
        'TD': tp.TD,
        'INT': tp.INT,
        'Rate': tp.Rate,
        'Sck': tp.Sck,
        'SckY': tp.SckY
    } for tp in team_passing_data]
    return jsonify(entries)

@views_bp.route('/api/team_rushing', methods=['GET'])
def get_team_rushing():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    team_rushing_data = team_rushing.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': tr.Team,
        'Att': tr.Att,
        'Rush_Yds': tr.Rush_Yds,
        'YPC': tr.YPC,
        'TD': tr.TD,
        'Rush_FUM': tr.Rush_FUM
    } for tr in team_rushing_data]
    return jsonify(entries)

@views_bp.route('/api/team_receiving', methods=['GET'])
def get_team_receiving():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    team_receiving_data = team_receiving.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': trc.Team,
        'Rec': trc.Rec,
        'Yds': trc.Yds,
        'TD': trc.TD,
        'Rec_FUM': trc.Rec_FUM
    } for trc in team_receiving_data]
    return jsonify(entries)

@views_bp.route('/api/team_defense_passing', methods=['GET'])
def get_team_defense_passing():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    team_defense_passing_data = team_defense_passing.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': tdp.Team,
        'Att': tdp.Att,
        'Cmp': tdp.Cmp,
        'Cmp_percent': tdp.Cmp_percent,
        'Yds': tdp.Yds,
        'TD': tdp.TD,
        'INT': tdp.INT,
        'Rate': tdp.Rate,
        'Sck': tdp.Sck
    } for tdp in team_defense_passing_data]
    return jsonify(entries)

@views_bp.route('/api/team_defense_rushing', methods=['GET'])
def get_team_defense_rushing():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    team_defense_rushing_data = team_defense_rushing.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': tdr.Team,
        'Att': tdr.Att,
        'Rush_Yds': tdr.Rush_Yds,
        'YPC': tdr.YPC,
        'TD': tdr.TD,
        'Rush_FUM': tdr.Rush_FUM
    } for tdr in team_defense_rushing_data]
    return jsonify(entries)

@views_bp.route('/api/team_defense_receiving', methods=['GET'])
def get_team_defense_receiving():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    team_defense_receiving_data = team_defense_receiving.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': tdrc.Team,
        'Rec': tdrc.Rec,
        'Yds': tdrc.Yds,
        'TD': tdrc.TD,
        'Rec_FUM': tdrc.Rec_FUM,
        'PDef': tdrc.PDef
    } for tdrc in team_defense_receiving_data]
    return jsonify(entries)

#################################
#### Betting Data Routes ########
#################################

@views_bp.route('/api/draft_odds_pick1', methods=['GET'])
def get_draft_odds_pick1():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    draft_odds_data = draft_odds_pick1.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'id': do.id,
        'Player': do.Player,
        'Odds': do.Odds,
        'pick_number': do.pick_number
    } for do in draft_odds_data]
    return jsonify(entries)

@views_bp.route('/api/draft_odds_pick2', methods=['GET'])
def get_draft_odds_pick2():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    draft_odds_data = draft_odds_pick2.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'id': do.id,
        'Player': do.Player,
        'Odds': do.Odds,
        'pick_number': do.pick_number
    } for do in draft_odds_data]
    return jsonify(entries)

@views_bp.route('/api/draft_odds_pick3', methods=['GET'])
def get_draft_odds_pick3():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    draft_odds_data = draft_odds_pick3.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'id': do.id,
        'Player': do.Player,
        'Odds': do.Odds,
        'pick_number': do.pick_number
    } for do in draft_odds_data]
    return jsonify(entries)

@views_bp.route('/api/draft_odds_pick4', methods=['GET'])
def get_draft_odds_pick4():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    draft_odds_data = draft_odds_pick4.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'id': do.id,
        'Player': do.Player,
        'Odds': do.Odds,
        'pick_number': do.pick_number
    } for do in draft_odds_data]
    return jsonify(entries)

@views_bp.route('/api/draft_odds_pick5', methods=['GET'])
def get_draft_odds_pick5():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    draft_odds_data = draft_odds_pick5.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'id': do.id,
        'Player': do.Player,
        'Odds': do.Odds,
        'pick_number': do.pick_number
    } for do in draft_odds_data]
    return jsonify(entries)

@views_bp.route('/api/week1_odds', methods=['GET'])
def get_week1_odds():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    week1_odds_data = week1_odds.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'id': wo.id,
        'Home': wo.Home,
        'Away': wo.Away,
        'Home_spread': wo.Home_spread,
        'Home_spread_odds': wo.Home_spread_odds,
        'Home_ml': wo.Home_ml,
        'Away_spread': wo.Away_spread,
        'Away_spread_odds': wo.Away_spread_odds,
        'Away_ml': wo.Away_ml,
        'game_total': wo.game_total,
        'game_total_odds': wo.game_total_odds,
    } for wo in week1_odds_data]
    return jsonify(entries)

@views_bp.route('/api/superbowl_odds', methods=['GET'])
def get_superbowl_odds():
    most_recent_snapshot = snapshots.query.order_by(snapshots.timestamp.desc()).first()
    if not most_recent_snapshot:
        return jsonify({'error': 'No recent snapshot found'}), 404

    superbowl_odds_data = superbowl_odds.query.filter_by(snapshot_id=most_recent_snapshot.id).all()
    entries = [{
        'Team': so.Team,
        'odds': so.odds
    } for so in superbowl_odds_data]
    return jsonify(entries)

@views_bp.route('/api/place_bet_draft', methods=['POST'])
@jwt_required()
def place_bet_draft():
    try:
        data = request.get_json()
        player_id = data.get('id')
        pick_number = data.get('pick_number')
        odds = data.get('odds')
        amount = data.get('amount')
        

        if not all([player_id, pick_number, odds, amount ]):
            return jsonify({'error': 'Missing required parameters'}), 400

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400

        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        if amount > user.currency:
            return jsonify({'error': 'Insufficient funds'}), 400

        new_bet = bets_draft(user_id=user.id, player=player_id, pick_number=pick_number, odds=odds, amount=amount)
        db.session.add(new_bet)

        user.currency -= amount
        db.session.commit()

        return jsonify({'newCurrency': user.currency}), 200

    except Exception as e:
        print(f'Error placing bet: {str(e)}')  # Logging the exception
        db.session.rollback()  # Ensure no partial changes are committed
        return jsonify({'error': 'Internal Server Error'}), 500

@views_bp.route('/api/place_bet_week1', methods=['POST'])
@jwt_required()
def place_bet_week1():
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        bet_type = data.get('bet_type')
        odds = data.get('odds')
        amount = data.get('amount')
        

        if not all([game_id, bet_type, odds, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400

        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        if amount > user.currency:
            return jsonify({'error': 'Insufficient funds'}), 400

        new_bet_week1 = bets_week1(user_id=user.id, game_id=game_id, bet_type=bet_type, odds=odds, amount=amount)
        db.session.add(new_bet_week1)

        user.currency -= amount
        db.session.commit()

        return jsonify({'newCurrency': user.currency}), 200

    except Exception as e:
        print(f'Error placing bet: {str(e)}')  # Logging the exception
        db.session.rollback()  # Ensure no partial changes are committed
        return jsonify({'error': 'Internal Server Error'}), 500

@views_bp.route('/api/place_bet_superbowl', methods=['POST'])
@jwt_required()
def place_bet_superbowl():
    try:
        data = request.get_json()
        Team = data.get('Team')
        odds = data.get('odds')
        amount = data.get('amount')
        

        if not all([Team, odds, amount]):
            return jsonify({'error': 'Missing required parameters'}), 400

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400

        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        if amount > user.currency:
            return jsonify({'error': 'Insufficient funds'}), 400

        new_bet_superbowl = bets_superbowl(user_id=user.id, Team=Team, odds=odds, amount=amount)
        db.session.add(new_bet_superbowl)

        user.currency -= amount
        db.session.commit()

        return jsonify({'newCurrency': user.currency}), 200

    except Exception as e:
        print(f'Error placing bet: {str(e)}')  # Logging the exception
        db.session.rollback()  # Ensure no partial changes are committed
        return jsonify({'error': 'Internal Server Error'}), 500

@views_bp.route('/api/user_bets', methods=['GET'])
@jwt_required()
def get_user_bets():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Query both bets tables for the current user
        draft_bets = bets_draft.query.filter_by(user_id=current_user_id).all()
        week1_bets = bets_week1.query.filter_by(user_id=current_user_id).all()
        superbowl_bets = bets_superbowl.query.filter_by(user_id=current_user_id).all()

        # Combine results
        bets = []

        for bet in draft_bets:
            bets.append({
                'bet_type': 'draft',
                'player_id': bet.player_id,
                'pick_number': bet.pick_number,
                'odds': bet.odds,
                'amount': bet.amount,
                'potential_payout': bet.potential_payout,
                'placed_at': bet.placed_at,
                'is_evaluated': bet.is_evaluated
            })

        for bet in week1_bets:
            bets.append({
                'bet_type': 'week1',
                'game_id': bet.game_id,
                'bet_type_details': bet.bet_type,
                'odds': bet.odds,
                'amount': bet.amount,
                'potential_payout': bet.potential_payout,
                'placed_at': bet.placed_at,
                'is_evaluated': bet.is_evaluated
            })
        
        for bet in superbowl_bets:
            bets.append({
                'bet_type': 'Superbowl',
                'team': bet.Team,
                'odds': bet.odds,
                'amount': bet.amount,
                'potential_payout': bet.potential_payout,
                'placed_at': bet.placed_at,
                'is_evaluated': bet.is_evaluated
            })

        return jsonify(bets), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@views_bp.route('/api/update_currency', methods=['POST'])
@jwt_required()
def update_currency():
    user_id = get_jwt_identity()  # Get user ID from the JWT
    score = request.json.get('score', 0)
    # Calculate currency change based on score, e.g., 1 point = 1 cent
    additional_currency = score * 0.01

    try:
        user = User.query.get(user_id)
        if user:
            user.currency += additional_currency
            db.session.commit()
            return jsonify({'newCurrency': user.currency, 'message': 'Currency updated successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating currency', 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        fetch_and_store_data()  # Call the function to fetch and store data
    app.run(debug=True)