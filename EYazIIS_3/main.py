from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox

import matplotlib.pyplot as plt

from wordcloud import WordCloud

from help import help_text
import time
from wiki_ru_wordnet import WikiWordnet

import nltk

def open_file():
    file_name = fd.askopenfilename(filetypes=(("TXT files", "*.txt"),))
    if file_name != '':
        file = open(file_name, 'r', encoding="utf-8")
        data = file.readlines()
        calculated_text.insert(1.0, data)


def show_information():
    children = Toplevel()
    children.title('Help')
    children.geometry("600x300+500+350")
    output_help_text = Text(children, height=20, width=80)
    scroll_b = Scrollbar(children, command=output_help_text.yview)
    scroll_b.grid(row=4, column=8, sticky='nsew')
    output_help_text.grid(row=4, column=0, sticky='nsew', columnspan=3)
    output_help_text.configure(yscrollcommand=scroll_b.set)
    output_help_text.insert('end', help_text)
    output_help_text.configure(state='disabled')


def letters_in_the_word(word):
    for i in list(word):
        if i == ' ':
            return False
    return True


def semantic_analysis():
    wikiwordnet = WikiWordnet()
    text = calculated_text.get(1.0, END).lower()
    text = text.replace('\n', '')
    if text == '':
        return None
    start = time.time()
    if letters_in_the_word(text):
        hyponyms = []
        # Кольцо синонимов или синсет - это группа элементов данных, которые считаются семантически эквивалентными
        # для целей поиска информации
        synsets2 = wikiwordnet.get_synsets(text)
        text = ''
        lemmas2 = [x.lemma() for x in synsets2[0].get_words()]

        # Synset представляет группу лемм, имеющих одинаковый смысл, а лемма представляет собой отдельную словоформу.
        for lemma in lemmas2:
            text += lemma + ' '

        synset2 = synsets2[0]
        for hypernym in wikiwordnet.get_hypernyms(synset2):
            for w in  hypernym.get_words():
                text += w.lemma() + ' '

        for hyponym in wikiwordnet.get_hyponyms(synset2):
            for w in hyponym.get_words():
                text += w.lemma() + ' '

        word_cloud(text)
        end = time.time()
        print("Total time: {:.1f}".format(end - start))
    else:
        messagebox.showwarning('Warning!!!', 'One word!', type='ok')


def word_cloud(text):
    # Облако тегов — это визуальное представление списка
    cloud = WordCloud(relative_scaling=1.0, ).generate(text)
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()


root = Tk()
root.title("Semantic text analysis")

root.resizable(width=False, height=False)
root.geometry("620x150+500+250")

label = Label(root, text='Input word:', font=("Times new Roman", 13, "bold"))
label.grid(row=0, column=0)

calculated_text = Text(root, height=5, width=50)
calculated_text.grid(row=1, column=1, sticky='nsew', columnspan=2)

help_button = Button(text="Help", width=10, command=show_information)
help_button.grid(row=0, column=3)

open_button = Button(text="Open file", width=10, command=open_file)
open_button.grid(row=1, column=3)

ok_button = Button(text="Semantic analysis", width=14, command=semantic_analysis)
ok_button.grid(row=2, column=3)
root.mainloop()