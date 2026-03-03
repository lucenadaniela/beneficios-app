import streamlit as st
from db import init_db, fetch_one, fetch_all, execute, CITIES
from auth import authenticate, create_user, user_exists
import datetime as dt
import calendar
import csv
import io

def page_login():
    # CSS Extra apenas para o Login
    st.markdown("""
        <style>
            /* Container principal do login */
            .login-wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 90vh;
                padding: 20px;
            }
            
            /* Card do Login */
            .login-card {
                width: 100%;
                max-width: 420px;
                padding: 3rem 2.5rem;
                background: rgba(17, 20, 28, 0.7);
                backdrop-filter: blur(24px);
                -webkit-backdrop-filter: blur(24px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 28px;
                box-shadow: 
                    0 25px 50px -12px rgba(0, 0, 0, 0.5),
                    0 0 0 1px rgba(255, 255, 255, 0.05),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            
            /* Efeito de gradiente no topo do card */
            .login-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #8b5cf6, #06b6d4, #8b5cf6);
                background-size: 200% 100%;
                animation: gradientMove 3s ease infinite;
            }
            
            @keyframes gradientMove {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Logo / Ícone */
            .login-icon {
                font-size: 4rem;
                margin-bottom: 0.5rem;
                display: inline-block;
                filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.5));
                animation: float 3s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-8px); }
            }
            
            /* Título */
            .login-title {
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                color: #fff !important;
                margin-bottom: 0.5rem !important;
                letter-spacing: -0.03em;
                background: linear-gradient(135deg, #fff 0%, #d1d5db 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            /* Subtítulo */
            .login-subtitle {
                font-size: 0.95rem;
                color: #9ca3af;
                margin-bottom: 2rem;
                font-weight: 400;
            }
            
            /* Labels dos inputs */
            .stTextInput label, .stPassword label {
                color: #e5e7eb !important;
                font-weight: 500 !important;
                font-size: 0.9rem !important;
                margin-bottom: 6px !important;
                text-align: left !important;
                display: block !important;
            }
            
            /* Inputs */
            .stTextInput > div > div > input, .stPassword > div > div > input {
                background: rgba(31, 41, 55, 0.5) !important;
                border: 1px solid #374151 !important;
                border-radius: 12px !important;
                padding: 14px 16px !important;
                font-size: 1rem !important;
                color: #fff !important;
                transition: all 0.2s ease !important;
            }
            
            .stTextInput > div > div > input:focus, .stPassword > div > div > input:focus {
                border-color: #8b5cf6 !important;
                box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
                outline: none !important;
                background: rgba(31, 41, 55, 0.8) !important;
            }
            
            /* Botão de Entrar */
            .login-button button {
                width: 100%;
                padding: 14px !important;
                border-radius: 12px !important;
                font-size: 1.05rem !important;
                font-weight: 600 !important;
                margin-top: 1rem !important;
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                border: none !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.35) !important;
                transition: all 0.25s ease !important;
            }
            
            .login-button button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.45) !important;
            }
            
            .login-button button:active {
                transform: translateY(0);
            }
            
            /* Rodapé / Versão */
            .login-footer {
                margin-top: 2rem;
                font-size: 0.8rem;
                color: #6b7280;
            }
            
            /* Alertas */
            .stAlert {
                background: rgba(239, 68, 68, 0.1) !important;
                border: 1px solid rgba(239, 68, 68, 0.3) !important;
                color: #fca5a5 !important;
                border-radius: 10px !important;
            }
            
            /* Info box */
            .stInfo {
                background: rgba(6, 182, 212, 0.1) !important;
                border: 1px solid rgba(6, 182, 212, 0.3) !important;
                color: #67e8f9 !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown("""
        <div class="login-card">
            <div class="login-icon">🚌</div>
            <h1 class="login-title">WS Benefícios</h1>
            <p class="login-subtitle">Sistema de Gestão de Benefícios</p>
        """, unsafe_allow_html=True)

    # Verifica se é o primeiro acesso
    if not user_exists():
        st.info("👋 Primeiro acesso detected! Crie o administrador do sistema.")
        
        with st.form("create_admin"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Usuário", placeholder="admin")
            with col2:
                password = st.text_input("Senha", type="password", placeholder="••••••")
            
            password2 = st.text_input("Confirmar Senha", type="password", placeholder="••••••")

            st.markdown('<div class="login-button">', unsafe_allow_html=True)
            if st.form_submit_button("✨ Criar Conta", use_container_width=True):
                st.markdown('</div>', unsafe_allow_html=True)
                
                if password != password2:
                    st.error("❌ As senhas não conferem.")
                elif len(password) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres.")
                else:
                    try:
                        create_user(username.strip().lower(), password)
                        st.success("✅ Usuário criado com sucesso! Agora faça login.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao criar usuário: {e}")
            else:
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Formulário de Login Normal
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="••••••••")
        
        st.markdown('<div class="login-button">', unsafe_allow_html=True)
        submit = st.form_submit_button("Entrar no Sistema", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit:
            if authenticate(username.strip().lower(), password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username.strip().lower()
                flash("Login realizado com sucesso! ✅", "success")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos.")

    st.markdown("""
            <div class="login-footer">
                WS Transportes © 2024
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# ────────────────────────────────────────────────
#                   NOTIFICAÇÃO GLOBAL
# ────────────────────────────────────────────────
def flash(message: str, kind: str = "success"):
    """
    kind: success | info | warning | error
    """
    st.session_state["_flash"] = {"kind": kind, "message": message}

def render_flash():
    f = st.session_state.pop("_flash", None)
    if not f:
        return

    # Toast (moderno) + fallback
    try:
        st.toast(f["message"])
    except Exception:
        kind = f.get("kind", "success")
        if kind == "success":
            st.success(f["message"])
        elif kind == "info":
            st.info(f["message"])
        elif kind == "warning":
            st.warning(f["message"])
        else:
            st.error(f["message"])

# ────────────────────────────────────────────────
#                   HELPERS
# ────────────────────────────────────────────────
def require_login():
    if not st.session_state.get("logged_in"):
        st.warning("Faça login para acessar o sistema.")
        st.stop()

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

def uf_label(uf):
    return "Pernambuco (PE)" if uf == "PE" else "Alagoas (AL)"

def cities_by_uf(uf: str):
    return ["Recife", "Paulista"] if uf == "PE" else ["Maceió"]

WEEKDAY_MAP = {
    "Seg": ("pres_mon", 0),
    "Ter": ("pres_tue", 1),
    "Qua": ("pres_wed", 2),
    "Qui": ("pres_thu", 3),
    "Sex": ("pres_fri", 4),
    "Sáb": ("pres_sat", 5),
}

def money(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def to_csv_bytes(rows: list[dict]) -> bytes:
    if not rows:
        return b""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()), delimiter=";")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return output.getvalue().encode("utf-8-sig")

