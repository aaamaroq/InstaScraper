from insta_scraper import InstagramScraper
from tqdm import tqdm
import argparse
import logging
import json
import time

logging.basicConfig(level=logging.INFO)

def main():

	parser = argparse.ArgumentParser(description='Instagram followers scrapper')
	parser.add_argument('--username', dest='username', action='store')
	parser.add_argument('--password', dest='password', action='store')
	args = parser.parse_args()

	scrapper = InstagramScraper(args.username, args.password)
	logging.info("Creating session")
	scrapper.create_session()


	logging.info("Extracting my followees")
	seguidores = scrapper.scrape_following(args.username)

	map = dict()
	#Introduzco mis datos
	map[args.username] = seguidores

	logging.info("Extracting followees of people")
	# Inicializar la barra de progreso
	pbar = tqdm(seguidores, desc="Recorriendo seguidores", ncols=80)

	# Recorrer todos los seguidores
	for seguidor in pbar:
		time.sleep(1)
		# Actualizar la barra de progreso
		pbar.set_postfix({"Seguidor actual": seguidor})
		# Para cada seguidor, guardar su relación con sus seguidores
		map[seguidor] = scrapper.scrape_following(seguidor)
		pbar.update(1)

	# Cerrar la barra de progreso
	pbar.close()

	
	#Guardo como json el map
	with open("relaciones.json", 'w') as archivo:
		json.dump(map, archivo)

		





if __name__ == '__main__':
	main()