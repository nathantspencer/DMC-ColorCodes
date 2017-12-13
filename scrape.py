#| Nathan Spencer 2017
#| ntspencer@mix.wvu.edu

from bs4 import BeautifulSoup
import requests
import code

colors = []

# class for printing colored output
class colorizer:
	END = '\033[0m'
	GREEN = '\033[92m'

"""
Runs the scraper and writes the resulting CSV.
"""
def main():

	scrape_colors()
	write_csv()
	print(colorizer.GREEN + 'Scraping completed.\r\n' + colorizer.END)

"""
Populates `colors` by scraping from `http://www.camelia.sk` color tables.
"""
def scrape_colors():

	global colors

	paths_to_scrape = []
	for i in range (1, 7):
		paths_to_scrape.append('http://www.camelia.sk/dmc_' + str(i) + '.htm')

	for path in paths_to_scrape:
		print('\r\nRequesting page...')
		response = requests.get(path)
		print('Parsing XML...')
		root_parse_tree = BeautifulSoup(response.text, 'lxml')

		# the fourth tbody on each page contains the DMC colors
		print('Finding color table...')
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
					dmc_code = cell.get_text().lstrip()

				# second cell contains color name
				elif cell_index % 3 == 1:
					raw_text = cell.get_text()
					color_words = raw_text.split()
					for color in color_words:
						color_name = color_name + color + ' '
					color_name = color_name.rstrip()

				# third cell contains rgb color code
				else:
					rgb_code = cell['bgcolor']
					color = (dmc_code, color_name, rgb_code)
					colors.append(color)
					dmc_code = ''
					color_name = ''
					rgb_code = ''

"""
Writes contents of `colors` to a CSV file `result.csv` in the current directory.
"""
def write_csv():

	print('\r\nOpening CSV file...')
	file_handle = open('result.csv', 'w')

	print('Writing CSV file...')
	file_handle.write('DMC_COLOR, COLOR_NAME, RGB_COLOR\r\n')
	for color in colors:
		file_handle.write(color[0] + ', ')
		file_handle.write(color[1] + ', ')
		file_handle.write(color[2] + '\r\n')

	file_handle.close()

if __name__ == '__main__':
	main()
