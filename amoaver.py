import json
from instagrapi import Client
from getpass import getpass

def instagram_login(username, password):
    client = Client()
    try:
        client.login(username, password)
        print("Inicio de sesión exitoso.")
        return client
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
        return None

def get_following(client, user_id):
    following_ids = client.user_following(user_id)
    return set(following_ids)

def get_common_users(client, target_username):
    my_user_id = client.user_id_from_username(client.username)
    my_following = get_following(client, my_user_id)

    target_user_id = client.user_id_from_username(target_username)
    target_following = get_following(client, target_user_id)

    common_users = my_following.intersection(target_following)
    common_usernames = [client.user_info(user_id).username for user_id in common_users]

    return common_usernames

if __name__ == "__main__":
    username = input("Introduzca su nombre de usuario: ")
    password = getpass("Introduzca su contraseña: ")
    client = instagram_login(username, password)

    if client:
        with open("perjudicados.json", "r") as file:
            perjudicados_data = json.load(file)

        common_users_map = {}
        for target_username in perjudicados_data:
            common_users = get_common_users(client, target_username)
            common_users_map[target_username] = common_users

        with open("resultado.json", "w") as file:
            json.dump(common_users_map, file, indent=2)

        print("Resultado guardado en 'resultado.json'.")