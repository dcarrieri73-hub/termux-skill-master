#!/usr/bin/env python3
# TERMUX SKILL MASTER v4.6 - Auto-Write & Didactic Edition (English)
import os, subprocess, logging, traceback, json
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Termux_Skill_Project")
os.makedirs(BASE_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(BASE_DIR,"error.log"),
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
    "1":"Simple Input/Output",
    "2":"Persistent JSON Memory",
    "3":"LLM Weights and Training",
    "4":"External HTTP/REST API",
    "5":"Infinity Polling loop",
    "6":"Interactive CLI with menu",
    "7":"Multi-file with modules",
    "8":"Custom",
    "9":"[ANALYSIS/DIDACTIC] Theoretical study only - no code",
}

def clr(): os.system("clear")
def div(c="=",n=46): print(c*n)

def safe_int(msg, lo, hi):
    while True:
        r = input(msg).strip()
        if r.isdigit() and lo <= int(r) <= hi: return int(r)
        print("  [!] Number between "+str(lo)+" and "+str(hi))

def ask_step(step_func):
    while True:
        res = step_func()
        cmd = input("\n  [ENTER] Confirm  [X] Repeat step: ").strip().lower()
        if cmd != 'x': return res

def relog(path):
    lp = os.path.join(path,"error.log")
    rl = logging.getLogger()
    for h in rl.handlers[:]: rl.removeHandler(h)
    rl.addHandler(logging.FileHandler(lp))

def clip(text):
    try:
        subprocess.run(["termux-clipboard-set"],input=text.encode("utf-8"),check=True)
        return True
    except FileNotFoundError:
        logging.error("termux-clipboard-set not found")
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
    hf = os.path.join(path,"prompt_history.json")
    h = []
    if os.path.exists(hf):
        try: h = json.load(open(hf))
        except: h = []
    h.append({"ts":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ver":ver,"prompt":prompt})
    try: json.dump(h,open(hf,"w"),indent=2,ensure_ascii=False)
    except Exception as e: logging.error("history:"+str(e))

def multiline(label):
    print("  "+label+" (Press ENTER twice to finish):")
    lines = []
    while True:
        l = input("  > ")
        if not l: break
        lines.append(l)
    return "\n".join(lines) if lines else "Not specified."

def write_skill_file(path, nome_tool, content):
    filename = f"{nome_tool}.py"
    full_path = os.path.join(path, filename)
    try:
        with open(full_path, "w") as f:
            f.write(content)
        os.chmod(full_path, 0o755)
        return True
    except Exception as e:
        logging.error("File writing: "+str(e))
        return False

def step_workspace():
    clr(); div()
    print("  TERMUX SKILL MASTER v4.6"); div()
    print("\n  [1] New project\n  [2] Open existing\n  [3] Root (no subfolders)\n  [4] New project from Home (~)")
    s = safe_int("Choose (1-4): ",1,4)
    path=BASE_DIR; nome="ROOT"; ver="1.0"
    rel="~/Termux_Skill_Project"; cd="cd "+rel
    if s==1:
        nome = input("  Folder name: ").strip() or "proj_"+datetime.now().strftime("%Y%m%d_%H%M")
        path = os.path.join(BASE_DIR,nome)
        os.makedirs(path,exist_ok=True); save_ver(path,"1.0")
        rel="~/Termux_Skill_Project/"+nome
        cd="mkdir -p "+rel+" && cd "+rel
    elif s==2:
        pl = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR,d))]
        if not pl: print("  No projects found.")
        else:
            for i,p in enumerate(pl,1): print("    ["+str(i)+"] "+p)
            idx = safe_int("  Select: ",1,len(pl))-1
            nome=pl[idx]; path=os.path.join(BASE_DIR,nome)
            ver=get_ver(path)
            rel="~/Termux_Skill_Project/"+nome; cd="cd "+rel
    elif s==4:
        nome = input("  Folder name (in Home): ").strip() or "proj_"+datetime.now().strftime("%Y%m%d_%H%M")
        path = os.path.join(os.path.expanduser("~"),nome)
        os.makedirs(path,exist_ok=True); save_ver(path,"1.0")
        rel="~/"+nome
        cd="cd ~ && mkdir -p "+nome+" && cd "+nome
    relog(path)
    return nome,path,rel,ver,cd

