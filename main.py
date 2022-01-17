#import libraries
#tkinter(documentation -> https://docs.python.org/3/library/tkinter.html)
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from functools import partial
#googletrans(documentation -> https://py-googletrans.readthedocs.io/en/latest/)
import googletrans
from googletrans import Translator


#all the languages available
languages = googletrans.LANGUAGES #dictionary of all languages
languages_list = list(languages.values()) #a list of the values of the languages dictionary

#find the key from the value in the languages dict
def get_lan(val):
    for key, value in languages.items():
         if val == value:
             return key
#translate function
def translate(txt, in_lan, out_lan, output_place):
	#obtains the languages that the user selected (entry widget)
	in_l = in_lan.get()
	out_l = out_lan.get()
	#finds the key of that value in the languages dict
	input_lan = get_lan(in_l)
	output_lan = get_lan(out_l)
	#obtains the info from the text widget
	text = txt.get('1.0', 'end')
	#creates the translator
	translator = Translator(service_urls=['translate.google.com',
		'translate.google.co.kr'
		])
	#detects the language in which the text is written
	try:
		detect_lan = translator.detect(text)
		real_lan = detect_lan.lang 
	except:
		pass
	#if the languages are congruent, translate the text normally
	if input_lan == real_lan:
		try:
			#translate the text from input language to output language
			translate = translator.translate(text, src=input_lan, dest=output_lan)
			#gets the result of the translation
			translated_text = str(translate.text) 
			#deletes the text that was there before
			output_place.delete('1.0', 'end')
			#inserts the translated text in the text widget
			output_place.insert('insert', translated_text)
		#if there is an error on the translation, just output the input text
		except:
			#deletes the text that was there before
			output_place.delete('1.0', 'end')
			#inserts the same text without changes
			output_place.insert('insert', text)
	#if the languages are not congruent, then, suggest to the user to translate the text from the real language
	if input_lan != real_lan:
		#deletes the text that was there before
		output_place.delete('1.0', 'end')
		#inserts the same text without changes
		output_place.insert('insert', text)
		def translate_from_real(real_language):	#translate from the real language 
			try:
				translate = translator.translate(text, src=real_language, dest=output_lan)#translate the text from the real language
				translated_text = str(translate.text) 
				output_place.delete('1.0', 'end')
				output_place.insert('insert', translated_text)#insert the translated text
				#changes the input language to the real language
				input_lan_txt.delete(0, 'end')#delete the text (language) that was there before
				input_lan_txt.insert('insert', f'{languages[real_language]}')
				real_trans_button.destroy()
			except:
				output_place.delete('1.0', 'end')
				output_place.insert('insert', text)
		#suggest the user to translate from the real language
		real_trans_button = ttk.Button(text=f'Translate from {languages[real_lan]}', command=partial(translate_from_real, real_lan))
		real_trans_button.place(x=80, y=425)
			
#select language window
def select_language_window(lan):
	
	#select the language function
	def select_lan(_list, lan):
		try:
			selection = _list.get(_list.curselection())#gets the selection
			#detect which language is being changed
			if lan == 'input':#either input language
				input_lan_txt.delete(0, 'end')#delete the text (language) that was there before
				input_lan_txt.insert('end', f'{selection}')#inserts the language that the user selected
			elif lan == 'output': #or output language
				output_lan_txt.delete(0, 'end')
				output_lan_txt.insert('end', f'{selection}')
		except:
			pass

		select_lan_win.destroy() #destroy the window after selecting the language

	#create the select language window
	select_lan_win = tk.Toplevel(trans_window)
	select_lan_win.config(width=300, height=300)
	select_lan_win.resizable(0,0) #blocks the possibility to the user of changing the size of the window
	select_lan_win.title('Select Language')
	#creates a list widget 
	languages_available = tk.Listbox(select_lan_win)
	#inserts the values from languages list into the list box
	languages_available.insert(0, *languages_list)
	languages_available.place(x=5, y=5, width=220, height=220)
	#select language button
	select = ttk.Button(select_lan_win, text='Select Language', command=partial(select_lan, languages_available, lan))
	select.place(x=10, y=250)



#main window
trans_window = tk.Tk()
trans_window.config(width=800, height=500)
trans_window.resizable(0,0) #blocks the possibility to the user of changing the size of the window
trans_window.title('Translator')

#text fonts
font_1 = tkFont.Font(family='Helvetica', size=18)


#title
title = ttk.Label(trans_window, text='Translator', font=font_1).place(x=5, y=10)
#input language entry
input_lan_txt = ttk.Entry(trans_window)
input_lan_txt.place(x=100, y=90)
input_lan_txt.insert('end', 'english')
#output language entry
output_lan_txt = ttk.Entry(trans_window)
output_lan_txt.place(x=500, y=90)
output_lan_txt.insert('end', 'spanish')
#text entry
text_entry = tk.Text(trans_window)
text_entry.place(x=40, y=120, width=300, height=300)
#text ouput
text_output = tk.Text(trans_window)
text_output.place(x=450, y=120, width=300, height=300)
#select language buttons
#change the input lanugage
select_input_lan = ttk.Button(text='>', command=partial(select_language_window, 'input'))
select_input_lan.place(x=265, y=90)
#change the output language
select_output_lan = ttk.Button(text='>', command=partial(select_language_window, 'output'))
select_output_lan.place(x=675, y=90)
#translate button
translate_button = ttk.Button(text='Translate', command=partial(translate, text_entry, input_lan_txt, output_lan_txt, text_output))
translate_button.place(x=260, y=425)


trans_window.mainloop()
#Code made by Thadeuks
