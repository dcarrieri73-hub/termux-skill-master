#!/usr/bin/env python3
# TERMUX SKILL MASTER v4.6 - Auto-Write & Didactic Edition (Italiano)
import os, subprocess, logging, traceback, json
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Termux_Skill_Project")
os.makedirs(BASE_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(BASE_DIR,"errori.log"),
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

LANGS = {
    "1":("Full English","English","English","English"),
    "2":("Full Italian","Italian","Italian","Italian"),
    "3":("Full German","German","German","German"),
    "4":("Italian > English","Italian","English","English"),
    "5":("Italian > German","Italian","Italian","German"),
    "6":("English > German","English","English","German"),
    "7":("Custom",None,None,None),
}

TOOL_TYPES = {
    "1":"Input/Output semplice",
    "2":"Memoria JSON persistente",
    "3":"Pesi e training LLM",
    "4":"API esterna HTTP/REST",
    "5":"Infinity Polling loop",
    "6":"CLI interattiva con menu",
    "7":"Multifile con moduli",
    "8":"Custom",
    "9":"[ANALISI/DIDATTICA] Solo studio teorico - nessun codice",
}

def clr(): os.system("clear")
def div(c="=",n=46): print(c*n)

def safe_int(msg, lo, hi):
    while True:
        r = input(msg).strip()
        if r.isdigit() and lo <= int(r) <= hi: return int(r)
        print("  [!] Inserisci un numero tra "+str(lo)+" e "+str(hi))

def relog(path):
    lp = os.path.join(path,"errori.log")
    rl = logging.getLogger()
    for h in rl.handlers[:]: rl.removeHandler(h)
    rl.addHandler(logging.FileHandler(lp))

def clip(text):
    try:
        subprocess.run(["termux-clipboard-set"],input=text.encode("utf-8"),check=True)
        return True
    except FileNotFoundError:
        logging.error("termux-clipboard-set non trovato")
        return False
    except Exception as e:
        logging.error("Clipboard: "+str(e))
        return False

def get_ver(path):
    vf = os.path.join(path,"version.txt")
    try:
        if os.path.exists(vf):
            p = open(vf).read().strip().split(".")
            if len(p)==2 and all(x.isdigit() for x in p):
                p[-1]=str(int(p[-1])+1); return ".".join(p)
    except Exception as e: logging.error("ver:"+str(e))
    return "1.0"

def save_ver(path,v):
    try: open(os.path.join(path,"version.txt"),"w").write(v)
    except Exception as e: logging.error("save_ver:"+str(e))

def save_history(path,prompt,ver):
    hf = os.path.join(path,"storico_prompt.json")
    h = []
    if os.path.exists(hf):
        try: h = json.load(open(hf))
        except: h = []
    h.append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ver":ver,"prompt":prompt})
    try: json.dump(h,open(hf,"w"),indent=2,ensure_ascii=False)
    except Exception as e: logging.error("history:"+str(e))

def multiline(label):
    print("  "+label+" (INVIO due volte per finire):")
    lines = []
    while True:
        l = input("  > ")
        if not l: break
        lines.append(l)
    return "\n".join(lines) if lines else "Non specificato."

def write_skill_file(path, nome_tool, content):
    filename = f"{nome_tool}.py"
    full_path = os.path.join(path, filename)
    try:
        with open(full_path, "w") as f:
            f.write(content)
        os.chmod(full_path, 0o755)
        return True
    except Exception as e:
        logging.error("Scrittura file: "+str(e))
        return False

def step_workspace():
    clr(); div()
    print("  TERMUX SKILL MASTER v4.6"); div()
    print("\n  [1] Nuovo progetto\n  [2] Apri esistente\n  [3] Root (senza sottocartelle)")
    s = safe_int("Scegli (1-3): ",1,3)
    path=BASE_DIR; nome="ROOT"; ver="1.0"
    rel="~/Termux_Skill_Project"; cd="cd "+rel
    if s==1:
        nome = input("  Nome cartella: ").strip() or "proj_"+datetime.now().strftime("%Y%m%d_%H%M")
        path = os.path.join(BASE_DIR,nome)
        os.makedirs(path,exist_ok=True); save_ver(path,"1.0")
        rel="~/Termux_Skill_Project/"+nome
        cd="mkdir -p "+rel+" && cd "+rel
    elif s==2:
        pl = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR,d))]
        if not pl: print("  Nessun progetto trovato.")
        else:
            for i,p in enumerate(pl,1): print("    ["+str(i)+"] "+p)
            idx = safe_int("  Seleziona: ",1,len(pl))-1
            nome=pl[idx]; path=os.path.join(BASE_DIR,nome)
            ver=get_ver(path)
            rel="~/Termux_Skill_Project/"+nome; cd="cd "+rel
    relog(path)
    return nome,path,rel,ver,cd

