from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import PlayersForm, ScoreForm
from app.models import Game, Score

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/numberplayers')
def numberplayers():
    game = Game.query.all()    

    if game:
        return render_template('warning.html', title='Careful!')
    else: 
        return render_template('numberplayers.html', title='How many players?')
    return render_template('numberplayers.html', title='How many players?')



@app.route('/nametheplayers/<numberplayers>', methods=['GET', 'POST'])
def nametheplayers(numberplayers):
    form = PlayersForm()

    if form.validate_on_submit():
        game = Game(
            numberofplayers=numberplayers,
            playerone = form.player1.data,
            playertwo = form.player2.data,
            playerthree = form.player3.data,
            playerfour = form.player4.data,
            playerfive = form.player5.data)
        db.session.add(game)
        db.session.commit()

        player1 = Score(name=form.player1.data, playerid=1)
        player2 = Score(name=form.player2.data, playerid=2)
        player3 = Score(name=form.player3.data, playerid=3)
        player4 = Score(name=form.player4.data, playerid=4)
        player5 = Score(name=form.player5.data, playerid=5)
        db.session.add(player1)
        db.session.add(player2)
        db.session.add(player3)
        db.session.add(player4)
        db.session.add(player5)
        db.session.commit()

        return redirect('/score')

    return render_template('nametheplayers.html', title='What are they called?', form=form, numberplayers=numberplayers)


@app.route('/reset')
def reset():
    game = Game.query.all()
    score = Score.query.all()

    for g in game:
        db.session.delete(g)
    for s in score:
        db.session.delete(s)
    db.session.commit()
    return redirect(url_for('numberplayers'))


