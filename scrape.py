#| Nathan Spencer 2017
#| ntspencer@mix.wvu.edu

from bs4 import BeautifulSoup
import requests
import code

colors = []

def main():

	scrape_colors()


def scrape_colors():

	global colors

	paths_to_scrape = []
	for i in range (1, 7):
		paths_to_scrape.append('http://www.camelia.sk/dmc_' + str(i) + '.htm')

	for path in paths_to_scrape:
		response = requests.get(path)
		root_parse_tree = BeautifulSoup(response.text, 'lxml')

		# the fourth tbody on each page contains the DMC colors
		tables = root_parse_tree.find_all('tbody')
		for row_index, row in enumerate(tables[4]):

			# the first row is a header, so we'll skip it
			if row_index == 1:
				continue

			row_utf8 = row.encode('utf-8')
			row_parse_tree = BeautifulSoup(row_utf8, 'lxml')
			cells = row_parse_tree.find_all('td')

			dmc_code = ''
			color_name = ''
			rgb_code = ''

			for cell_index, cell in enumerate(cells):

				# first cell contains dmc color code
				if cell_index % 3 == 0:
					dmc_code = cell.get_text()

				# second cell contains color name
				elif cell_index % 3 == 1:
					color_name = cell.get_text()

				# third cell contains rgb color code
				else:
					rgb_code = cell['bgcolor']
					print((dmc_code, color_name, rgb_code))


if __name__ == '__main__':
	main()
