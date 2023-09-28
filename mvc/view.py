import customtkinter
from PIL import Image
from mvc.controller import BotController


class Bot(customtkinter.CTk):
    """Cria a classe Bot herdando da super classe customtkinter.CTk"""
    font_size = 15
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
        self.email_lab.place(x=self.position_x, y=37)

        self.password_lab = customtkinter.CTkLabel(self.principal, text='Password:', font=('Arial', self.font_size))
        self.password_lab.place(x=self.position_x, y=102)

        self.prof_lab = customtkinter.CTkLabel(self.principal, text='Profession to Search:', font=('Arial', self.font_size))
        self.prof_lab.place(x=self.position_x, y=145)

        self.message_lab = customtkinter.CTkLabel(self.principal, text='Custom Message to send: ', font=('Arial', self.font_size))
        self.message_lab.place(x=self.position_x, y=220)

        self.connect_lab = customtkinter.CTkLabel(self.principal, text='Number of Connections: ', font=('Arial', self.font_size))
        self.connect_lab.place(x=self.position_x, y=420)


        self.email = customtkinter.CTkEntry(self.principal, font=('Arial', self.font_size), placeholder_text='Your E-mail')
        self.email.place(x=self.position_x, y=60, w=375)

        self.password = customtkinter.CTkEntry(self.principal, font=('Arial', self.font_size), show='*', placeholder_text='Your Password')
        self.password.place(x=90, y=102,  w=260)

        self.see_password = customtkinter.CTkButton(self.principal, font=('Arial', self.font_size), text='', fg_color='#ABABAB', hover_color='#6E6E6E',
                                                    image=customtkinter.CTkImage(Image.open('images/eye.png')),
                                                    command=lambda: [self.controller.show_password(self.password, self.see_password)])
        self.see_password.place(x=355, y=102,  w=35)

        self.profession = customtkinter.CTkEntry(self.principal, font=('Arial', self.font_size))
        self.profession.place(x=self.position_x, y=177,  w=375)


        self.message = customtkinter.CTkTextbox(self.principal, font=('Arial', self.font_size))
        self.message.place(x=self.position_x, y=245, h=165, w=375)


        self.start = customtkinter.CTkButton(self.principal, text='START', font=('Arial', self.font_size),
                                             command=lambda: self.controller.check_elements(self.email.get(),
                                                                                            self.password.get(),
                                                                                            self.profession.get(),
                                                                                            self.message.get("0.0", "end"),
                                                                                            self.optionmenu.get()))
        self.start.place(x=self.position_x, y=470, w=100)

        self.stop = customtkinter.CTkButton(self.principal, text='STOP', font=('Arial', self.font_size), fg_color="red",
                              hover_color="darkred", state='disabled', command=lambda:[self.controller.loggin_out()])
        self.stop.place(x=self.position_x + 125, y=470, w=100)

        self.theme = customtkinter.CTkSwitch(self.principal, text="Dark Mode",
                                command=lambda : [customtkinter.set_appearance_mode(self.main_color.get()),
                                                   self.controller.change_theme(self.main_color.get())],
                                variable=self.main_color, onvalue='dark', offvalue="light")
        self.theme.place(x=self.position_x, y=15)

        self.optionmenu = customtkinter.CTkOptionMenu(self.principal, values=[f"{i}" for i in range(1, 51) if not i % 5])
        self.optionmenu.place(x=self.position_x + 170, y=420, w=60)

        self.elements = (self.theme, self.email_lab, self.password_lab,
                         self.email,self.password, self.prof_lab,
                         self.message_lab, self.connect_lab, self.start,
                         self.stop)

        self.controller.change_language(self.controller.config['language'], self.elements)

        self.language = customtkinter.CTkOptionMenu(self.principal, values=sorted(["pt-BR", "en-US"]),
                                                    command=lambda _: [self.controller.change_language(self.language.get(), self.elements)])
        self.language.set(self.controller.config['language'])
        self.language.place(x=self.position_x + 180, y=15, w=80)

        self.mainloop()
