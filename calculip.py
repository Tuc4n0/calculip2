import customtkinter as ctk
import ipaddress
import pyperclip

def atualizar_exemplo(*args):
    classe = combo_class.get()

    if classe == "A":
        entrada_ip.delete(0, "end")
        entrada_ip.insert(0, "10.0.0.1")
        combo_mask.set("/8")
    elif classe == "B":
        entrada_ip.delete(0, "end")
        entrada_ip.insert(0, "172.16.0.1")
        combo_mask.set("/16")
    elif classe == "C":
        entrada_ip.delete(0, "end")
        entrada_ip.insert(0, "192.168.0.1")
        combo_mask.set("/24")

def calcular():
    try:
        ip = entrada_ip.get().strip()
        if not ip:
            raise ValueError("Informe um endereço IP.")

        prefixo = combo_mask.get().replace("/", "")
        if not prefixo.isdigit():
            raise ValueError("Selecione uma máscara válida.")

        prefixo = int(prefixo)
        if prefixo < 1 or prefixo > 30:
            raise ValueError("A máscara deve estar entre /1 e /30.")

        rede = ipaddress.ip_network(f"{ip}/{prefixo}", strict=False)

        network = rede.network_address
        broadcast = rede.broadcast_address
        mascara_decimal = str(rede.netmask)

        total_hosts = rede.num_addresses - 2 if rede.num_addresses > 2 else 0
        hosts_lista = list(rede.hosts())
        first_host = hosts_lista[0] if hosts_lista else "N/A"
        last_host = hosts_lista[-1] if hosts_lista else "N/A"

        resultado_text.delete("1.0", "end")
        resultado_text.insert("end", f"Endereço Inserido: {ip}\n")
        resultado_text.insert("end", f"Máscara: {mascara_decimal} (/{prefixo})\n")
        resultado_text.insert("end", f"Endereço de Rede: {network}\n")
        resultado_text.insert("end", f"Primeiro IP Válido: {first_host}\n")
        resultado_text.insert("end", f"Último IP Válido: {last_host}\n")
        resultado_text.insert("end", f"Broadcast: {broadcast}\n")
        resultado_text.insert("end", f"Hosts possíveis: {total_hosts}\n\n")

        # Gera sub-redes automáticas (se possível)
        resultado_text.insert("end", "Sub-redes (prefixo +1):\n")
        nova_mascara = prefixo + 1 if prefixo < 32 else prefixo
        subnets = list(rede.subnets(new_prefix=nova_mascara))
        for s in subnets[:8]:  # limita a exibir só as primeiras
            resultado_text.insert("end", f" - {s}\n")

    except Exception as e:
        resultado_text.delete("1.0", "end")
        resultado_text.insert("end", f"Erro: {e}")

def copiar_resultado():
    pyperclip.copy(resultado_text.get("1.0", "end-1c"))

def limpar():
    entrada_ip.delete(0, "end")
    combo_class.set("")
    combo_mask.set("")
    resultado_text.delete("1.0", "end")

def alternar_tema():
    modo_atual = ctk.get_appearance_mode()
    if modo_atual == "Light":
        ctk.set_appearance_mode("Dark")
        botao_tema.configure(text="☀️ Modo Claro")
    else:
        ctk.set_appearance_mode("Light")
        botao_tema.configure(text="🌙 Modo Escuro")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Calculadora de IP (Completa)")
app.geometry("680x600")

frame = ctk.CTkFrame(app)
frame.pack(pady=18, padx=18, fill="both", expand=True)

titulo = ctk.CTkLabel(frame, text="Calculadora de IP", font=("Arial", 24, "bold"))
titulo.pack(pady=10)

entrada_frame = ctk.CTkFrame(frame)
entrada_frame.pack(pady=10, fill="x")

ctk.CTkLabel(entrada_frame, text="Classe:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
combo_class = ctk.CTkComboBox(
    entrada_frame,
    values=["A", "B", "C"],
    width=100,
    command=atualizar_exemplo
)
combo_class.set("")
combo_class.grid(row=0, column=1, padx=6, pady=6, sticky="w")

ctk.CTkLabel(entrada_frame, text="Endereço IP:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
entrada_ip = ctk.CTkEntry(entrada_frame, placeholder_text="Ex: 192.168.0.1", width=200)
entrada_ip.grid(row=0, column=3, padx=6, pady=6, sticky="w")

ctk.CTkLabel(entrada_frame, text="Máscara:").grid(row=0, column=4, padx=6, pady=6, sticky="w")
combo_mask = ctk.CTkComboBox(
    entrada_frame,
    values=[f"/{i}" for i in range(1, 31)],
    width=90
)
combo_mask.set("")
combo_mask.grid(row=0, column=5, padx=6, pady=6, sticky="w")

botoes_frame = ctk.CTkFrame(frame)
botoes_frame.pack(pady=10)

botao_calcular = ctk.CTkButton(botoes_frame, text="Calcular", command=calcular, width=120)
botao_calcular.grid(row=0, column=0, padx=8, pady=6)

botao_copiar = ctk.CTkButton(botoes_frame, text="Copiar Resultado", command=copiar_resultado, width=150)
botao_copiar.grid(row=0, column=1, padx=8, pady=6)

botao_limpar = ctk.CTkButton(botoes_frame, text="Limpar", command=limpar, width=100)
botao_limpar.grid(row=0, column=2, padx=8, pady=6)

botao_tema = ctk.CTkButton(botoes_frame, text="🌙 Modo Escuro", command=alternar_tema, width=130)
botao_tema.grid(row=0, column=3, padx=8, pady=6)

resultado_text = ctk.CTkTextbox(frame, height=340, width=620)
resultado_text.pack(pady=10)

app.mainloop()
