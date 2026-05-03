#!/usr/bin/env python3
# TERMUX SKILL MASTER v4.7 - Webhook & Mini-App Edition (English)
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
    "1":"Simple Input/Output",
    "2":"Persistent JSON memory",
    "3":"Weights and LLM training",
    "4":"External HTTP/REST API",
    "5":"Infinity Polling loop",
    "6":"Interactive CLI with menu",
    "7":"Multifile with modules",
    "8":"Custom",
    "9":"[ANALYSIS/DIDACTIC] Theoretical study only - no code",
}

def clr(): os.system("clear")
def div(c="=",n=46): print(c*n)

def safe_int(msg, lo, hi):
    while True:
        r = input(msg).strip()
        if r.isdigit() and lo <= int(r) <= hi: return int(r)
        print("  [!] Enter a number between "+str(lo)+" and "+str(hi))

def ask_step(step_func):
    while True:
        res = step_func()
        cmd = input("\n  [ENTER] Confirm  [X] Repeat this step: ").strip().lower()
        if cmd != 'x': return res

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
    print("  "+label+" (ENTER twice to finish):")
    lines = []
    while True:
        l = input("  > ")
        if not l: break
        lines.append(l)
    return "\n".join(lines) if lines else "Not specified."

def write_skill_file(path, tool_name, content):
    filename = f"{tool_name}.py"
    full_path = os.path.join(path, filename)
    try:
        with open(full_path, "w") as f:
            f.write(content)
        os.chmod(full_path, 0o755)
        return True
    except Exception as e:
        logging.error("File write: "+str(e))
        return False

def step_workspace():
    clr(); div()
    print("  TERMUX SKILL MASTER v4.7"); div()
    print("\n  [1] New project\n  [2] Open existing\n  [3] Root (no subfolders)\n  [4] New project from Home (~)")
    s = safe_int("Choose (1-4): ",1,4)
    path=BASE_DIR; name="ROOT"; ver="1.0"
    rel="~/Termux_Skill_Project"; cd="cd "+rel
    if s==1:
        name = input("  Folder name: ").strip() or "proj_"+datetime.now().strftime("%Y%m%d_%H%M")
        path = os.path.join(BASE_DIR,name)
        os.makedirs(path,exist_ok=True); save_ver(path,"1.0")
        rel="~/Termux_Skill_Project/"+name
        cd="mkdir -p "+rel+" && cd "+rel
    elif s==2:
        pl = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR,d))]
        if not pl: print("  No projects found.")
        else:
            for i,p in enumerate(pl,1): print("    ["+str(i)+"] "+p)
            idx = safe_int("  Select: ",1,len(pl))-1
            name=pl[idx]; path=os.path.join(BASE_DIR,name)
            ver=get_ver(path)
            rel="~/Termux_Skill_Project/"+name; cd="cd "+rel
    elif s==4:
        name = input("  Folder name (in Home): ").strip() or "proj_"+datetime.now().strftime("%Y%m%d_%H%M")
        path = os.path.join(os.path.expanduser("~"),name)
        os.makedirs(path,exist_ok=True); save_ver(path,"1.0")
        rel="~/"+name
        cd="cd ~ && mkdir -p "+name+" && cd "+name
    relog(path)
    return name,path,rel,ver,cd

def step_cognitive():
    div("-"); print("  STEP 2 - COGNITIVE MODEL\n")
    print("  Mode: [1] EI Analysis  [2] Coder  [3] Hybrid")
    mode=["EI Analysis","Coder","Hybrid"][safe_int("  Choose (1-3): ",1,3)-1]
    
    print("\n  Autonomy: [1] Strategic Assistant  [2] Autonomous Agent")
    aut="Autonomous Agent" if safe_int("  Choose (1-2): ",1,2)==2 else "Strategic Assistant"
    
    print("\n  Rigidity: [1] Executive  [2] Consultative")
    rig="Executive" if safe_int("  Choose (1-2): ",1,2)==1 else "Consultative"
    return mode,aut,rig

def step_stack():
    div("-"); print("  STEP 3 - TECH STACK\n")
    print("  UI Interface: [1] CLI  [2] Chat Bot  [3] WebApp  [4] Telegram Mini-App  [5] Desktop GUI  [6] Other")
    raw_ui = input("  Choose from menu (e.g., 1,4): ").strip()
    mappa_ui = {1:"CLI", 2:"Chat Bot", 3:"WebApp", 4:"Telegram Mini-App", 5:"Desktop GUI", 6:"Other"}
    ui_scelte = []
    for x in raw_ui.split(","):
        x = x.strip()
        if x.isdigit() and 1 <= int(x) <= 6:
            ui_scelte.append(mappa_ui[int(x)])
    if not ui_scelte: ui_scelte = ["CLI"]
    ui = " + ".join(ui_scelte)
    
    print("\n  Data Management: [1] JSON Only  [2] JSON + CSV Export")
    exp="JSON+CSV" if safe_int("  Choose (1-2): ",1,2)==2 else "JSON"
    
    log_on = input("\n  Enable errors.log? (y/n): ").strip().lower()=="y"
    
    print("\n  Bot Architecture: [1] Infinity Polling (Local)  [2] Webhook")
    if safe_int("  Choose (1-2): ", 1, 2) == 2:
        print("\n  Webhook Environment: [1] Cloud Server (e.g., Render)  [2] Local Termux (e.g., Ngrok/Tunnel)")
        amb = "Cloud Server" if safe_int("  Choose (1-2): ", 1, 2) == 1 else "Local Termux"
        arch = f"Webhook ({amb})"
    else:
        arch = "Infinity Polling"
        
    sec = input("\n  Separate API keys? (y/n): ").strip().lower()=="y"
    return ui,exp,log_on,arch,sec

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
    deps = input("  Dependencies (e.g., requests, telebot, fastapi): ").strip() or ""
    tech = multiline("Technical description / request")
    return obj,vers,tool,deps,tech