def step_cognitive():
    div("-"); print("  STEP 2 - COGNITIVE MODEL\n")
    print("  Mode: [1] EI Analysis  [2] Coder  [3] Hybrid")
    modo=["EI Analysis","Coder","Hybrid"][safe_int("  Choose (1-3): ",1,3)-1]
    
    print("\n  Autonomy: [1] Strategic Assistant  [2] Autonomous Agent")
    aut="Autonomous Agent" if safe_int("  Choose (1-2): ",1,2)==2 else "Strategic Assistant"
    
    print("\n  Rigidity: [1] Executive  [2] Consultative")
    rig="Executive" if safe_int("  Choose (1-2): ",1,2)==1 else "Consultative"
    return modo,aut,rig

def step_stack():
    div("-"); print("  STEP 3 - TECH STACK\n")
    print("  UI Interface: [1] CLI  [2] Chat Bot  [3] WebApp  [4] Data Only  [5] Desktop GUI  [6] Custom")
    raw_ui = input("  Choose (e.g., 1,3): ").strip()
    mappa_ui = {1:"CLI", 2:"Chat Bot", 3:"WebApp", 4:"Data Only", 5:"Desktop GUI", 6:"Custom"}
    ui_scelte = []
    for x in raw_ui.split(","):
        x = x.strip()
        if x.isdigit() and 1 <= int(x) <= 6:
            ui_scelte.append(mappa_ui[int(x)])
    if not ui_scelte: ui_scelte = ["CLI"]
    ui = " + ".join(ui_scelte)
    
    print("\n  Data Storage: [1] JSON Only  [2] JSON + CSV Export")
    exp="JSON+CSV" if safe_int("  Choose (1-2): ",1,2)==2 else "JSON"
    
    log_on = input("\n  Enable error.log? (y/n): ").strip().lower()=="y"
    poll   = input("  Infinity Polling? (y/n): ").strip().lower()=="y"
    sec    = input("  Separate API keys? (y/n): ").strip().lower()=="y"
    return ui,exp,log_on,poll,sec

def step_language():
    div("-"); print("  STEP 4 - LANGUAGE\n")
    for k,v in LANGS.items(): print("    ["+k+"] "+v[0])
    s=safe_int("  Choose (1-7): ",1,7); preset=LANGS[str(s)]
    if s==7:
        lp = input("  Prompt Language: ").strip() or "English"
        lr = input("  Response Language: ").strip() or "English"
        lc = input("  Code Language: ").strip() or "English"
    else: 
        lp,lr,lc=preset[1],preset[2],preset[3]
    return lp,lr,lc

def step_ei():
    div("-"); print("  STEP 5 - EI ANALYSIS\n")
    obj  = input("  Objective: ").strip() or "Not specified"
    vers = input("  Version: ").strip() or "v1.0"
    tool = input("  Tool/Framework: ").strip() or "Not specified"
    deps = input("  Dependencies (e.g., requests, telebot): ").strip() or ""
    tech = multiline("Technical description / request")
    return obj,vers,tool,deps,tech

def step_desc():
    div("-"); print("  STEP 6 - STRATEGIC DESCRIPTION\n")
    return multiline("Project goal")

def step_tools():
    div("-"); print("  STEP 7 - TOOLS DEFINITION\n")
    for k,v in TOOL_TYPES.items(): print("    ["+k+"] "+v)
    raw = input("\n  Choose (e.g., 1,4 | 9 for Analysis only): ").strip()

    tipi_sel = []; is_didactic = False
    for x in raw.split(","):
        x = x.strip()
        if x == "9":
            is_didactic = True
            tipi_sel = ["ANALYSIS/DIDACTIC - Theoretical study without code"]; break
        elif x == "8":
            tipi_sel.append(input("  Describe custom tool: ").strip() or "Custom")
        elif x in TOOL_TYPES: tipi_sel.append(TOOL_TYPES[x])
    if not tipi_sel: tipi_sel = ["Simple Input/Output"]

    if is_didactic:
        nome_tool = input("  Analysis title: ").strip() or "Theoretical_Analysis"
        n_tools, extra = "1", ""
        funzione = multiline("What do you want to study/analyze?")
    else:
        nome_tool = input("  Tool file name (e.g., main_bot): ").strip() or "main"
        n_tools = input("  How many tools?: ") or "1"
        funzione = multiline("What does the tool do?")
        extra = ""
        if any("Weights" in t for t in tipi_sel): extra += "  Weights: "+(input("  Weights structure: ") or "JSON")+"\n"
        if any("API" in t for t in tipi_sel): extra += "  API: "+(input("  API Endpoint: ") or "N/A")+"\n"

    return tipi_sel, nome_tool, funzione, n_tools, extra, is_didactic

