# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

from synodlnatrakt.encodingKludge import fixStupidEncodings

def ex(e):
	"""
	Returns a unicode string from the exception text if it exists.
	"""
	
	# sanity check
	if not e.args or not e.args[0]:
		return ""

	e_message = fixStupidEncodings(e.args[0], True)
	
	# if fixStupidEncodings doesn't fix it then maybe it's not a string, in which case we'll try printing it anyway
	if not e_message:
		try:
			e_message = str(e.args[0])
		except:
			e_message = ""
	
	return e_message
	