def ym_str(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"

def month_dates(year: int, month: int):
    cal = calendar.Calendar()
    for d in cal.itermonthdates(year, month):
        if d.month == month:
            yield d

def next_month_ym(d: dt.date) -> str:
    year = d.year + (1 if d.month == 12 else 0)
    month = 1 if d.month == 12 else d.month + 1
    return ym_str(year, month)

def get_holidays_set(city: str, year: int, month: int) -> set[dt.date]:
    rows = fetch_all("""
        SELECT date FROM holidays_city_date
        WHERE city = ? AND substr(date,1,7) = ?;
    """, (city, ym_str(year, month)))
    s = set()
    for r in rows:
        try:
            s.add(dt.date.fromisoformat(r["date"]))
        except:
            pass
    return s

def count_work_days_by_schedule(city: str, year: int, month: int, schedule: str) -> int:
    holidays = get_holidays_set(city, year, month)
    count = 0
    for d in month_dates(year, month):
        wd = d.weekday()
        ok = (wd <= 4) if schedule == "SEG-SEX" else (wd <= 5)
        if ok and d not in holidays:
            count += 1
    return count

def count_presential_days_with_schedule(employee_row, city: str, year: int, month: int) -> int:
    schedule = (employee_row["work_schedule"] or "SEG-SEX").upper()
    holidays = get_holidays_set(city, year, month)
    keys = set(employee_row.keys()) if hasattr(employee_row, "keys") else set()

    selected_weekdays = set()
    for _, (col, wd) in WEEKDAY_MAP.items():
        val = employee_row[col] if col in keys else 0
        if int(val or 0) == 1:
            selected_weekdays.add(wd)

    pres = 0
    for d in month_dates(year, month):
        wd = d.weekday()
        if schedule == "SEG-SEX" and wd > 4:
            continue
        if schedule == "SEG-SAB" and wd > 5:
            continue
        if wd in selected_weekdays and d not in holidays:
            pres += 1
    return pres

def get_benefit_deltas(employee_id: int, year: int, month: int):
    row = fetch_one("""
        SELECT COALESCE(SUM(vt_delta), 0) AS vt,
               COALESCE(SUM(va_delta), 0) AS va
        FROM benefit_day_adjustments
        WHERE employee_id = ? AND pay_month = ?;
    """, (employee_id, ym_str(year, month)))
    row_dict = dict(row) if row else {}
    return int(row_dict.get("vt", 0)), int(row_dict.get("va", 0))

def list_benefit_deltas(employee_id: int, year: int, month: int):
    return fetch_all("""
        SELECT id, date, vt_delta, va_delta, note, pay_month
        FROM benefit_day_adjustments
        WHERE employee_id = ? AND pay_month = ?
        ORDER BY date;
    """, (employee_id, ym_str(year, month)))

def backfill_pay_month_if_null():
    rows = fetch_all("SELECT id, date FROM benefit_day_adjustments WHERE pay_month IS NULL OR pay_month = '';")
    for r in rows:
        try:
            d = dt.date.fromisoformat(r["date"])
            pm = next_month_ym(d)
            execute("UPDATE benefit_day_adjustments SET pay_month = ? WHERE id = ?;", (pm, int(r["id"])))
        except:
            pass

# ────────────────────────────────────────────────
#                   FÉRIAS
# ────────────────────────────────────────────────
def daterange(d1: dt.date, d2: dt.date):
    cur = d1
    while cur <= d2:
        yield cur
        cur += dt.timedelta(days=1)

def list_vacations(employee_id: int):
    return fetch_all("""
        SELECT id, start_date, end_date, note
        FROM vacations
        WHERE employee_id = ?
        ORDER BY start_date;
    """, (employee_id,))

def get_vacation_dates_in_month(employee_id: int, year: int, month: int) -> set[dt.date]:
    ym = ym_str(year, month)
    rows = fetch_all("""
        SELECT start_date, end_date
        FROM vacations
        WHERE employee_id = ?
          AND (substr(start_date,1,7) <= ? AND substr(end_date,1,7) >= ?);
    """, (employee_id, ym, ym))

    s = set()
    for r in rows:
        try:
            a = dt.date.fromisoformat(r["start_date"])
            b = dt.date.fromisoformat(r["end_date"])
            for d in daterange(a, b):
                if d.year == year and d.month == month:
                    s.add(d)
        except:
            pass
    return s

def count_vacation_workdays(employee_row, city: str, year: int, month: int) -> tuple[int, int]:
    """
    Retorna:
      (qtd_dias_uteis_de_ferias, qtd_dias_presenciais_de_ferias)
    """
    schedule = (employee_row["work_schedule"] or "SEG-SEX").upper()
    holidays = get_holidays_set(city, year, month)
    vac_dates = get_vacation_dates_in_month(int(employee_row["id"]), year, month)

    keys = set(employee_row.keys()) if hasattr(employee_row, "keys") else set()
    selected_weekdays = set()
    for _, (col, wd) in WEEKDAY_MAP.items():
        val = employee_row[col] if col in keys else 0
        if int(val or 0) == 1:
            selected_weekdays.add(wd)

    vac_workdays = 0
    vac_presential_days = 0

    for d in vac_dates:
        wd = d.weekday()

        if schedule == "SEG-SEX" and wd > 4:
            continue
        if schedule == "SEG-SAB" and wd > 5:
            continue
        if d in holidays:
            continue

        vac_workdays += 1
        if wd in selected_weekdays:
            vac_presential_days += 1

    return vac_workdays, vac_presential_days

# ────────────────────────────────────────────────
#                   INIT + SESSION
# ────────────────────────────────────────────────
init_db()
backfill_pay_month_if_null()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# mostra notificação pendente (se houver)
render_flash()

# ────────────────────────────────────────────────
#                   SIDEBAR
# ────────────────────────────────────────────────
if st.session_state["logged_in"]:
    st.sidebar.markdown("### 🚌 WS Transportes")
    st.sidebar.caption(f"**{st.session_state.get('username', '').title()}**")
    st.sidebar.markdown("---")

    pages = {
        "⚙️ Configurações": "config",
        "👥 Funcionários": "employees",
        "📊 Quadro Mensal": "quadro"
    }

    choice = st.sidebar.radio("Navegação", list(pages.keys()))
    current_page = pages[choice]

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair"):
        logout()
        flash("Você saiu do sistema.", "info")
        st.rerun()
else:
    current_page = "login"

# ────────────────────────────────────────────────
#                   PÁGINAS
# ────────────────────────────────────────────────
def page_login():
    st.markdown('<div class="login-container"><div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Sistema de Benefícios</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8b949e; margin-bottom:2rem;'>WS Transportes</p>", unsafe_allow_html=True)

    if not user_exists():
        st.info("Primeiro acesso: crie o administrador")
        with st.form("create_admin"):
            col1, col2 = st.columns(2)
            username = col1.text_input("Usuário", value="admin")
            password = col2.text_input("Senha", type="password")
            password2 = st.text_input("Confirmar senha", type="password")

            if st.form_submit_button("Criar conta", use_container_width=True):
                if password != password2:
                    flash("Senhas não conferem.", "error")
                    st.rerun()
                elif len(password) < 6:
                    flash("Senha deve ter pelo menos 6 caracteres.", "error")
                    st.rerun()
                else:
                    try:
                        create_user(username, password)
                        flash("Usuário criado! Faça login.", "success")
                        st.rerun()
                    except Exception as e:
                        flash(f"Erro: {e}", "error")
                        st.rerun()

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar", type="primary", use_container_width=True):
            if authenticate(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username.strip().lower()
                flash("Login realizado com sucesso ✅", "success")
                st.rerun()
            else:
                flash("Usuário ou senha inválidos.", "error")
                st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

def page_config():
    require_login()
    st.header("⚙️ Configurações")

    config_row = fetch_one("SELECT * FROM config WHERE id = 1;")
    config = dict(config_row) if config_row else {}

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("Valores por UF")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Pernambuco (PE)**")
            vt_pe = st.number_input("Valor VT PE", value=float(config.get("vt_pe", 0)), step=0.5)
            va_vr_pe = st.number_input("Valor VA/VR PE", value=float(config.get("va_vr_pe", 0)), step=0.5)
            vt_sup_pe = st.number_input("VT fixo supervisor PE", value=float(config.get("vt_fixo_supervisor_pe", 0)), step=0.5)
            ho_pe_a = st.number_input("Homeoffice PE - A", value=float(config.get("homeoffice_pe", 0)), step=0.5)
            ho_pe_b = st.number_input("Homeoffice PE - B", value=float(config.get("homeoffice_pe_b", 0)), step=0.5)
        with c2:
            st.markdown("**Alagoas (AL)**")
            vt_al = st.number_input("Valor VT AL", value=float(config.get("vt_al", 0)), step=0.5)
            va_vr_al = st.number_input("Valor VA/VR AL", value=float(config.get("va_vr_al", 0)), step=0.5)
            vt_sup_al = st.number_input("VT fixo supervisor AL", value=float(config.get("vt_fixo_supervisor_al", 0)), step=0.5)
            ho_al_a = st.number_input("Homeoffice AL - A", value=float(config.get("homeoffice_al", 0)), step=0.5)
            ho_al_b = st.number_input("Homeoffice AL - B", value=float(config.get("homeoffice_al_b", 0)), step=0.5)

        if st.button("💾 Salvar configurações", type="primary"):
            execute("""
                UPDATE config SET
                    vt_pe = ?, vt_al = ?,
                    va_vr_pe = ?, va_vr_al = ?,
                    vt_fixo_supervisor_pe = ?, vt_fixo_supervisor_al = ?,
                    homeoffice_pe = ?, homeoffice_pe_b = ?,
                    homeoffice_al = ?, homeoffice_al_b = ?,
                    updated_at = datetime('now')
                WHERE id = 1;
            """, (vt_pe, vt_al, va_vr_pe, va_vr_al, vt_sup_pe, vt_sup_al, ho_pe_a, ho_pe_b, ho_al_a, ho_al_b))
            flash("Configurações salvas com sucesso ✅", "success")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("Feriados por Cidade")

        city = st.selectbox("Cidade", CITIES, key="hol_city")
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            date_val = st.date_input("Data do feriado", dt.date.today())
        with col2:
            name_val = st.text_input("Nome (opcional)")
        with col3:
            st.write("")
            if st.button("Adicionar feriado"):
                execute(
                    "INSERT OR IGNORE INTO holidays_city_date (city, date, name) VALUES (?, ?, ?);",
                    (city, date_val.isoformat(), name_val.strip() or None)
                )
                flash("Feriado adicionado ✅", "success")
                st.rerun()

        rows = fetch_all("SELECT date, name FROM holidays_city_date WHERE city = ? ORDER BY date;", (city,))
        if rows:
            st.dataframe([{"Data": r["date"], "Nome": r["name"] or ""} for r in rows],
                         use_container_width=True, hide_index=True)
            del_date = st.selectbox("Excluir data", [r["date"] for r in rows])
            if st.button("Excluir feriado selecionado"):
                execute("DELETE FROM holidays_city_date WHERE city = ? AND date = ?;", (city, del_date))
                flash("Feriado excluído ✅", "success")
                st.rerun()
        else:
            st.info("Nenhum feriado cadastrado para esta cidade.")

        st.markdown('</div>', unsafe_allow_html=True)

def page_employees():
    require_login()
    st.header("👥 Funcionários")

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("Cadastrar Novo")

        name = st.text_input("Nome completo")
        cpf = st.text_input("CPF")
        uf = st.selectbox("UF", ["PE", "AL"], format_func=uf_label)
        city = st.selectbox("Cidade", cities_by_uf(uf))
        vt_per_day = st.number_input("VT por dia", min_value=0, value=0, step=1)
        work_schedule = st.selectbox("Expediente", ["SEG-SEX", "SEG-SAB"])

        st.markdown("**Dias presenciais**")
        days_selected = st.multiselect("", list(WEEKDAY_MAP.keys()), default=[])

        st.markdown("**Benefícios**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            benefit_vt = st.checkbox("VT")
        with c2:
            benefit_va_vr = st.checkbox("VA/VR")
        with c3:
            is_supervisor = st.checkbox("Supervisor(a)")
        with c4:
            homeoffice_choice = st.selectbox("Homeoffice", ["Sem", "A", "B"])

        benefit_homeoffice = 1 if homeoffice_choice != "Sem" else 0
        homeoffice_type = homeoffice_choice if homeoffice_choice in ["A", "B"] else "A"

        if st.button("💾 Salvar funcionário", type="primary"):
            if not name.strip() or not cpf.strip():
                flash("Nome e CPF são obrigatórios.", "error")
                st.rerun()
            else:
                pres_flags = {col: 0 for col, _ in WEEKDAY_MAP.values()}
                for label in days_selected:
                    col, _ = WEEKDAY_MAP[label]
                    pres_flags[col] = 1

                execute("""
                    INSERT INTO employees (
                        name, cpf, uf, city, vt_per_day, work_schedule,
                        pres_mon, pres_tue, pres_wed, pres_thu, pres_fri, pres_sat,
                        benefit_vt, benefit_va_vr, benefit_homeoffice, is_supervisor,
                        homeoffice_type, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'));
                """, (
                    name.strip(), cpf.strip(), uf, city, vt_per_day, work_schedule,
                    pres_flags["pres_mon"], pres_flags["pres_tue"], pres_flags["pres_wed"],
                    pres_flags["pres_thu"], pres_flags["pres_fri"], pres_flags["pres_sat"],
                    1 if benefit_vt else 0, 1 if benefit_va_vr else 0,
                    benefit_homeoffice, 1 if is_supervisor else 0, homeoffice_type
                ))
                flash("Funcionário salvo ✅", "success")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("Lista de Funcionários")

        rows = fetch_all("SELECT * FROM employees ORDER BY name;")

        if not rows:
            st.info("Nenhum funcionário cadastrado ainda.")
        else:
            def pres_days_str(r):
                labels = [day for day, (col, _) in WEEKDAY_MAP.items() if r[col]]
                return ", ".join(labels) or "—"

            display_rows = [{
                "Nome": r["name"],
                "CPF": r["cpf"],
                "UF": r["uf"],
                "Cidade": r["city"],
                "Expediente": r["work_schedule"] or "SEG-SEX",
                "VT/dia": r["vt_per_day"],
                "Presencial": pres_days_str(r),
                "VT": "Sim" if r["benefit_vt"] else "Não",
                "VA/VR": "Sim" if r["benefit_va_vr"] else "Não",
                "Homeoffice": "Sem" if not r["benefit_homeoffice"] else (r["homeoffice_type"] or "A").upper(),
                "Supervisor": "Sim" if r["is_supervisor"] else "Não",
                "ID": r["id"]
            } for r in rows]

            st.dataframe(display_rows, use_container_width=True, hide_index=True)

            st.divider()

            options = {f"{r['name']} | CPF: {r['cpf']} | ID: {r['id']}": r["id"] for r in rows}
            selected = st.selectbox("Editar / Excluir", list(options.keys()))
            emp_id = options[selected]
            emp = fetch_one("SELECT * FROM employees WHERE id = ?;", (emp_id,))
            emp_dict = dict(emp) if emp else {}

            with st.form("edit_employee"):
                new_name = st.text_input("Nome", value=emp_dict.get("name", ""))
                new_cpf = st.text_input("CPF", value=emp_dict.get("cpf", ""))
                new_uf = st.selectbox("UF", ["PE", "AL"],
                                      index=0 if emp_dict.get("uf") == "PE" else 1,
                                      format_func=uf_label)
                new_city_options = cities_by_uf(new_uf)
                new_city_index = new_city_options.index(emp_dict.get("city")) if emp_dict.get("city") in new_city_options else 0
                new_city = st.selectbox("Cidade", new_city_options, index=new_city_index)
                new_vt_day = st.number_input("VT por dia", value=int(emp_dict.get("vt_per_day", 0)))
                new_schedule = st.selectbox("Expediente", ["SEG-SEX", "SEG-SAB"],
                                            index=0 if emp_dict.get("work_schedule", "SEG-SEX") == "SEG-SEX" else 1)

                st.markdown("**Dias presenciais**")
                current_days = [k for k, (c, _) in WEEKDAY_MAP.items() if emp_dict.get(c, 0) == 1]
                new_days = st.multiselect("", list(WEEKDAY_MAP.keys()), default=current_days)

                st.markdown("**Benefícios**")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    new_vt = st.checkbox("VT", value=bool(emp_dict.get("benefit_vt", 0)))
                with c2:
                    new_va = st.checkbox("VA/VR", value=bool(emp_dict.get("benefit_va_vr", 0)))
                with c3:
                    new_sup = st.checkbox("Supervisor(a)", value=bool(emp_dict.get("is_supervisor", 0)))
                with c4:
                    idx_ho = ["Sem", "A", "B"].index(
                        "Sem" if not emp_dict.get("benefit_homeoffice") else (emp_dict.get("homeoffice_type", "A").upper())
                    )
                    new_ho = st.selectbox("Homeoffice", ["Sem", "A", "B"], index=idx_ho)

                if st.form_submit_button("💾 Salvar alterações", type="primary"):
                    pres = {c: 0 for c, _ in WEEKDAY_MAP.values()}
                    for d in new_days:
                        pres[WEEKDAY_MAP[d][0]] = 1

                    new_ho_val = 1 if new_ho != "Sem" else 0
                    new_ho_type = new_ho if new_ho in ["A", "B"] else "A"

                    execute("""
                        UPDATE employees SET
                            name=?, cpf=?, uf=?, city=?, vt_per_day=?, work_schedule=?,
                            pres_mon=?, pres_tue=?, pres_wed=?, pres_thu=?, pres_fri=?, pres_sat=?,
                            benefit_vt=?, benefit_va_vr=?, benefit_homeoffice=?, is_supervisor=?,
                            homeoffice_type=?, updated_at=datetime('now')
                        WHERE id=?;
                    """, (
                        new_name, new_cpf, new_uf, new_city, new_vt_day, new_schedule,
                        pres["pres_mon"], pres["pres_tue"], pres["pres_wed"],
                        pres["pres_thu"], pres["pres_fri"], pres["pres_sat"],
                        1 if new_vt else 0, 1 if new_va else 0,
                        new_ho_val, 1 if new_sup else 0, new_ho_type, emp_id
                    ))
                    flash("Alterações salvas ✅", "success")
                    st.rerun()

            st.warning("Exclusão é permanente.")
            if st.checkbox("Confirmo que quero excluir este funcionário"):
                if st.button("🗑️ Excluir funcionário"):
                    execute("DELETE FROM employees WHERE id = ?;", (emp_id,))
                    flash("Funcionário excluído ✅", "success")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

def page_quadro_mensal():
    require_login()
    st.header("📊 Quadro Mensal de Benefícios")

    today = dt.date.today()
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Ano", 2020, 2100, today.year)
    with col2:
        month = st.selectbox("Mês", range(1, 13), index=today.month - 1,
                             format_func=lambda m: calendar.month_name[m])

    config_row = fetch_one("SELECT * FROM config WHERE id = 1;")
    config = dict(config_row) if config_row else {}

    employees = fetch_all("SELECT * FROM employees ORDER BY name;")
    if not employees:
        st.info("Cadastre funcionários primeiro.")
        return

    results = []
    total_vt = total_va = total_ho = total_geral = 0.0

    for e in employees:
        e_dict = dict(e)
        uf = e_dict["uf"]
        city = e_dict["city"] or cities_by_uf(uf)[0]
        schedule = (e_dict["work_schedule"] or "SEG-SEX").upper()

        dias_uteis = count_work_days_by_schedule(city, year, month, schedule)
        pres = count_presential_days_with_schedule(e_dict, city, year, month)

        # ✅ férias descontam no mês selecionado
        vac_workdays, vac_pres_days = count_vacation_workdays(e_dict, city, year, month)
        dias_uteis_adj = max(dias_uteis - vac_workdays, 0)
        pres_adj = max(pres - vac_pres_days, 0)
        pres_adj = max(min(pres_adj, dias_uteis_adj), 0)

        vt_unit = float(config.get("vt_pe" if uf == "PE" else "vt_al", 0))
        va_unit = float(config.get("va_vr_pe" if uf == "PE" else "va_vr_al", 0))
        vt_sup = float(config.get("vt_fixo_supervisor_pe" if uf == "PE" else "vt_fixo_supervisor_al", 0))

        ho_type = (e_dict["homeoffice_type"] or "A").upper()
        ho_key = "homeoffice_pe" if uf == "PE" else "homeoffice_al"
        ho_key_b = ho_key + "_b"
        ho_unit = float(config.get(ho_key if ho_type == "A" else ho_key_b, 0))

        vt_d, va_d = get_benefit_deltas(e_dict["id"], year, month)

        vt_qty = 0
        if e_dict["benefit_vt"] and not e_dict["is_supervisor"]:
            vt_qty = int(e_dict.get("vt_per_day", 0)) * pres_adj

        va_days = dias_uteis_adj if e_dict["benefit_va_vr"] else 0

        vt_final = max(vt_qty + vt_d, 0)
        va_final = max(va_days + va_d, 0)

        vt_val = vt_sup if e_dict["is_supervisor"] and e_dict["benefit_vt"] else (vt_unit * vt_final)
        va_val = va_unit * va_final
        ho_val = ho_unit if e_dict["benefit_homeoffice"] else 0

        total = vt_val + va_val + ho_val

        total_vt += vt_val
        total_va += va_val
        total_ho += ho_val
        total_geral += total

        results.append({
            "Nome": e_dict["name"],
            "CPF": e_dict["cpf"],
            "UF": uf,
            "Cidade": city,
            "Expediente": schedule,
            "Férias (dias úteis)": vac_workdays,
            "Dias úteis": dias_uteis_adj,
            "Presencial": pres_adj,
            "VT (R$)": round(vt_val, 2),
            "VA/VR (R$)": round(va_val, 2),
            "Homeoffice (R$)": round(ho_val, 2),
            "Total (R$)": round(total, 2),
        })

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader(f"Resumo – {calendar.month_name[month]} {year}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💳 VT Total", money(total_vt))
        c2.metric("🍴 VA/VR Total", money(total_va))
        c3.metric("🏠 Home Office", money(total_ho))
        c4.metric("💰 Total Geral", money(total_geral))

        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("Detalhamento por Funcionário")
        st.dataframe(results, use_container_width=True, hide_index=True)

        st.download_button(
            "📥 Baixar CSV",
            to_csv_bytes(results),
            f"quadro_beneficios_{year}_{month:02d}.csv",
            "text/csv"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("Ajustes Manuais (lança em X → paga em X+1)")

        employees_list = fetch_all("SELECT id, name, cpf FROM employees ORDER BY name;")
        emp_options = {f"{e['name']} | CPF: {e['cpf']}": e["id"] for e in employees_list}
        selected_emp = st.selectbox("Funcionário", list(emp_options.keys()), key="adj_emp")
        emp_id = emp_options[selected_emp]

        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            adj_date = st.date_input("Data do ajuste", dt.date.today())
        with col2:
            vt_delta = st.number_input("VT Δ", value=0, step=1)
        with col3:
            va_delta = st.number_input("VA Δ", value=0, step=1)

        note = st.text_input("Observação (opcional)")
        pay_m = next_month_ym(adj_date)
        st.caption(f"Esse ajuste entra no pagamento de **{pay_m}**")

        if st.button("💾 Registrar ajuste", type="primary"):
            execute("""
                INSERT INTO benefit_day_adjustments
                (employee_id, date, vt_delta, va_delta, note, pay_month)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (emp_id, adj_date.isoformat(), int(vt_delta), int(va_delta), note or None, pay_m))
            flash("Ajuste salvo ✅", "success")
            st.rerun()

        deltas = list_benefit_deltas(emp_id, year, month)
        if deltas:
            st.dataframe(
                [{
                    "Data": d["date"],
                    "VT Δ": d["vt_delta"],
                    "VA Δ": d["va_delta"],
                    "Obs": d["note"] or "",
                    "ID": d["id"]
                } for d in deltas],
                use_container_width=True, hide_index=True
            )

            del_id = st.selectbox("Excluir ajuste", [d["id"] for d in deltas])
            if st.button("🗑️ Excluir ajuste selecionado"):
                execute("DELETE FROM benefit_day_adjustments WHERE id = ?;", (del_id,))
                flash("Ajuste removido ✅", "success")
                st.rerun()
        else:
            st.info("Nenhum ajuste para este funcionário neste mês de pagamento.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ✅ NOVO: Lançamento de férias
    with st.container():
        st.markdown('<div class="ws-card">', unsafe_allow_html=True)
        st.subheader("🌴 Lançamento de Férias (desconta no mês selecionado)")

        employees_list2 = fetch_all("SELECT id, name, cpf FROM employees ORDER BY name;")
        emp_options2 = {f"{e['name']} | CPF: {e['cpf']}": e["id"] for e in employees_list2}
        selected_emp2 = st.selectbox("Funcionário (Férias)", list(emp_options2.keys()), key="vac_emp")
        emp_id2 = emp_options2[selected_emp2]

        c1, c2 = st.columns(2)
        with c1:
            vac_start = st.date_input("Início das férias", value=dt.date(year, month, 1), key="vac_start")
        with c2:
            vac_end = st.date_input("Fim das férias", value=dt.date(year, month, 1), key="vac_end")

        vac_note = st.text_input("Observação (opcional)", key="vac_note")

        if st.button("💾 Registrar férias", type="primary", key="btn_vac_save"):
            if vac_end < vac_start:
                flash("A data final não pode ser menor que a inicial.", "error")
                st.rerun()

            execute("""
                INSERT INTO vacations (employee_id, start_date, end_date, note)
                VALUES (?, ?, ?, ?);
            """, (emp_id2, vac_start.isoformat(), vac_end.isoformat(), vac_note or None))

            flash("Férias registradas! Já desconta no mês selecionado ✅", "success")
            st.rerun()

        st.divider()
        st.caption("Férias registradas para este funcionário:")

        vacs = list_vacations(emp_id2)
        if vacs:
            st.dataframe(
                [{"ID": v["id"], "Início": v["start_date"], "Fim": v["end_date"], "Obs": v["note"] or ""} for v in vacs],
                use_container_width=True,
                hide_index=True
            )

            del_vac_id = st.selectbox("Excluir lançamento de férias", [v["id"] for v in vacs], key="del_vac_id")
            if st.button("🗑️ Excluir férias selecionada", key="btn_vac_del"):
                execute("DELETE FROM vacations WHERE id = ?;", (del_vac_id,))
                flash("Lançamento de férias excluído ✅", "success")
                st.rerun()
        else:
            st.info("Nenhuma férias cadastrada para este funcionário.")

        st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────
#                   ROUTER
# ────────────────────────────────────────────────
if current_page == "login":
    page_login()
elif current_page == "config":
    page_config()
elif current_page == "employees":
    page_employees()
elif current_page == "quadro":
    page_quadro_mensal()