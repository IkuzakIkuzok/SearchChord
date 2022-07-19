
# cspell:disable-next-line
import chordutil as cu
import re
import tkinter
import tkinter.ttk as ttk

def search_chord(words: list[str], option: int, results: ttk.Treeview):
  if option == 0:
    for word in words:
      try:
          for chord in cu.get_all_chord(*cu.get_key_and_name(word)):
            results.insert(parent='', index='end', values=(word, chord))
      except KeyError:
        print(f'Unknown chord name: {word}')
  else:
    predicate = [
      lambda chord: all(map(lambda c: c in chord, words)),
      lambda chord: cu.get_name(chord.chord[0]) in words,
      lambda chord: cu.get_name(chord.chord[-1]%12) in words,
    ][option-1]
    for key, name, chord in cu.all_chords():
      try:
        if predicate(chord):
          results.insert(parent='', index='end', values=(f'{key}{name}', chord))
      except ValueError:
        pass

def main():
  root = tkinter.Tk()
  root.title('コード検索')
  root.geometry('350x400')

  search_box = tkinter.Entry(root, width=35)
  search_box.place(x=20, y=20)

  search_option = ttk.Combobox(
    root,
    values=['コード名', '音を含む', '最も低い音', '最も高い音'],
    width=10,
    state='readonly',
  )
  search_option.current(0)
  search_option.place(x=250, y=20)

  results = ttk.Treeview(
    root,
    columns=['name', 'chord'],
    height=15
  )
  results.heading('name', text='コード名')
  results.heading('chord', text='コード')

  results.column('#0', width=0, stretch=False)
  results.column('name', width=100)
  results.column('chord', width=210)
  results.place(x=20, y=50)

  def search(_):
    word = search_box.get().replace('♯', '#')
    if len(word) == 0: return
    words = list(map(cu.normalize_key, re.split(r'\s+', word)))
    option = search_option.current()
    if len(words) == 0: return
    results.delete(*results.get_children())
    search_chord(words, option, results)

  search_box.bind('<FocusOut>', search)
  search_box.bind('<Return>', search)
  search_option.bind('<<ComboboxSelected>>', search)

  root.mainloop()

if __name__ == '__main__':
  main()
