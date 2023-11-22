import argparse
import random
import time
from collections import defaultdict

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES += NOTES

STRINGS = {'E' : NOTES[4:17],
           'A' : NOTES[9:22],
           'D' : NOTES[2:15],
           'G' : NOTES[7:20],
           'B' : NOTES[11:]
           }

random.seed(time.time())

def get_query(strings):
    string = random.choice(strings)[0]
    notes = STRINGS[string]
    fret = random.randint(0, len(notes) - 1)
    note = notes[fret]
    return string, fret, note

class Score:
    def __init__(self):
        self.hit = 0
        self.miss = 0

    def correct(self):
        self.hit += 1

    def wrong(self):
        self.miss += 1

    def total(self):
        return self.hit + self.miss

    def auto_score(self, v):
        if v: self.correct()
        else: self.wrong()


def print_scores(scores, strings):
    print(f'strings: {strings}')
    total = 0
    hits = 0
    for s in ['E','A','D','G','B']:
        if s not in strings:
            continue
        for f in range(13):
            k = f'{s}-{f}'
            #print(f'key: {k}')
            s = scores.get(k, None)
            if not s or not s.total():
                #print(f'skipping: {k}')
                continue
            total += s.total()
            hits += s.hit
            print(f'{k}: {s.hit}/{s.total()}')
    if total:
        accuracy = hits*100.0/total
        print(f'Overall accuracy: {accuracy:.2f}%')
    else:
        print(f'No scores')

def main(strings):
    scores = defaultdict(Score)

    print("starting game, good luck")
    while True:
        s, f, note =  get_query(strings)
        question = f'{s}-{f}'
        ans = input(f'{question}?\n> ')
        ans = ans.upper()
        print(ans)
        for c in "',.":
            ans = ans.replace(c, "#")
        if ans == 'Q':
            break
        correct = ans == note
        scores[question].auto_score(correct)
        if correct: print('Correct!')
        else: print(f'Incorrect! {note}')


    print_scores(scores, strings)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--string', '-s', dest='strings', choices=['E','A','D','G','B','e'], action='append')

    args = parser.parse_args()
    if not args.strings: args.strings=['E']
    main(args.strings)