def step_desc():
    div("-"); print("  STEP 6 - STRATEGIC DESCRIPTION\n")
    return multiline("Project objective")

def step_tools():
    div("-"); print("  STEP 7 - TOOL DEFINITION\n")
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
        tool_name = input("  Analysis title: ").strip() or "Theoretical_Analysis"
        n_tools, extra = "1", ""
        function = multiline("What do you want to study/analyze?")
    else:
        tool_name = input("  Tool file name (e.g., main_bot): ").strip() or "main"
        n_tools = input("  How many tools?: ") or "1"
        function = multiline("What does the tool do?")
        extra = ""
        if any("Weights" in t for t in tipi_sel): extra += "  Weights: "+(input("  Weight structure: ") or "JSON")+"\n"
        if any("API" in t for t in tipi_sel): extra += "  API: "+(input("  API Endpoint: ") or "N/A")+"\n"

    return tipi_sel, tool_name, function, n_tools, extra, is_didactic

def build_prompt(nome,path,rel,ver,cd,modo,aut,rig,ui,exp,log_on,arch,sec,
                 lp,lr,lc,obj,vers,tool,deps,tech,desc,
                 tipi_tool,tool_name,function_tool,n_tools,extra_tool,is_didactic):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    S = "="*46
    out = f"{S}\n HYBRID SKILL v{ver} - {nome}\n Path: {rel}\n {cd}\n"
    if is_didactic: out += " Mode: ANALYSIS/DIDACTIC\n"
    out += f"{S}\n\nOBJECTIVE: {obj}\nVERSION: {vers}\nTOOL: {tool}\n"
    if not is_didactic and deps: out += f"DEPENDENCIES: {deps}\n"
    
    out += f"\nTECHNIQUE:\n{tech}\n\nSTRATEGY:\n{desc}\n\n"
    out += f"CONFIGURATION:\nMode={modo} | Autonomy={aut} | Language={lr}\n"
    out += f"STACK: UI={ui} | Log={log_on} | Bot Architecture={arch} | Separate Keys={sec}\n\n"
    
    out += f"TOOLS ({tool_name}):\n"
    for t in tipi_tool: out += f" - {t}\n"
    out += f"\nFUNCTION:\n{function_tool}\n\n"
    
    out += f"{S}\n  INSTRUCTIONS\n{S}\n"
    if is_didactic:
        out += "[1] MODE: ANALYSIS ONLY (Schemas, tables, explanations. NO EXECUTABLE CODE).\n"
    else:
        out += "[1] SAFE BOOTSTRAP: Check for dependencies first. Use scripts or `pip install` ONLY if the modules are missing on the system.\n"
        out += f"[2] PROTOCOL: Send COMPLETE CODE with cat-EOF to {rel}/{tool_name}.py\n"
    out += "[3] LOGGING: Always manage and update error.log.\n"
    out += "[4] API POLICY: If external APIs are needed, exclusively use free and available APIs without blocking authentication. If unavailable, program the logic from scratch locally.\n"
    out += "[5] ANTI-HALLUCINATION & CLARIFICATION: If the strategy mentions pre-existing components not provided, presents ambiguities, or has logical gaps, DO NOT invent fake code. Stop and ask clarifying questions to the user.\n"
    return out

def main():
    clr()
    nome,path,rel,ver,cd = ask_step(step_workspace)
    modo,aut,rig = ask_step(step_cognitive)
    ui,exp,log_on,arch,sec = ask_step(step_stack)
    lp,lr,lc = ask_step(step_language)
    obj,vers,tool,deps,tech = ask_step(step_ei)
    desc = ask_step(step_desc)
    tipi_t,nome_t,fun_t,n_t,ex_t,did = ask_step(step_tools)

    prompt = build_prompt(nome,path,rel,ver,cd,modo,aut,rig,ui,exp,log_on,arch,sec,
                          lp,lr,lc,obj,vers,tool,deps,tech,desc,
                          tipi_t,nome_t,fun_t,n_t,ex_t,did)

    with open(os.path.join(path,"latest_prompt.txt"),"w") as f: f.write(prompt)
    save_history(path,prompt,ver)
    if nome!="ROOT": save_ver(path,ver)

    clr(); div(); print(prompt); div()

    if clip(prompt): print("\n  ✅ Prompt copied to clipboard!")

    if not did:
        div("-")
        if input(f"  Do you want to automatically create empty {nome_t}.py now? (y/n): ").lower() == 'y':
            if write_skill_file(path, nome_t, f"#!/usr/bin/env python3\n# v{ver} - {nome_t}\n"):
                print(f"  ✅ OK: File created and executable at: {rel}/{nome_t}.py")

    input("\nPress ENTER to close...")

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        print("\n  [!] Interrupted by user. Clean exit.")
    except Exception as e:
        logging.error("CRASH:\n"+traceback.format_exc())
        print("\n  [X] CRITICAL ERROR - Details saved in error.log")
        input("Press ENTER to close...")