def build_prompt(nome,path,rel,ver,cd,modo,aut,rig,ui,exp,log_on,poll,sec,
                 lp,lr,lc,obj,vers,tool,deps,tech,desc,
                 tipi_tool,nome_tool,funzione_tool,n_tools,extra_tool,is_didactic):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    S = "="*46
    out = f"{S}\n HYBRID SKILL v{ver} - {nome}\n Path: {rel}\n {cd}\n"
    if is_didactic: out += " Mode: ANALYSIS/DIDACTIC\n"
    out += f"{S}\n\nOBJECTIVE: {obj}\nVERSION: {vers}\nTOOL: {tool}\n"
    if not is_didactic and deps: out += f"DEPENDENCIES: {deps}\n"
    
    out += f"\nTECHNICAL:\n{tech}\n\nSTRATEGY:\n{desc}\n\n"
    out += f"CONFIGURATION:\nMode={modo} | Autonomy={aut} | Languages={lr}\n"
    out += f"STACK: UI={ui} | Log={log_on} | Polling={poll}\n\n"
    
    out += f"TOOLS ({nome_tool}):\n"
    for t in tipi_tool: out += f" - {t}\n"
    out += f"\nFUNCTION:\n{funzione_tool}\n\n"
    
    out += f"{S}\n  INSTRUCTIONS\n{S}\n"
    if is_didactic:
        out += "[1] MODE: ANALYSIS ONLY (Schemas, tables, explanations. NO EXECUTABLE CODE).\n"
    else:
        out += "[1] SAFE BOOTSTRAP: Check for dependencies first. Use scripts or `pip install` ONLY if the modules are missing on the system.\n"
        out += f"[2] PROTOCOL: Send COMPLETE CODE with cat-EOF to {rel}/{nome_tool}.py\n"
    out += "[3] LOGGING: Always manage and update error.log.\n"
    out += "[4] API POLICY: If external APIs are needed, exclusively use free and available APIs without blocking authentication. If unavailable, program the function from scratch locally.\n"
    out += "[5] ANTI-HALLUCINATION & CLARIFICATION: If the strategy mentions pre-existing components not provided, presents ambiguities, or has logical gaps, DO NOT invent fake code. Stop and ask clarifying questions to the user.\n"
    return out

def main():
    while True:
        clr()
        nome,path,rel,ver,cd = ask_step(step_workspace)
        modo,aut,rig = ask_step(step_cognitive)
        ui,exp,log_on,poll,sec = ask_step(step_stack)
        lp,lr,lc = ask_step(step_language)
        obj,vers,tool,deps,tech = ask_step(step_ei)
        desc = ask_step(step_desc)
        tipi_t,nome_t,fun_t,n_t,ex_t,did = ask_step(step_tools)

    prompt = build_prompt(nome,path,rel,ver,cd,modo,aut,rig,ui,exp,log_on,poll,sec,
                          lp,lr,lc,obj,vers,tool,deps,tech,desc,
                          tipi_t,nome_t,fun_t,n_t,ex_t,did)

    with open(os.path.join(path,"latest_prompt.txt"),"w") as f: f.write(prompt)
    save_history(path,prompt,ver)
    if nome!="ROOT": save_ver(path,ver)

    clr(); div(); print(prompt); div()

    if clip(prompt): print("\n  ✅ Prompt copied to clipboard!")

    if not did:
        div("-")
        if input(f"  Do you want to auto-create an empty {nome_t}.py now? (y/n): ").lower() == 'y':
            if write_skill_file(path, nome_t, f"#!/usr/bin/env python3\n# v{ver} - {nome_t}\n"):
                print(f"  ✅ OK: File created and executable in: {rel}/{nome_t}.py")

    input("\nPress ENTER to close...")

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        print("\n  [!] Interrupted by user. Exiting cleanly.")
    except Exception as e:
        logging.error("CRASH:\n"+traceback.format_exc())
        print("\n  [X] CRITICAL ERROR - Details saved in error.log")
        input("Press ENTER to close...")