def step_cognitive():
    div("-"); print("  STEP 2 - MODELLO COGNITIVO\n")
    print("  Modo: [1] Analisi EI  [2] Coder  [3] Ibrido")
    modo=["Analisi EI","Coder","Ibrido"][safe_int("  Scegli (1-3): ",1,3)-1]
    
    print("\n  Autonomia: [1] Assistente Strategico  [2] Agente Autonomo")
    aut="Agente Autonomo" if safe_int("  Scegli (1-2): ",1,2)==2 else "Assistente Strategico"
    
    print("\n  Rigidita: [1] Esecutivo  [2] Consultivo")
    rig="Esecutivo" if safe_int("  Scegli (1-2): ",1,2)==1 else "Consultivo"
    return modo,aut,rig

def step_stack():
    div("-"); print("  STEP 3 - TECH STACK\n")
    print("  Interfaccia UI: [1] CLI  [2] Chat Bot  [3] WebApp  [4] Solo dati")
    ui={1:"CLI",2:"Chat Bot",3:"WebApp",4:"Solo dati"}[safe_int("  Scegli (1-4): ",1,4)]
    
    print("\n  Gestione Dati: [1] Solo JSON  [2] JSON + CSV Export")
    exp="JSON+CSV" if safe_int("  Scegli (1-2): ",1,2)==2 else "JSON"
    
    log_on = input("\n  Attivare errori.log? (s/n): ").strip().lower()=="s"
    poll   = input("  Infinity Polling? (s/n): ").strip().lower()=="s"
    sec    = input("  Separare API keys? (s/n): ").strip().lower()=="s"
    return ui,exp,log_on,poll,sec

def step_language():
    div("-"); print("  STEP 4 - LINGUA\n")
    for k,v in LANGS.items(): print("    ["+k+"] "+v[0])
    s=safe_int("  Scegli (1-7): ",1,7); preset=LANGS[str(s)]
    if s==7:
        lp = input("  Lingua Prompt: ").strip() or "Italiano"
        lr = input("  Lingua Risposta: ").strip() or "Italiano"
        lc = input("  Lingua Codice: ").strip() or "Italiano"
    else: 
        lp,lr,lc=preset[1],preset[2],preset[3]
    return lp,lr,lc

def step_ei():
    div("-"); print("  STEP 5 - ANALISI EI\n")
    obj  = input("  Obiettivo: ").strip() or "Non specificato"
    vers = input("  Versione: ").strip() or "v1.0"
    tool = input("  Tool/Framework: ").strip() or "Non specificato"
    deps = input("  Dipendenze (es. requests, telebot): ").strip() or ""
    tech = multiline("Descrizione tecnica / richiesta")
    return obj,vers,tool,deps,tech

def step_desc():
    div("-"); print("  STEP 6 - DESCRIZIONE STRATEGICA\n")
    return multiline("Obiettivo del progetto")

def step_tools():
    div("-"); print("  STEP 7 - DEFINIZIONE TOOLS\n")
    for k,v in TOOL_TYPES.items(): print("    ["+k+"] "+v)
    raw = input("\n  Scegli (es: 1,4 | 9 per solo Analisi): ").strip()

    tipi_sel = []; is_didactic = False
    for x in raw.split(","):
        x = x.strip()
        if x == "9":
            is_didactic = True
            tipi_sel = ["ANALISI/DIDATTICA - Studio teorico senza codice"]; break
        elif x == "8":
            tipi_sel.append(input("  Descrivi tool custom: ").strip() or "Custom")
        elif x in TOOL_TYPES: tipi_sel.append(TOOL_TYPES[x])
    if not tipi_sel: tipi_sel = ["Input/Output semplice"]

    if is_didactic:
        nome_tool = input("  Titolo analisi: ").strip() or "Analisi_Teorica"
        n_tools, extra = "1", ""
        funzione = multiline("Cosa vuoi studiare/analizzare?")
    else:
        nome_tool = input("  Nome file tool (es: main_bot): ").strip() or "main"
        n_tools = input("  Quanti tools?: ") or "1"
        funzione = multiline("Cosa fa il tool?")
        extra = ""
        if any("Pesi" in t for t in tipi_sel): extra += "  Pesi: "+(input("  Struttura pesi: ") or "JSON")+"\n"
        if any("API" in t for t in tipi_sel): extra += "  API: "+(input("  Endpoint API: ") or "N/D")+"\n"

    return tipi_sel, nome_tool, funzione, n_tools, extra, is_didactic

