
from copy import copy
from itertools import product

CHORDS = {
  '': [0, 4, 7],
  'm': [0, 3, 7],
  '7': [0, 4, 7, 10],
  'M7': [0, 4, 7, 11],
  'm7': [0, 3, 7, 10],
  'mM7': [0, 3, 7, 11],
  '6': [0, 4, 7, 9],
  'm6': [0, 3, 7, 9],
  '9': [0, 4, 7, 10, 14],
  'M9': [0, 4, 7, 11, 14],
  'm9': [0, 3, 7, 10, 14],
  '69': [0, 4, 7, 9, 14],
  'm69': [0, 3, 7, 9, 14],
  'sus4': [0, 5, 7],
  '7sus4': [0, 5, 7, 10],
  'dim': [0, 3, 6],
  'aug': [0, 4, 8],
  'aug7': [0, 4, 8, 10],
  'add9': [0, 4, 7, 14],
  '7+5': [0, 4, 8, 10],
  '7-5': [0, 4, 6, 10],
  'm7-5': [0, 3, 6, 10],
  '7+9': [0, 4, 7, 10, 15],
  '7-9': [0, 4, 7, 10, 13],
}

ALIASES = {
  '7+5': ['7(#5)', '7(♯5)'],
  '7-5': ['7(b5)', '7(♭5)'],
  'm7-5': ['m7(b5)', 'm7(♭5)'],
  '7+9': ['7(#9)', '7(♯9)'],
  '7-9': ['7(b9)', '7(♭9)'],
}

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


class Code():
  def __init__(self, chord: (list[int] | str)):
    if isinstance(chord, str):
      self.chord = CHORDS[get_alias(chord)]
    else:
      self.chord = chord
    self.current = 0
    self.max = len(self.chord) if max(self.chord) < 12 else 1

  def __contains__(self, value: (int | str)):
    value = get_key(value) % 12
    return value in [c%12 for c in self.chord]

  def __lshift__(self, value: int):
    return self.__class__([c-value for c in self.chord])
  
  def __rshift__(self, value: int):
    return self.__class__([c+value for c in self.chord])

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.current >= self.max:
      self.current = 0
      raise StopIteration()
    
    chord = copy(self.chord)
    for i in range(self.current):
      chord[i] += 12
    self.current += 1
    return self.__class__(chord)
  
  def normalize(self):
    shift = 0xffffffff
    for c in self.chord:
      shift = min(c // 12, shift)
    for i, c in enumerate(self.chord):
      self.chord[i] = c - shift * 12
      if (self.chord[i] // 12) > 1:
        self.chord[i] -= 12
    self.chord.sort()
    return self
  
  def __str__(self):
    return get_name(self)

def get_name(value : (Code | int)):
  if isinstance(value, Code):
    return ', '.join(get_name(c) for c in sorted(value.chord))
  else:
    shift = value // 12
    oct = f'+{shift}' if shift > 0 else ''
    return NAMES[value % 12] + oct

def get_key(value: (int | str)):
  if isinstance(value, str):
    return NAMES.index(value)
  return value

def get_key_and_name(s: str):
  if len(s) == 1:
    return s, ''
  elif s[1] == '#':
    return s[:2], s[2:]
  else:
    return s[0], s[1:]

def normalize_key(key: str):
  if len(key) < 2:
    return key
  if key[1] in ['♭', 'b']:
    k = get_key(key[0]) - 2
    return f'{get_name(k)}#{key[2:]}'
  return key

def get_alias(key: str):
  if key in CHORDS:
    return key
  for alias, candidates in ALIASES.items():
    if key in candidates:
      return alias
  raise KeyError

def get_all_chord(key: (int | str), name: str):
  for chord in Code(name):
    yield (chord >> get_key(key)).normalize()

def all_chords():
  for key, name in product(NAMES, CHORDS.keys()):
    for chord in get_all_chord(key, name):
      yield key, name, chord
