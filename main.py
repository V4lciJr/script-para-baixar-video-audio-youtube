import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import threading
import requests


class YouTubeDownloader:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("JValci YT Downloader")

        #entrada da URL
        tk.Label(self.janela, text='URL do vídeo').grid(row=0, column=0)
        self.url_entry = tk.Entry(self.janela, width=50)
        self.url_entry.grid(row=0, column=1)

        #download de video ou audio
        tk.Label(self.janela, text='Tipo de download: ').grid(row=1, column=0)
        self.tipo_download = tk.StringVar()
        self.tipo_download.set('vídeo')
        tk.OptionMenu(self.janela, self.tipo_download, 'vídeo', 'áudio').grid(row=1, column=1)

        #verificar a URL
        tk.Button(self.janela, text='Verificar URL', command=self.verificar_url).grid(row=2, column=0)

        #baixar video
        tk.Button(self.janela, text='Baixar', command=self.baixar_video).grid(row=2, column=1, columnspan=2)

        #barra de progresso
        self.progress_bar = ttk.Progressbar(self.janela, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=2)

        #status
        self.status_label = tk.Label(self.janela, text='')
        self.status_label.grid(row=7, column=0, columnspan=2)

        self.baixando = False

    def checa_url(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror('Erro!!!', 'Informe a URL do vídeo')
            return
        return url

    def verificar_url(self):

        url = self.checa_url()

        try:
            requests.head(url)
            self.status_label.config(text='URL válida!!')
        except requests.ConnectionError:
            self.status_label.config(text='URL inválida!!!')

    def baixar_video(self):
        url = self.checa_url()

        self.baixando = True
        # cria uma thread para baixar o video em segundo plano
        thread = threading.Thread(target=self.baixar_video_segundo_plano, args=(url,))
        thread.start()

    def baixar_video_segundo_plano(self, url):
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'bestaudio' if self.tipo_download.get() == 'áudio' else 'best',
                'progress_hooks': [self.atualizar_progresso]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text='Download do áudio feito com sucesso!')
            self.baixando = False
            self.perguntar_baixar_novamente()
        except Exception as e:
            self.status_label.config(text=f'Erro ao efetuar o download do vídeo/áudio: {str(e)}')
            self.baixando = False

    def atualizar_progresso(self, valor):
        if valor['status'] == 'downloading':
            #porcentagem = int(valor['percentage'])
            #self.progress_bar['value'] = porcentagem
            self.status_label.config(text=f'Baixando... {valor["downloaded_bytes"]} de {valor["total_bytes"]}')
            self.janela.update_idletasks()

    def perguntar_baixar_novamente(self):

        if not self.baixando:
            resp = messagebox.askyesno('Downloader', 'Deseja baixar outro vídeo ou áudio?')
            if resp:
                self.url_entry.delete(0, tk.END)
                self.progress_bar['value'] = 0
                self.status_label.config(text='')
            else:
                self.janela.destroy()

    def run(self):
        self.janela.mainloop()


if __name__ == '__main__':
    app = YouTubeDownloader()
    app.run()