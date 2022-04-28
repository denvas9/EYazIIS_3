from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox

import matplotlib.pyplot as plt

from wordcloud import WordCloud
import docx
from help import help_text
import multiprocessing
import time
from wiki_ru_wordnet import WikiWordnet


def open_file():
    file_name = fd.askopenfilename(filetypes=(("docx files", "*.docx"),))
    if file_name != '':
        doc = docx.Document(file_name)
        
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        inp_text='\n'.join(text)

        print(inp_text)
        calculated_text.insert(END, inp_text)

def show_information():
    children = Toplevel()
    children.title('Help')
    children.geometry("600x300+500+350")
    output_help_text = Text(children, height=20, width=80)
    scroll_b = Scrollbar(children, command=output_help_text.yview)
    scroll_b.grid(row=4, column=8, sticky='nsew')
    output_help_text.grid(row=4, column=0, sticky='nsew', columnspan=3)
    output_help_text.configure(yscrollcommand=scroll_b.set)
    output_help_text.insert(END, help_text)
    output_help_text.configure(state='disabled')


def letters_in_the_word(word):
    for i in word:
        if i == ' ':
            return False
    return True


def semantic_analysis():
    text = calculated_text.get(1.0,END)
    temp_symbs = ['\t','\n','.',',','!','?',':',';','(',')']
    for i in temp_symbs:
        text = text.replace(i, '')
    text = text.lower()
    if text == '':
        return None
        
    start = time.time()
    if letters_in_the_word(text):

        a = multiprocessing.Process(target=semantic_analysis_syno,args=(text,))
        b = multiprocessing.Process(target=semantic_analysis_hypo,args=(text,))
        c = multiprocessing.Process(target=semantic_analysis_hyper,args=(text,))

        a.start()
        b.start()
        c.start()
            
        a.join()
        b.join()
        c.join()

    else:
        messagebox.showwarning('Warning!!!', 'One word!', type='ok')
        
    end = time.time()
    print("Total time: {:.1f}".format(end - start))


def semantic_analysis_syno(text):
    wikiwordnet = WikiWordnet()
    # Кольцо синонимов или синсет - это группа элементов данных, которые считаются семантически эквивалентными
    # для целей поиска информации
    synsets = wikiwordnet.get_synsets(text)
    text = ''
    lemmas = [x.lemma() for x in synsets[0].get_words()]

    # Synset представляет группу лемм, имеющих одинаковый смысл, а лемма представляет собой отдельную словоформу.
    for lemma in lemmas:
        text += lemma + ' '

    word_cloud(text,"Синонимы")
    #print("job is done")

def semantic_analysis_hypo(text):
    wikiwordnet = WikiWordnet()
    # Кольцо синонимов или синсет - это группа элементов данных, которые считаются семантически эквивалентными
    # для целей поиска информации
    synsets = wikiwordnet.get_synsets(text)
    text = ''

    synset = synsets[0]

    for hyponym in wikiwordnet.get_hyponyms(synset):
        for w in hyponym.get_words():
            text += w.lemma() + ' '
            
    word_cloud(text,"Гипонимы")
    #print("job is done")

def semantic_analysis_hyper(text):
    wikiwordnet = WikiWordnet()
    # Кольцо синонимов или синсет - это группа элементов данных, которые считаются семантически эквивалентными
    # для целей поиска информации
    synsets = wikiwordnet.get_synsets(text)
    text = ''

    synset = synsets[0]

    for hypernym in wikiwordnet.get_hypernyms(synset):
        for w in  hypernym.get_words():
            text += w.lemma() + ' '
    word_cloud(text,"Гиперонимы")
    #print("job is done")


def word_cloud(text,title):
    cloud = WordCloud(relative_scaling=1.0, ).generate(text)
    fig = plt.figure() 
    fig.canvas.manager.set_window_title(title) 
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    root = Tk()
    root.title("Семантический анализ")

  #  root.resizable(width=False, height=False)
  #  root.geometry("620x150+800+350")

    label = Label(root, text='Анализируемое слово', font=("Times new Roman", 13, "bold"))
    label.grid(row=0, column=0)

    calculated_text = Text(root, height=5, width=50)
    calculated_text.grid(row=1, column=0, sticky='nsew', columnspan=2)

    help_button = Button(text="Помощь", width=10, command=show_information)
    help_button.grid(row=0, column=3)

    open_button = Button(text="Считать из файла", width=15, command=open_file)
    open_button.grid(row=1, column=3)

    ok_button = Button(text="Анализировать", width=15, command=semantic_analysis)
    ok_button.grid(row=2, column=3)
    root.mainloop()