import streamlit as st
import json
import random
import math
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

# ========================== CORE ENGINE ==========================
class VirtualLabCore:
    def __init__(self, student_id: str, student_name: str, school_id: str, grade: str):
        self.student_id = student_id
        self.student_name = student_name
        self.school_id = school_id
        self.grade = grade
        self.progress: Dict[str, list] = {"physics": [], "chemistry": [], "biology": [], "maths": []}
        self.session_start = datetime.now()

    def _apply_real_world_error(self, theoretical: float, min_var: float = 2.0, max_var: float = 5.0) -> float:
        variance = random.uniform(min_var, max_var)
        sign = random.choice([-1, 1])
        return max(theoretical + theoretical * (variance / 100.0) * sign, 0.0)

    def record_experiment(self, subject: str, topic: str, user_inputs: Dict, 
                         observed: float, theoretical: float, notes: str = ""):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "user_inputs": user_inputs,
            "observed": round(observed, 4),
            "theoretical": round(theoretical, 4),
            "percentage_error": round(abs((observed - theoretical) / theoretical * 100), 2) if theoretical != 0 else 0,
            "notes": notes
        }
        self.progress[subject].append(entry)

    def generate_teacher_report(self) -> Dict:
        report = {
            "student_name": self.student_name,
            "student_id": self.student_id,
            "school_id": self.school_id,
            "grade": self.grade,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_experiments": sum(len(v) for v in self.progress.values()),
            "subjects": {}
        }
        for sub, exps in self.progress.items():
            if exps:
                avg_err = sum(e["percentage_error"] for e in exps) / len(exps)
                report["subjects"][sub] = {"count": len(exps), "avg_error_%": round(avg_err, 2)}
        return report


# ========================== LABS ==========================
class PhysicsLab:
    def __init__(self, core): self.core = core

    def density(self, mass: float, volume: float):
        theo = mass / volume
        obs = self.core._apply_real_world_error(theo)
        self.core.record_experiment("physics", "Density", {"mass_g": mass, "volume_cm3": volume}, obs, theo)
        return {"observed": obs, "theoretical": theo, "unit": "g/cm³"}

    def hookes_law(self, force: float, extension: float):
        theo_k = force / extension
        obs_k = self.core._apply_real_world_error(theo_k)
        self.core.record_experiment("physics", "Hooke's Law", {"force_N": force, "extension_m": extension}, obs_k, theo_k)
        return {"observed_k": obs_k, "theoretical_k": theo_k, "unit": "N/m"}

    def specific_heat(self, mass: float, delta_t: float, energy: float):
        theo = energy / (mass * delta_t)
        obs = self.core._apply_real_world_error(theo)
        self.core.record_experiment("physics", "Specific Heat Capacity", 
                                  {"mass_kg": mass, "ΔT": delta_t, "energy_J": energy}, obs, theo)
        return {"observed": obs, "theoretical": theo, "unit": "J/kg°C"}

class ChemistryLab:
    def __init__(self, core): self.core = core

    def titration(self, acid_vol: float, acid_conc: float, base_conc: float):
        theo = (acid_vol * acid_conc) / base_conc
        obs = self.core._apply_real_world_error(theo, 1.5, 4.0)
        self.core.record_experiment("chemistry", "Acid-Base Titration", 
                                  {"acid_vol": acid_vol, "acid_M": acid_conc, "base_M": base_conc}, obs, theo)
        return {"observed_vol": obs, "theoretical_vol": theo, "unit": "cm³"}

    def reaction_rate(self, temp: float, conc: float):
        theo = 0.02 * conc * math.exp(0.07 * (temp - 25))
        obs = self.core._apply_real_world_error(theo)
        self.core.record_experiment("chemistry", "Reaction Rate (Mass Loss)", {"temp": temp, "conc": conc}, obs, theo)
        return {"observed_rate": obs, "theoretical_rate": theo, "unit": "g/s"}

class BiologyLab:
    def __init__(self, core): self.core = core

    def osmosis(self, initial_mass: float, conc_diff: float):
        theo = -12.5 * conc_diff
        obs = self.core._apply_real_world_error(theo, 3.0, 7.0)
        self.core.record_experiment("biology", "Osmosis", {"initial_mass": initial_mass, "conc_diff": conc_diff}, obs, theo)
        return {"observed_%change": obs, "theoretical_%change": theo}

