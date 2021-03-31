import sys
from mido import MidiFile
from pynput.keyboard import Key, Controller

def get_correct_note(num):
    octava = (num-1) // 12
    note = num % 12
    note_tmp = note
    if note >= 2:
        note_tmp -= 1
    if note >= 4:
        note_tmp -= 1
    if note >= 7:
        note_tmp -= 1
    if note >= 9:
        note_tmp -= 1
    if note >= 11:
        note_tmp -= 1
    out_note = octava * 7 + note_tmp
    return out_note


KEYBOARD_MAP = ["z", "x", "c", "v", "b", "n", "m",
                "a", "s", "d", "f", "g", "h", "j",
                "q", "w", "e", "r", "t", "y", "u"]
CHANNEL = 0
if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} file.mid")
    exit(1)
mid = MidiFile(sys.argv[1])
min_note = 200
channels = []
for msg in mid:
    if msg.type == "note_on":
        if msg.channel not in channels:
            channels.append(msg.channel)
        if msg.channel == CHANNEL:
            note = get_correct_note(msg.note)
            if note < min_note:
                min_note = note
channels.sort()
print(channels)
min_note = min_note // 7 * 7  # Переходит на начало октавы
keyboard = Controller()
for msg in mid.play():
    if msg.type == "note_on" and msg.channel == CHANNEL:
        note = get_correct_note(msg.note)
        game_note = note - min_note
        if len(KEYBOARD_MAP) <= game_note:
            print("key not found")
            continue
        key = KEYBOARD_MAP[game_note]
        print(f"key - {key}")
        keyboard.press(key)
        keyboard.release(key)