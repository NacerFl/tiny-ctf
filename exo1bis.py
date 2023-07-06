import socket

#My secret: c917b6545479a1c3c10fef57ced43b8390c94eeb66f8c3c71bc6e948b8400f74

#Welcome to the challenge !
#Here is your first Hint: 53e98c2129df4c8d74d62597e5125a03035a6bc3
#Don't forget that: 9bc1ebb7e87fda9e7e26092de414fe7c083dc6e3


import http.client
import json

IP_ADDRESS = '10.33.2.123'  # Remplacez par votre adresse IP cible

while True:
    for port in range(1024, 4096):
        #print(f"Port check  : {port}")
        conn = http.client.HTTPConnection(IP_ADDRESS, port, timeout=0.01)
        try:
            conn.request("GET", "/ping")
            response = conn.getresponse()
            if response.status == 200 and response.read().decode() == "pong":
                print(f"Port ouvert trouvé : {port}")
                print(f"Réponse du serveur : pong")

                signup_data = {"User": "nacer"}
                signup_body = json.dumps(signup_data)
                headers = {"Content-Type": "application/json"}

                conn.request("POST", "/signup", body=signup_body, headers=headers)
                signup_response = conn.getresponse()
                print(f"Réponse du serveur (signup) : {signup_response.status} {signup_response.reason}")



                conn.request("POST", "/getChallenge", body=signup_body, headers=headers)
                getChallenge_response = conn.getresponse()
                print(f"Réponse du serveur (getChallenge) : {getChallenge_response.status} {getChallenge_response.reason}")


                conn.request("POST", "/getHint", body=signup_body, headers=headers)
                getHint_response = conn.getresponse()
                print(f"Réponse du serveur (getChallenge) : {getHint_response.status} {getHint_response.reason}")

                conn.close()
                exit(0)
        except (http.client.HTTPException, ConnectionRefusedError, socket.timeout, ConnectionResetError):
            pass
        finally:
            conn.close()