class MathsLab:
    def __init__(self, core): self.core = core

    def pythagoras(self, a: float, b: float):
        c_theo = math.sqrt(a**2 + b**2)
        c_obs = self.core._apply_real_world_error(c_theo, 1.0, 3.0)
        self.core.record_experiment("maths", "Pythagoras Theorem", {"a": a, "b": b}, c_obs, c_theo)

        fig = go.Figure()
        fig.add_shape(type="rect", x0=0, y0=0, x1=a, y1=a, fillcolor="lightblue", opacity=0.6, line=dict(color="blue"))
        fig.add_shape(type="rect", x0=a, y0=0, x1=a+b, y1=b, fillcolor="lightgreen", opacity=0.6, line=dict(color="green"))
        fig.add_trace(go.Scatter(x=[0, a, a, 0], y=[0, 0, b, b], mode="lines+markers", 
                                line=dict(color="red", width=4), name="Triangle"))
        fig.update_layout(title="a² + b² = c² — Visual Proof", 
                         xaxis_range=[-1, a+b+2], yaxis_range=[-1, max(a,b)+2], height=500)
        return {"observed_c": c_obs, "theoretical_c": c_theo, "figure": fig}

    def quadratic(self, a: float, b: float, c: float):
        disc = b**2 - 4*a*c
        if disc < 0: return {"error": "No real roots"}
        r1 = (-b + math.sqrt(disc)) / (2*a)
        r2 = (-b - math.sqrt(disc)) / (2*a)
        obs1 = self.core._apply_real_world_error(r1)
        obs2 = self.core._apply_real_world_error(r2)
        self.core.record_experiment("maths", "Quadratic Equation", {"a":a,"b":b,"c":c}, obs1, r1)

        x = [i/10 for i in range(-100, 101)]
        y = [a*xi**2 + b*xi + c for xi in x]
        fig = px.line(x=x, y=y, title="Quadratic Function")
        fig.add_vline(x=obs1, line_dash="dash", annotation_text="Observed Root 1")
        fig.add_vline(x=obs2, line_dash="dash", annotation_text="Observed Root 2", annotation_position="bottom right")
        return {"observed_roots": [obs1, obs2], "theoretical_roots": [r1,r2], "figure": fig}


# ========================== STREAMLIT APP ==========================
st.set_page_config(page_title="LETS'ELA NYAKALLO", layout="wide", page_icon="🔬")

st.title("🔬 LETS'ELA NYAKALLO AI Virtual Lab")
st.markdown("**Realistic IGCSE Lab Simulations with 2–5% Measurement Error**")

# Sidebar
with st.sidebar:
    st.header("Student Profile")
    name = st.text_input("Name", "Thabo Mokoena")
    sid = st.text_input("Student ID", "STU2026001")
    school = st.text_input("School ID", "SCH001")
    grade = st.selectbox("Grade", ["IGCSE Year 1", "IGCSE Year 2", "A-Level"])

    if st.button("New Session"):
        st.session_state.core = VirtualLabCore(sid, name, school, grade)
        st.success("Session started!")

if "core" not in st.session_state:
    st.session_state.core = VirtualLabCore(sid, name, school, grade)

core = st.session_state.core
physics = PhysicsLab(core)
chemistry = ChemistryLab(core)
biology = BiologyLab(core)
maths = MathsLab(core)

tab_home, tab_p, tab_c, tab_b, tab_m, tab_r = st.tabs([
    "🏠 Home", "🧪 Physics", "🧪 Chemistry", "🧬 Biology", "📐 Mathematics", "📊 Report"
])

with tab_home:
    st.info("Welcome to the Virtual AI Laboratory. Select a subject tab above to begin your experiments.")
    st.markdown("### Recent Activity")
    st.write(core.generate_teacher_report())

# ========================== PHYSICS TAB ==========================
with tab_p:
    st.subheader("Physics Lab")
    choice = st.selectbox("Physics Experiment", ["Density", "Hooke's Law", "Specific Heat Capacity"])
    
    if choice == "Density":
        col1, col2 = st.columns(2)
        m = col1.number_input("Mass (g)", 50.0)
        v = col2.number_input("Volume (cm³)", 20.0)
        if st.button("Run Density Experiment"):
            r = physics.density(m, v)
            st.success(f"Observed: **{r['observed']:.4f}** {r['unit']}")
            st.info(f"Theoretical: {r['theoretical']:.4f} {r['unit']}")
            
    elif choice == "Hooke's Law":
        col1, col2 = st.columns(2)
        f = col1.number_input("Force (N)", 10.0)
        ext = col2.number_input("Extension (m)", 0.2)
        if st.button("Test Spring Constant"):
            r = physics.hookes_law(f, ext)
            st.success(f"Observed Spring Constant (k): **{r['observed_k']:.4f}** {r['unit']}")
            st.info(f"Theoretical (k): {r['theoretical_k']:.4f} {r['unit']}")

    elif choice == "Specific Heat Capacity":
        col1, col2, col3 = st.columns(3)
        mass_kg = col1.number_input("Mass (kg)", 1.0)
        dt = col2.number_input("Temperature Change (°C)", 10.0)
        energy = col3.number_input("Energy Supplied (J)", 42000.0)
        if st.button("Calculate Specific Heat"):
            r = physics.specific_heat(mass_kg, dt, energy)
            st.success(f"Observed Heat Capacity (c): **{r['observed']:.2f}** {r['unit']}")
            st.info(f"Theoretical (c): {r['theoretical']:.2f} {r['unit']}")


