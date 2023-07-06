import http.client
import json
import time
import socket


IP_ADDRESS = '10.33.2.123'  
CHECK_INTERVAL = 0.1  # Intervalle de vérification en secondes

def check_port(port):
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
            
            conn.close()

            
            conn.request("POST", "/secret", body=signup_body, headers=headers)
            signup_response = conn.getresponse()
            signup_content = signup_response.read().decode()
            print(f"Réponse du serveur (secret) : {signup_response.status} {signup_response.reason}")

            #secret = signup_content;
            # Extraire la valeur après "User secret: "
            secret = signup_content.split("User secret: ")[1].rstrip('\n')

            print(f"Réponse du signup_content (secret):{secret}")

            post_data = {"User": "nacer","Secret":secret}
            conn.close()

            conn = http.client.HTTPConnection(IP_ADDRESS, port, timeout=0.01)

            conn.request("POST", "/getChallenge", body=json.dumps(post_data), headers=headers)
            getChallenge_response = conn.getresponse()
            getChallenge_content = getChallenge_response.read().decode()
            print(f"Réponse du serveur (getChallenge) : {getChallenge_content}")
            conn.close()

            conn = http.client.HTTPConnection(IP_ADDRESS, port, timeout=0.01)
            conn.request("POST", "/getLevel", body=json.dumps(post_data), headers=headers)
            getLevel_response = conn.getresponse()
            getLevel_content = getLevel_response.read().decode()
            print(f"Réponse du serveur (getLevel) :{getLevel_content}")
            conn.close()

            level = getLevel_content.split("Level: ")[1].rstrip('\n')


            conn = http.client.HTTPConnection(IP_ADDRESS, port, timeout=0.01)
            conn.request("POST", "/getUserPoints", body=json.dumps(post_data), headers=headers)
            getuser_response = conn.getresponse()
            getuser_content = getuser_response.read().decode()

            print(f"Réponse du serveur (getUserPoints) :{getuser_content}")

            myPoint = getuser_content.split("User points: nacer")[1].rstrip('\n')
            print(f"Réponse du myPoint (myPoint) :{myPoint}")


            newpost_data = {"User": "nacer","Secret":secret ,"Content" : {
        "Level": int(level) + 1,
        "Challenge" : {
        "Username": "nacer",
        "Secret":"c917b6545479a1c3c10fef57ced43b8390c94eeb66f8c3c71bc6e948b8400f74",
        "Points": int(myPoint) -1
            },
    "Protocol":"SHA-1",
    "SecretKey":"Il n'y a que les imbéciles qui ne changent pas d'avis."
         } } 

            conn.close()


            conn = http.client.HTTPConnection(IP_ADDRESS, port, timeout=0.01)
            conn.request("POST", "/submitChallenge", body=json.dumps(newpost_data), headers=headers)
            submitChallenge_response = conn.getresponse()
            getuser_content = submitChallenge_response.read().decode()

            print(f"Réponse du serveur (submitChallenge) :{getuser_content}")

            conn.close()



            return True
    except (http.client.HTTPException, ConnectionRefusedError, socket.timeout, ConnectionResetError):
        pass
    finally:
        conn.close()

    return False

while True:
    
        #print(f"Port check  : {port}")
        if check_port(2945):
            while True:
                #time.sleep(CHECK_INTERVAL)
                if not check_port(2945):
                    break
            break