@app.route('/score', methods=['GET', 'POST'])
def score():
    form = ScoreForm()
    # general variables
    currentgame = Game.query.filter_by(id=1).first()
    numberofplayers = currentgame.numberofplayers
    nextplayer = currentgame.nextplayer
    currentplayer = Score.query.filter_by(playerid = nextplayer).first()
    playerone = Score.query.filter_by(playerid = 1).first()
    playertwo = Score.query.filter_by(playerid = 2).first()
    playerthree = Score.query.filter_by(playerid = 3).first()
    playerfour = Score.query.filter_by(playerid = 4).first()
    playerfive = Score.query.filter_by(playerid = 5).first()

    subtotalupper = currentplayer.subtotalupper

    
    # check for end of game
    if numberofplayers ==2:
        if playerone.full == 'yes' and playertwo.full=='yes':
            return redirect(url_for('end'))


    elif numberofplayers==3:
        if playerone.full == 'yes' and playertwo.full=='yes' and playerthree.full=='yes':
            return redirect(url_for('end'))

    elif numberofplayers==4:
        if playerone.full == 'yes' and playertwo.full=='yes' and playerthree.full=='yes' and playerfour.full=='yes':
            return redirect(url_for('end'))

    elif numberofplayers==5:
        if playerone.full == 'yes' and playertwo.full=='yes' and playerthree.full=='yes' and playerfour.full=='yes' and playerfive.full =='yes':
            return redirect(url_for('end'))

    # get totals from all players
    totp1 = playerone.total
    totp2 = playertwo.total
    totp3 = playerthree.total
    totp4 = playerfour.total
    totp5 = playerfive.total

    # TODO: Fix the totals not showing up in real time
    # Perhaps calculating the totals at each round for all players? 

    # form actions
    if request.method == 'GET':
        form.ones.data = currentplayer.ones
        form.twos.data = currentplayer.twos
        form.threes.data = currentplayer.threes
        form.fours.data = currentplayer.fours
        form.fives.data = currentplayer.fives
        form.sixes.data = currentplayer.sixes
        form.threex.data = currentplayer.threex
        form.fourx.data = currentplayer.fourx
        form.fullhouse.data = currentplayer.fullhouse
        form.small.data = currentplayer.small
        form.large.data = currentplayer.large
        form.yahtzee.data = currentplayer.yahtzee
        form.chance.data = currentplayer.chance

            
    elif form.validate_on_submit():
        currentplayer.ones = form.ones.data
        currentplayer.twos = form.twos.data
        currentplayer.threes = form.threes.data
        currentplayer.fours = form.fours.data
        currentplayer.fives = form.fives.data
        currentplayer.sixes = form.sixes.data
        currentplayer.threex = form.threex.data
        currentplayer.fourx = form.fourx.data
        currentplayer.fullhouse = form.fullhouse.data
        currentplayer.small = form.small.data
        currentplayer.large = form.large.data
        currentplayer.yahtzee = form.yahtzee.data
        currentplayer.chance = form.chance.data
        db.session.commit()

        form.ones.data = ""
        form.twos.data = ""
        form.threes.data = ""
        form.fours.data = ""
        form.fives.data = ""
        form.sixes.data = ""
        form.threex.data = ""
        form.fourx.data = ""
        form.fullhouse.data = ""
        form.small.data = ""
        form.large.data = ""
        form.yahtzee.data = "" 
        form.chance.data = ""
        
        nextplayer = nextplayer + 1
        if nextplayer > numberofplayers:
            nextplayer = 1
        currentgame.nextplayer = nextplayer
        # db.session.commit()


        #pull scores
        ones = currentplayer.ones 
        twos = currentplayer.twos 
        threes = currentplayer.threes 
        fours = currentplayer.fours
        fives = currentplayer.fives
        sixes = currentplayer.sixes
        threex = currentplayer.threex 
        fourx = currentplayer.fourx 
        fullhouse = currentplayer.fullhouse 
        small = currentplayer.small
        large = currentplayer.large
        yahtzee = currentplayer.yahtzee
        chance = currentplayer.chance 
        
        # check for full card and mark as full
        if ones and twos and threes and fours and fives and sixes and threex and fourx and \
            fullhouse and small and large and yahtzee and chance:
            currentplayer.full = 'yes'

        # deal with empty strings
        if not ones:
            ones='0'
        if not twos:
            twos = '0'   
        if not threes:
            threes = '0'   
        if not fours:
            fours = '0'   
        if not fives:
            fives = '0'   
        if not sixes: 
            sixes = '0'  

        if not threex:
            threex='0'
        if not fourx:
            fourx = '0'   
        if not fullhouse:
            fullhouse = '0'   
        if not small:
            small = '0'   
        if not large:
            large = '0'   
        if not yahtzee: 
            yahtzee = '0'  
        if not chance:
            chance='0'

        # subtotal upper section
        subtotalupper = int(float(ones)) + int(float(twos)) + int(float(threes)) + int(float(fours)) \
             + int(float(fives)) + int(float(sixes))
        currentplayer.subtotalupper = subtotalupper
        
        # bonus upper section
        if subtotalupper > 62:
            bonus = 35
        else:
            bonus = 0 
        currentplayer.bonus = bonus
        

        # total lower section
        totallower = int(float(threex)) + int(float(fourx)) + int(float(fullhouse)) + int(float(small)) \
            + int(float(large)) + int(float(yahtzee)) + int(float(chance))
        currentplayer.totallower = totallower


        # total so far
        total = subtotalupper + bonus + totallower
        currentplayer.total = total

        db.session.commit()



        return redirect(url_for('score'))



    return render_template('score.html', title='Score', currentplayer=currentplayer, form=form,
        subtotalupper=subtotalupper, totp1 = totp1, playerone = playerone, totp2 = totp2, playertwo = playertwo, 
        totp3 = totp3, playerthree = playerthree, totp4 = totp4, playerfour = playerfour, totp5 = totp5, 
        playerfive = playerfive)

@app.route('/pause')
def pause():
    currentgame = Game.query.filter_by(id=1).first()
    nextplayer = currentgame.nextplayer 
    if nextplayer < 1:
        nextplayer = 3
    currentgame.nextplayer = nextplayer
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/end')
def end():
    # get all players
    playerone = Score.query.filter_by(playerid = 1).first()
    playertwo = Score.query.filter_by(playerid = 2).first()
    playerthree = Score.query.filter_by(playerid = 3).first()
    playerfour = Score.query.filter_by(playerid = 4).first()
    playerfive = Score.query.filter_by(playerid = 5).first()

    # get totals from all players
    totp1 = playerone.total
    totp2 = playertwo.total
    totp3 = playerthree.total
    totp4 = playerfour.total
    totp5 = playerfive.total

    return render_template('end.html', playerone=playerone,playertwo=playertwo,playerthree=playerthree,
        playerfour=playerfour, playerfive=playerfive, totp1=totp1, totp2=totp2,totp3=totp3, totp4=totp4,
        totp5=totp5)
