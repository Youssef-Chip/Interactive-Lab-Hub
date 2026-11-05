import time
import random
import paho.mqtt.client as mqtt

BROKER = "farlab.infosci.cornell.edu"
PORT = 1883
USER = "idd"
PASSWORD = "device@theFarm"

COMMAND_TOPIC = f"IDD/simon_says_team/simon/command"
EVENT_TOPIC_WILDCARD = f"IDD/simon_says_team/simon/+/event"

current_event = None
event_source = None


def on_message(client, userdata, msg):
    global current_event, event_source
    # Only capture the first person to trigger their sensor
    if current_event is None:
        parts = msg.topic.split('/')
        event_source = parts[3]
        current_event = msg.payload.decode()


client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(EVENT_TOPIC_WILDCARD)
client.loop_start()

scores = {"pi1": 0, "pi2": 0}
actions = ["red", "green", "close", "blue"]

print(f"Starting HEAD-TO-HEAD Race...")
time.sleep(2)

try:
    while True:
        target_action = random.choice(actions)
        is_simon = random.choice([True, False])  # 50% chance of a fake-out

        # Generate the correct prompt
        if is_simon:
            command_text = f"SIMON SAYS: FIRST TO SHOW [{target_action.upper()}] WINS!"
        else:
            command_text = f"FIRST TO SHOW [{target_action.upper()}] WINS!"

        print("\n" + "="*50)
        print(f"SCORES -> P1: {scores['pi1']} | P2: {scores['pi2']}")
        print("\n*** READ THIS OUT LOUD ***")
        print(f"-> {command_text}")

        # Broadcast the text to the players' screens
        client.publish(COMMAND_TOPIC, f"display:{command_text}")

        # Clear any accidental early triggers
        current_event = None
        event_source = None

        print("Listening for sensors... (5 seconds to react!)")

        # 5-SECOND TIMEOUT LOOP
        start_time = time.time()
        while current_event is None and time.time() - start_time < 5.0:
            time.sleep(0.05)

        # Evaluation Logic
        if is_simon:
            if current_event == target_action:
                scores[event_source] += 1
                result_msg = f"BOOM! {event_source.upper()} got it right first! +1 point."
            elif current_event is not None:
                scores[event_source] -= 1
                result_msg = f"OOPS! {event_source.upper()} showed {current_event.upper()}! -1 point."
            else:
                result_msg = "TOO SLOW! Time expired. No points."
        else:  # The Fake-Out
            if current_event is not None:
                scores[event_source] -= 1
                result_msg = f"CAUGHT YOU! {event_source.upper()} moved when Simon didn't say! -1 point."
            else:
                result_msg = "Phew! Both held still. Good job."

        print(result_msg)

        # Broadcast the result and score to the players' screens
        client.publish(
            COMMAND_TOPIC, f"result:{result_msg} (P1:{scores['pi1']} P2:{scores['pi2']})")

        # Give them 3.5 seconds to lower their colored objects before the next round starts
        time.sleep(3.5)

        # Check Win Condition
        WINNING_SCORE = 5
        if scores["pi1"] >= WINNING_SCORE or scores["pi2"] >= WINNING_SCORE:
            if scores["pi1"] > scores["pi2"]:
                winner = "PLAYER 1"
            elif scores["pi2"] > scores["pi1"]:
                winner = "PLAYER 2"
            else:
                winner = "TIE"

            game_over_text = f"GAME OVER! {winner} WINS THE MATCH!"
            print("\n" + "#"*50)
            print(game_over_text)
            print("#"*50 + "\n")

            client.publish(COMMAND_TOPIC, f"display:{game_over_text}")
            time.sleep(5)
            break

except KeyboardInterrupt:
    print("\nQuitting game server.")
    client.loop_stop()
    client.disconnect()
