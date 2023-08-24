import customtkinter
from mvc.controller import BotController

class Bot(customtkinter.CTk):
    """Cria a classe Bot herdando da super classe customtkinter.CTk"""
    font_size = 15
    altura_entrys = 40
    position_x = 15

    def __init__(self):
        super().__init__()
        self.controller = BotController(self)
        self.principal = customtkinter.CTkFrame(self)
        self.principal.pack(fill = customtkinter.BOTH, expand=True)
        self.geometry('400x525')
        self.resizable(False, False)
        self.configure()
        self.main_color = customtkinter.StringVar(value=self.controller.config['theme'])
        self.title('LinkedInAutoConnectBot')
        customtkinter.set_appearance_mode(self.main_color.get())
        self.email_lab = customtkinter.CTkLabel(self.principal, text='Email:', font=('Arial', self.font_size))
        self.email_lab.place(x=self.position_x, y=40, h=21)

        self.password_lab = customtkinter.CTkLabel(self.principal, text='Password:', font=('Arial', self.font_size))
        self.password_lab.place(x=self.position_x, y=110, h=21)

        self.prof_lab = customtkinter.CTkLabel(self.principal, text='Profession to Search:', font=('Arial', self.font_size))
        self.prof_lab.place(x=self.position_x, y=145)

        self.message_lab = customtkinter.CTkLabel(self.principal, text='Custom Message to send: ', font=('Arial', self.font_size))
        self.message_lab.place(x=self.position_x, y=220, h=21)

        self.connect_lab = customtkinter.CTkLabel(self.principal, text='Number of Connections: ', font=('Arial', self.font_size))
        self.connect_lab.place(x=self.position_x, y=420, h=21)


        self.email = customtkinter.CTkEntry(self.principal, font=('Arial', self.font_size), placeholder_text='Seu E-mail')
        self.email.place(x=self.position_x, y=60, h=self.altura_entrys, w=460)

        self.password = customtkinter.CTkEntry(self.principal, font=('Arial', self.font_size), show='*', placeholder_text='Sua Senha')
        self.password.place(x=90, y=102, h=self.altura_entrys, w=366)

        self.profession = customtkinter.CTkEntry(self.principal, font=('Arial', self.font_size))
        self.profession.place(x=self.position_x, y=177, h=self.altura_entrys, w=460)


        self.message = customtkinter.CTkTextbox(self.principal, font=('Arial', self.font_size))
        self.message.place(x=self.position_x, y=245, h=200, w=460)


        self.start = customtkinter.CTkButton(self.principal, text='START', font=('Arial', self.font_size),
                                             command=lambda: self.controller.check_elements(self.email.get(),
                                                                                            self.password.get(),
                                                                                            self.profession.get(),
                                                                                            self.message.get("0.0", "end"),
                                                                                            self.optionmenu.get()))
        self.start.place(x=self.position_x, y=470, w=100)

        self.stop = customtkinter.CTkButton(self.principal, text='STOP', font=('Arial', self.font_size), fg_color="red",
                              hover_color="darkred")
        self.stop.place(x=self.position_x + 125, y=470, w=100)

        self.theme = customtkinter.CTkSwitch(self.principal, text="Dark Mode",
                                command=lambda : [customtkinter.set_appearance_mode(self.main_color.get()),
                                                   self.controller.change_theme(self.main_color.get())],
                                variable=self.main_color, onvalue='dark', offvalue="light")
        self.theme.place(x=self.position_x, y=15)

        self.optionmenu = customtkinter.CTkOptionMenu(self.principal, values=[f"{i}" for i in range(1, 51) if not i % 5])
        self.optionmenu.place(x=self.position_x + 180, y=417, w=70)

        self.elements = (self.theme, self.email_lab, self.password_lab,
                         self.email,self.password, self.prof_lab,
                         self.message_lab, self.connect_lab, self.start,
                         self.stop)

        self.controller.change_language(self.controller.config['language'], self.elements)

        self.language = customtkinter.CTkOptionMenu(self.principal, values=sorted(["pt-BR", "en-US"]),
                                                    command=lambda _: [self.controller.change_language(self.language.get(), self.elements)])
        self.language.set(self.controller.config['language'])
        self.language.place(x=self.position_x + 180, y=15, w=90)

        self.mainloop()
