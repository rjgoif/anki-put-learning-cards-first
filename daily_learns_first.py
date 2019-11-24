# # # -*- coding: utf-8 -*-

#########################################################################
# Copyright (C) 2014–2020 by anki/github user rjgoif <https://github.com/rjgoif/>
#                                                                       #
# This program is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

## this is an Anki 2.1 update of my popular Anki 2.0 add-on
## that changes the order of your daily reviews: 

## This is a simple add-on that inserts the daily-learning cards, i.e.
## cards in the learning queue with intervals that crossed the day turnover,
## before starting standard reviews (the green number). Normally these cards
## daily-learning cards go last, but I want them to go first. 

## as of beta 32, there is an option to enable this built into Anki if you are using the 
## v2 scheduler. 
## HOWEVER, I still think the learning reviews should come before new reviews. So I have built that in. If you use v2, this add-on respects the option toggle built into native Anki.
## I won't be testing v2 myself, so if it works for you please let me know via Github

## a legacy version will be uploaded to Github for anyone holding out with Anki 2.0.

## https://github.com/rjgoif/

# # # # # # # # # # # # # # # #

__version__ = '2.1.001'


# classic (ie from v2.0) scheduler
import anki.sched as oldSched
def _getCardReordered(self):
	"Return the next due card id, or None."
	# learning card due?
	c = self._getLrnCard()
	if c:
		return c
	# day learning card due?
	c = self._getLrnDayCard()
	if c:
		return c
	# new first, or time for one?
	if self._timeForNewCard():
		c = self._getNewCard()
		if c:
			return c
	# card due for review?
	c = self._getRevCard()
	if c:
		return c
	# new cards left?
	c = self._getNewCard()
	if c:
		return c
	# collapse or finish
	return self._getLrnCard(collapse=True)

	
oldSched.Scheduler._getCard = _getCardReordered




# # Anki 2.1 scheduler v2
import anki.schedv2 as oldSchedv2
def _getCardReorderedv2(self):
	"Return the next due card id, or None."
	# learning card due?
	c = self._getLrnCard()
	if c:
		return c

	# day learning first and card due?
	dayLearnFirst = self.col.conf.get("dayLearnFirst", False)
	c = dayLearnFirst and self._getLrnDayCard()
	if c:
		return c

	# new first, or time for one?
	if self._timeForNewCard():
		c = self._getNewCard()
		if c:
			return c

	# card due for review?
	c = self._getRevCard()
	if c:
		return c

	# day learning card due?
	c = not dayLearnFirst and self._getLrnDayCard()
	if c:
		return c

	# new cards left?
	c = self._getNewCard()
	if c:
		return c

	# collapse or finish
	return self._getLrnCard(collapse=True)

oldSchedv2.Scheduler._getCard = _getCardReorderedv2