def build_prompt(nome,path,rel,ver,cd,modo,aut,rig,ui,exp,log_on,poll,sec,
                 lp,lr,lc,obj,vers,tool,deps,tech,desc,
                 tipi_tool,nome_tool,funzione_tool,n_tools,extra_tool,is_didactic):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    S = "="*46
    out = f"{S}\n HYBRID SKILL v{ver} - {nome}\n Path: {rel}\n {cd}\n"
    if is_didactic: out += " Modalita: ANALISI/DIDATTICA\n"
    out += f"{S}\n\nOBIETTIVO: {obj}\nVERSIONE: {vers}\nTOOL: {tool}\n"
    if not is_didactic and deps: out += f"DIPENDENZE: {deps}\n"
    
    out += f"\nTECNICA:\n{tech}\n\nSTRATEGIA:\n{desc}\n\n"
    out += f"CONFIGURAZIONE:\nModo={modo} | Autonomia={aut} | Lingue={lr}\n"
    out += f"STACK: UI={ui} | Log={log_on} | Polling={poll}\n\n"
    
    out += f"TOOLS ({nome_tool}):\n"
    for t in tipi_tool: out += f" - {t}\n"
    out += f"\nFUNZIONE:\n{funzione_tool}\n\n"
    
    out += f"{S}\n  ISTRUZIONI\n{S}\n"
    if is_didactic:
        out += "[1] MODALITA: SOLO ANALISI (Schemi, tabelle, spiegazioni. NIENTE CODICE ESEGUIBILE).\n"
    else:
        out += "[1] BOOTSTRAP: Usa pip install per le dipendenze se specificate.\n"
        out += f"[2] PROTOCOLLO: Invia CODICE COMPLETO con cat-EOF su {rel}/{nome_tool}.py\n"
    out += "[3] LOGGING: Gestisci e aggiorna sempre errori.log.\n"
    return out

def main():
    clr()
    nome,path,rel,ver,cd = step_workspace()
    modo,aut,rig = step_cognitive()
    ui,exp,log_on,poll,sec = step_stack()
    lp,lr,lc = step_language()
    obj,vers,tool,deps,tech = step_ei()
    desc = step_desc()
    tipi_t,nome_t,fun_t,n_t,ex_t,did = step_tools()

    prompt = build_prompt(nome,path,rel,ver,cd,modo,aut,rig,ui,exp,log_on,poll,sec,
                          lp,lr,lc,obj,vers,tool,deps,tech,desc,
                          tipi_t,nome_t,fun_t,n_t,ex_t,did)

    with open(os.path.join(path,"latest_prompt.txt"),"w") as f: f.write(prompt)
    save_history(path,prompt,ver)
    if nome!="ROOT": save_ver(path,ver)

    clr(); div(); print(prompt); div()

    if clip(prompt): print("\n  ✅ Prompt copiato negli appunti!")

    if not did:
        div("-")
        if input(f"  Vuoi creare in automatico {nome_t}.py vuoto ora? (s/n): ").lower() == 's':
            if write_skill_file(path, nome_t, f"#!/usr/bin/env python3\n# v{ver} - {nome_t}\n"):
                print(f"  ✅ OK: File creato ed eseguibile in: {rel}/{nome_t}.py")

    input("\nPremi INVIO per chiudere...")

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        print("\n  [!] Interrotto dall'utente. Uscita pulita.")
    except Exception as e:
        logging.error("CRASH:\n"+traceback.format_exc())
        print("\n  [X] ERRORE CRITICO - Dettagli salvati in errori.log")
        input("Premi INVIO per chiudere...")
