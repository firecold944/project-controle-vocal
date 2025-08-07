import speech_recognition as sr
import pyautogui
import subprocess
import time
import webbrowser
import pyperclip
import os
import customtkinter as ctk
import threading

# Configuration de l'apparence de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ApplicationCommandeVocale:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface de Commande Vocale(ethan project)")
        self.root.geometry("500x400")
        
        self.recognizer = sr.Recognizer()
        self.last_action = None
        self.is_listening = False
        self.listening_thread = None
        
        # Éléments de l'interface
        self.label_status = ctk.CTkLabel(
            master=self.root,
            text="État : Arrêté",
            font=("Arial", 16)
        )
        self.label_status.pack(pady=20)
        
        self.label_command = ctk.CTkLabel(
            master=self.root,
            text="Dernière commande : Aucune",
            font=("Arial", 14),
            wraplength=450
        )
        self.label_command.pack(pady=20)
        
        self.button_toggle = ctk.CTkButton(
            master=self.root,
            text="Démarrer l'écoute",
            command=self.toggle_listening
        )
        self.button_toggle.pack(pady=20)
        
        self.button_quit = ctk.CTkButton(
            master=self.root,
            text="Quitter",
            command=self.quit_app,
            fg_color="red",
            hover_color="darkred"
        )
        self.button_quit.pack(pady=20)
        
        # Configuration de pyautogui
        pyautogui.FAILSAFE = True
    
    def executer_commande(self, commande):
        commande_lower = commande.lower()
        self.label_command.configure(text=f"Dernière commande : {commande}")
        
        if "ouvre chrome" in commande_lower and self.last_action != "ouvre_chrome":
            subprocess.Popen("start chrome", shell=True)
            self.last_action = "ouvre_chrome"
        elif "éteins l'ordinateur" in commande_lower and self.last_action != "eteindre_ordinateur":
            subprocess.call("shutdown /s /t 1", shell=True)
            self.last_action = "eteindre_ordinateur"
        elif "redémarrer" in commande_lower and self.last_action != "redemarrer":
            subprocess.call("shutdown /r /t 1", shell=True)
            self.last_action = "redemarrer"
        elif "ouvre notepad" in commande_lower and self.last_action != "ouvre_notepad":
            subprocess.Popen("notepad", shell=True)
            self.last_action = "ouvre_notepad"
        elif "ouvre youtube" in commande_lower and self.last_action != "ouvre_youtube":
            webbrowser.open("https://www.youtube.com")
            self.last_action = "ouvre_youtube"
        elif "écris" in commande_lower and self.last_action != "ecrire_texte":
            texte = commande_lower.replace("écris", "").strip()
            pyperclip.copy(texte)
            pyautogui.hotkey("ctrl", "v")
            self.last_action = "ecrire_texte"
        elif "volume plus" in commande_lower and self.last_action != "volume_plus":
            pyautogui.press("volumeup")
            self.last_action = "volume_plus"
        elif "volume moins" in commande_lower and self.last_action != "volume_moins":
            pyautogui.press("volumedown")
            self.last_action = "volume_moins"
        elif "cherche" in commande_lower and self.last_action != "cherche_edge":
            recherche=commande_lower.replace("cherche","").strip()
            url=f"https://www.bing.com/search?q={recherche}"
            webbrowser.open(url)
            self.last_action="cherche_edge"
        
        elif "arrête" in commande_lower:
            return False
        else:
            self.last_action = None
        return True
    
    def ecouter_et_reconnaitre(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                commande = self.recognizer.recognize_google(audio, language="fr-FR")
                return commande
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
    
    def listen_loop(self):
        while self.is_listening:
            commande = self.ecouter_et_reconnaitre()
            if commande:
                if not self.executer_commande(commande):
                    self.stop_listening()
                    break
            time.sleep(0.1)
    
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.label_status.configure(text="État : En écoute...")
            self.button_toggle.configure(text="Arrêter l'écoute")
            self.listening_thread = threading.Thread(target=self.listen_loop)
            self.listening_thread.daemon = True
            self.listening_thread.start()
        else:
            self.stop_listening()
    
    def stop_listening(self):
        self.is_listening = False
        self.label_status.configure(text="État : Arrêté")
        self.button_toggle.configure(text="Démarrer l'écoute")
    
    def quit_app(self):
        self.stop_listening()
        self.root.quit()
        os._exit(0)

if __name__ == "__main__":
    root = ctk.CTk()
    root.iconbitmap("vocal_93739.ico")
    

    app = ApplicationCommandeVocale(root)
    root.mainloop()
    
