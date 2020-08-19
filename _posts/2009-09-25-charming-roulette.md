---
layout: post
title: Charming Roulette
date: 2009-09-25T11:28:25.000Z
type: post
tags:
  - gambling
  - roulette
  - statistics
  - python
permalink: /2009/09/25/charming-roulette/
flickr_user: 'https://www.flickr.com/people/johnwardell/'
flickr_username: John Wardell (Netinho)
flickr_image: 'https://live.staticflickr.com/43/80125882_3347a3ab46_w.jpg'
flickr_imagelink: 'http://www.flickr.com/photos/johnwardell/80125882/'
flickr_imagename: Roulette wheel
---
Recently I went to a wedding which had a casino theme. To keep the guests entertained they gave every guest $100 from the Bank Of Fun to spend on the roulette and black jack tables. I decided to play roulette and I knew that the best way to maximise my chances of winning was to bet only on odd or even and to double my bet whenever I lost. At one point I was 2.6x up on my initial stake, but unfortunately, as you'd expect, I eventually lost the lot.

I want to see what I could have done to increase my peak winnings, and to try my best to leave the table with a positive cash flow. To do this we'll simulate a roulette table using Python and try out various betting strategies. The Roulette wheel that was used at the Wedding was an American wheel and featured the numbers 1 to 36 as well as 0 and 00. Betting on odd or even will win if a number 1 to 36 comes up and it is odd or even. 0 or 00 will lose you your money. If you win your stake is doubled. This means that by betting on odd or even you stand a 47% chance of winning.

To help work out the best strategy we need to build a roulette wheel simulator. To do this we use the Python function given below. It takes four parameters and returns the amount money left at the end of the run. The first parameter is the amount of money to start with, the second is a function which takes the current amount of money and returns the bet. The next to function determine when to give up - either a limit on the number of rounds, or the amount of money to stop at. The variable `wheel` is a list containing 18 "odd" strings, 18 "even" strings as well as one "0" and one "00" string.

    from random import choicen
    def roulette(stake, bet_func, go_limit=None, walk_away=None):
        go = 0
        while stake &gt; 0 and (go_limit is None or go &lt; go_limit) and (walk_away is None or stake &lt; walk_away):
            go += 1
            bet = bet_func(stake)
            if bet &gt; stake: bet = stake
            if choice(wheel) == &quot;odd&quot;:
                stake += bet
            else:<br />
                stake -= bet
        return stake

So, with the simulation in place let's start working out some odds. The simplest betting strategy is to bet $1 each round. To do this we used this simple betting function.

    def flat_bet(stake):
        return 1

The graph below shows how likely you are to win when following this strategy for the given target. As you can see if you only want to increase you money from $100 to $101 then you've a 90% chance of doing this betting $1 each go. However, if you set your sights higher then your chances quickly diminish and you've almost no chance of making even a $40 profit.

<img src="{{ site.baseurl }}/assets/chart?cht=lc&amp;chs=400x250&amp;chd=e:5u0ywUoYkah6eRawYxWVThSDR7OFNsKXKsI5IMHPFxGNF1FEFIEWEWDZCYCgB3CYBaB7CLBSBWBCA5BCAdA5AdAdApAtAZAZAUAh&amp;chco=0000FF&amp;chxt=y,x&amp;chxl=0:||20%25|40%25|60%25|80%25|100%25|1:|101|111|121|131|141|151&amp;chg=0,25,5,5" alt="Constant $1 bet with an increasing target" />

The strategy I used was to double my bet every time I lost and reset to a $1 bet when I won. This means that on average you only stand to win $1 per round, but because your bet is doubled each win wipes out any previous loses. The code for this bet function is more complicated and we need to use a callable class to store the state of our bet.

    class scale_bet:
        def __init__(self, scale):
            self.bet = 1
            self.scale = scale
            self.prev_stake = None
        def __call__(self, stake):
            if self.prev_stake is None or stake &gt; self.prev_stake:
                self.bet = 1
            else:
                self.bet *= self.scale
            self.prev_stake = stake
            return math.floor(self.bet)

The probably of winning is much better with the doubling strategy, and if you're aiming for increasing your cash pile to $250 then you have a 25% chance of doing that.

<img src="{{ site.baseurl }}/assets/chart?cht=lc&amp;chs=400x250&amp;chd=e:kvf3h2iPmNgtf3crc.ehWVUeSfRaRyPrQAN9OqMaNsLtKHJuJaIlKLIEGmIdG-GNHnGVGeGRFUF1F9FoFg&amp;chco=0000FF&amp;chxt=y,x&amp;chxl=0:||20%25|40%25|60%25|80%25|100%25|1:|101|201|301|401|501&amp;chg=0,25,5,5" alt="Doubling bet with a $1 reset and an increasing target" />

The chances of winning are much better if you double your bet, but why stop at doubling? In the next test I aimed for a target of $200 and increased the scaling factor of the bet from 0.1 to 50. You can see from the graph below that increasing the scaling factor doesn't change your chances of winning, instead it remains at about 47%.

<img src="{{ site.baseurl }}/assets/chart?cht=lc&amp;chs=400x250&amp;chd=e:AAc7eVfXfCdwdLfOfndDdgcadoe-dDfjfzgAd0eqfSdPdscKbtd8e2eVe2gYeZd8dHczfCeqeJfKc3dweyfGhFc.ffffeRdoedeB&amp;chco=0000FF&amp;chxt=y,x&amp;chxl=0:||20%25|40%25|60%25|80%25|100%25|1:|0|10|20|30|40|50&amp;chg=0,25,5,5" alt="Chances of reaching $200 with an increasing scaled bet and a $1 reset" />

The final chart shows the chance of reaching $200 with a bet which doubles when you lose. In this test the starting bet is set so that you have at least <i>x</i> goes remaining. We begin with having only one possible other bet, and go up to twenty. Despite what you might think, the chances of winning do not really change much.

<img src="{{ site.baseurl }}/assets/chart?cht=lc&amp;chs=400x250&amp;chd=e:fPemdjd6dWeFd.eddpbkd-eud8d8eTeqeFeKdief&amp;chco=0000FF&amp;chxt=y,x&amp;chxl=0:||20%25|40%25|60%25|80%25|100%25|1:|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20&amp;chg=0,25,5,5" alt="Chances of reaching $200 with an doubling bet and an increasing reset" />

So, what's the outcome of all this? What ever you do, you've got a less than 50/50 chance of winning, but doubling your bet each time you lose will give a longer run before your lose your house.

Charts generated with Google Charts.
