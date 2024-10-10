import flet as ft
import re

def main(page: ft.Page):
    page.title = "Conversor de bases"
    lbl_conversao=ft.Text(
        size=22,
        selectable=True
    )
    
    base_regex={
        "Binario": [2,r"^[0-1]*$"],
        "Octal": [8,r"^[0-7]*$"],
        "Decimal": [10,r"^[0-9]*$"],
        "Hexadecimal":[16,r"^[0-9a-f]*$"],
        "Texto":["",r"[.*]*"]
    }
    #numero de caracters minimo para a conversao ser valida, format de minimo necessario
    texto_conversao={
        "Binario": [8,lambda x:f"0{x}b"],
        "Octal": [3,lambda x:f"0{x}o"],
        "Decimal": [3,lambda x:f"0{x}d"],
        "Hexadecimal":[2,lambda x:f"0{x}x"],
        "Texto":[1,lambda x:f"0{x}c"]
    }
    #texto para numero
    def texto_base(input,slc_converte):
        return ' '.join(format(ord(c), texto_conversao[slc_converte][1](texto_conversao[slc_converte][0])) for c in input)
    
    #numero para texto
    def base_texto(input,slc_num,slc_converte):
        input=input.replace(" ","")
        if len(input)>=texto_conversao[slc_num][0]:
            return ''.join([format(int(input[a:a+texto_conversao[slc_num][0]],base_regex[slc_num][0]),
                                    texto_conversao[slc_converte][1](0)) for a in range(0,len(input),texto_conversao[slc_num][0])])

    def conversao():
        if  select_numero.value=="Texto":
            return f"{select_converte.value}: {texto_base(input_numero.value,select_converte.value)}"
        if select_converte.value=="Texto":
            return f"{select_converte.value}: {base_texto(input_numero.value,select_numero.value,select_converte.value)}"
        
        num=format(int(input_numero.value,base_regex[select_numero.value][0]), texto_conversao[select_converte.value][1](0))
        return f"{select_converte.value}: {num}"

    def alterar(e):
        #muda o regex, e se for conversao para texto, permite espaço nos numeros
        input_numero.input_filter.regex_string=base_regex[select_numero.value][1] if select_converte.value!="Texto" else base_regex[select_numero.value][1].replace("[",r"[\s")
        #verifica se o texto, ao mudar o select, bate com o regex
        input_numero.value=input_numero.value if re.search(fr"{str(input_numero.input_filter.regex_string)}", input_numero.value) else ""
        input_numero.update()
        if input_numero.value != '':
            lbl_conversao.value=conversao()
            lbl_conversao.update()
    
    opcoes_select=[ft.dropdown.Option(item) for item in base_regex.keys()]
    select_numero=ft.Dropdown(
        width=200,
        on_change=alterar,
        options=opcoes_select,
        label="De:",
        value="Decimal"
    )
    select_converte = ft.Dropdown(
        width=200,
        on_change=alterar,
        options=opcoes_select,
        label="Para:",
        value="Binario",
        autofocus=True
    )

    input_numero = ft.TextField(
        label="Conversão", 
        hint_text="Valor para conversão", 
        on_change=alterar, 
        input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$")
    )

    row = ft.Row(
        spacing=10, 
        controls=[select_numero,select_converte],
        wrap=True
    )

    page.add(input_numero, row, lbl_conversao)

ft.app(target=main)