# ========================== CHEMISTRY TAB ==========================
with tab_c:
    st.subheader("Chemistry Lab")
    c_choice = st.selectbox("Chemistry Experiment", ["Acid-Base Titration", "Reaction Rate (Mass Loss)"])
    
    if c_choice == "Acid-Base Titration":
        col1, col2, col3 = st.columns(3)
        a_vol = col1.number_input("Acid Volume (cm³)", 25.0)
        a_conc = col2.number_input("Acid Concentration (M)", 0.1)
        b_conc = col3.number_input("Base Concentration (M)", 0.1)
        if st.button("Perform Titration"):
            r = chemistry.titration(a_vol, a_conc, b_conc)
            st.success(f"Observed Titre Volume: **{r['observed_vol']:.2f}** {r['unit']}")
            st.info(f"Theoretical Volume: {r['theoretical_vol']:.2f} {r['unit']}")
            
    elif c_choice == "Reaction Rate (Mass Loss)":
        col1, col2 = st.columns(2)
        temp = col1.number_input("Temperature (°C)", 30.0)
        conc = col2.number_input("Concentration (M)", 1.0)
        if st.button("Measure Reaction Rate"):
            r = chemistry.reaction_rate(temp, conc)
            st.success(f"Observed Reaction Rate: **{r['observed_rate']:.5f}** {r['unit']}")
            st.info(f"Theoretical Rate: {r['theoretical_rate']:.5f} {r['unit']}")


# ========================== BIOLOGY TAB ==========================
with tab_b:
    st.subheader("Biology Lab")
    b_choice = st.selectbox("Biology Experiment", ["Osmosis"])
    
    if b_choice == "Osmosis":
        col1, col2 = st.columns(2)
        i_mass = col1.number_input("Initial Mass of Tissue (g)", 5.0)
        c_diff = col2.number_input("Concentration Difference (M)", 0.5)
        if st.button("Observe Osmosis"):
            r = biology.osmosis(i_mass, c_diff)
            st.success(f"Observed Mass Change: **{r['observed_%change']:.2f}%**")
            st.info(f"Theoretical Mass Change: {r['theoretical_%change']:.2f}%")


# ========================== MATHEMATICS TAB ==========================
with tab_m:
    st.subheader("Mathematics Lab")
    mchoice = st.selectbox("Mathematics Topic", ["Pythagoras Theorem (Visual)", "Quadratic Equation"])
    
    if mchoice == "Pythagoras Theorem (Visual)":
        col1, col2 = st.columns(2)
        a = col1.number_input("Side a", value=3.0)
        b = col2.number_input("Side b", value=4.0)
        if st.button("Perform Measurement"):
            res = maths.pythagoras(a, b)
            st.plotly_chart(res["figure"], use_container_width=True)
            st.success(f"Observed Hypotenuse: **{res['observed_c']:.3f} cm**")
            st.info(f"Theoretical: {res['theoretical_c']:.3f} cm")
            
    elif mchoice == "Quadratic Equation":
        col1, col2, col3 = st.columns(3)
        a_q = col1.number_input("Coefficient a", value=1.0)
        b_q = col2.number_input("Coefficient b", value=-5.0)
        c_q = col3.number_input("Constant c", value=6.0)
        if st.button("Solve & Plot Roots"):
            res = maths.quadratic(a_q, b_q, c_q)
            if "error" in res:
                st.error(res["error"])
            else:
                st.plotly_chart(res["figure"], use_container_width=True)
                st.success(f"Observed Roots: **{res['observed_roots'][0]:.3f}**, **{res['observed_roots'][1]:.3f}**")
                st.info(f"Theoretical Roots: {res['theoretical_roots'][0]:.3f}, {res['theoretical_roots'][1]:.3f}")


# ========================== REPORT TAB ==========================
with tab_r:
    st.subheader("Teacher Dashboard & Export")
    report = core.generate_teacher_report()
    
    st.json(report)
    
    # Optional: Download button for the JSON report
    report_json = json.dumps(report, indent=4)
    st.download_button(
        label="Download Report as JSON",
        file_name=f"{core.student_id}_report.json",
        mime="application/json",
        data=report_json
    )

st.caption("LETS'ELA NYAKALLO © 2026 | Designed for authentic IGCSE preparation with real-world experimental error.")
