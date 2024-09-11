#pip install rsconnect-python
#会生成新的文件rsconnect deploy shiny -n xjtlu-wlap . -N
#rsconnect deploy shiny -n xjtlu-wlap .
#旧的rsconnect add --account xjtlu-wlap --name xjtlu-wlap --token 953A2E50A81FD422F4A8A7C474176894 --secret Q7KpgHjoBwKqWndcvgJo01w6BpVOdIcShhjDiDEf
#新的rsconnect add --account xjtlu-wlap --name xjtlu-wlap --token C279352AEB06D5E63AEEFD557F50219F --secret fnXextVNOVeDC84y1zphV7btub9q6PPOrkdFKBpf
#好像不能成功rsconnect deploy "D:\Desktop\TB Transmission" --name xjtlu-wlap --title TB_Transmission
import pandas as pd
import matplotlib.pyplot as plt 
import asyncio
import io

from functools import partial
from shiny.ui import page_navbar
from shiny.express import ui, input, output
from shiny import render, reactive, App


ui.page_opts(
    title="TB Transmission Simulation",  
    page_fn=partial(page_navbar, id="page"), 
    fillable=True 
    )

with ui.nav_panel("Introduction"):
    @reactive.effect
    def _():
        m = ui.modal(
            ui.markdown(
                """
                Here are four pages within this Shiny APP \n
                Introduction: About Our Model for Simulation \n 
                Simulation: Panel to Simulate \n 
                Data table: Generated after Simulation \n 
                About us: Project and Team Informations
                """),
            title=ui.h3("Welcome Visit SURF-2024-0177",ui.HTML("&#128075;")),
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)

    ui.h3('Overview of the model')
    ui.markdown("""
                The model is used to simulate the spread of Mycobacterium tuberculosis (Mtb) in spatially and age-structured populations and was developed to simulate Mtb transmission. The population of individuals simulated by the model is designed based on demographics and initial state structure, and then a network of links between individuals is established. After establishing the population, the model iterates over unit discrete time steps (e.g., one week) to simulate the spread of Mtb in the population. Our model requires several rate parameters to describe the rate at which infected individuals transition between disease states (see 'Rate parameters of status transformation')
                """)
    ui.markdown("""
                At the beginning of each time step, our model will update the disease status of the infected individual based on the transition probabilities inferred from these ratios, and then calculate, based on the relevant formula (see 'Probability of status transformation'), the transition of the susceptible individual from disease state m to the the probability of disease state n. Ultimately, the probability of infection of a susceptible individual (studying at school or working in a workplace) when in contact with an infected individual (i.e., an individual in a subclinical or clinical disease state) can be calculated for each unit time step.
                """)

    with ui.layout_columns():
        with ui.card(height='300px'):
                ui.card_header('Diagram of status transformation')
                @render.image
                def image1():
                    from pathlib import Path

                    dir = Path("D:\Desktop\TB Transmission\Status.png").resolve().parent
                    img1 = {"src": str(dir / "Status.png"), "width": "700px"}
                    return img1
                
                
       

    with ui.layout_columns(fill=True):         
        with ui.card(height='100px',fill=True):
            ui.card_header('Probability of status transformation')
            @render.image
            def image2():
                from pathlib import Path

                dir = Path("D:\Desktop\TB Transmission\probability.png").resolve().parent
                img2 = {"src": str(dir / "probability.png"), "width": "330px"}
                return img2
           

        with ui.card(height='400px',fill=True):
            ui.card_header('Rate parameters of status transformation')
            @render.image
            def image3():
                from pathlib import Path

                dir = Path("D:\Desktop\TB Transmission\parameters.png").resolve().parent
                img3 = {"src": str(dir / "parameters.png"), "width": "360px"}
                return img3
            
   
    
    
    


    
    
    

with ui.nav_panel("Simulation"):  
    with ui.layout_sidebar():
        with ui.sidebar(bg=""):  
            ui.input_dark_mode(mode="light") # << 
            ui.input_numeric("population", "Total Population (Max. 10M)", value='', min=100, max=10000000),
            ui.input_numeric("initial_infected", "Initial Infection (Max. 10M)", value='', min=1, max=10000000),
            ui.input_numeric("infection_rate", "Infection Rate", value='', min=0.001, max=1.0, step=0.01),
            ui.input_numeric("initial_minimal", "Initial Minimal (Max. 10M)", value='', min=1, max=10000000),
            ui.input_numeric("initial_subclinical", "Initial Subclinical (Max. 10M)", value='', min=1, max=10000000),
            ui.input_numeric("initial_clinical", "Initial Clinical (Max. 10M)", value='', min=1, max=100000000),
            ui.input_numeric("simulation_days", "Simulation Days (Max. 10Yrs)", value='', min=1, max=3650),
            ui.input_action_button("simulate", "Simulation")

        ui.h4('Enter the user defined value', ui.HTML("&#128075;"))

        

        @render.ui
        @reactive.event(input.simulate)
        async def compute():
            with ui.Progress(min=1, max=10) as p:
                p.set(message="Simulation in progress", detail="This may take a while...")

                for i in range(1, 10):
                    p.set(i, message="Simulating")
                    await asyncio.sleep(0.1)

            return "Done Simulating!"

        @render.plot
        def plot():
            # Check if the button has been clicked
            if not input.simulate():
                return

            # Get input values
            population = input.population()
            initial_infected = input.initial_infected()
            infection_rate = input.infection_rate()
            initial_minimal = input.initial_minimal()
            initial_subclinical = input.initial_subclinical()
            initial_clinical = input.initial_clinical()
            simulation_days = input.simulation_days()


            # Simulate virus transmission
            itom = 0.09516
            itosub = 0.03921
            itor = 0.83958
            mtor = 0.16472
            subtom = 0.73815
            subtoc = 0.13929
            ctod = 0.28107
            rtos = 0.58104
            susceptible = population - initial_infected - initial_minimal - initial_subclinical - initial_clinical
            infected = initial_infected
            minimal = initial_minimal
            subclinical = initial_subclinical
            clinical = initial_clinical
            recovered = 0
            death = 0

            susceptible_history = []
            infected_history = []
            minimal_history = []
            subclinical_history = []
            clinical_history = []
            recovered_history = []
            death_history = []
            population_history=[]

            for _ in range(simulation_days):
                new_susceptible = max(0, int(recovered * rtos))
                new_infected = max(0,int(infection_rate * (((infected+minimal+subclinical+clinical) * susceptible) / population)))
                new_minimal =max(0, int(itom * infected + subtom * subclinical))
                new_subclinical = max(0,int(itosub * infected))
                new_clinical =max(0, int(subtoc * subclinical))
                new_recovered = max(0,int(itor * infected + mtor * minimal))
                new_death =max(0, int(ctod * clinical))

                susceptible = max(0, int(susceptible - new_infected + new_susceptible))
                infected = max(0, int(infected + new_infected - (new_minimal * (itom / (subtom + itom))) - (new_recovered * (itor / (mtor + itor))) - new_subclinical))
                minimal = max(0, int(minimal + new_minimal - (new_recovered * (mtor / (mtor + itor)))))
                subclinical = max(0, int(subclinical + new_subclinical - new_clinical - (new_minimal * (subtom / (subtom + itom)))))
                clinical = max(0, int(clinical + new_clinical - new_death))
                recovered = max(0, int(recovered + new_recovered - new_susceptible))
                death = max(0, int(death + new_death))


                susceptible_history.append(susceptible)
                infected_history.append(infected)
                minimal_history.append(minimal)
                subclinical_history.append(subclinical)
                clinical_history.append(clinical)
                recovered_history.append(recovered)
                death_history.append(death)

            # Plot results
            fig, ax = plt.subplots()
            ax.plot(susceptible_history, label='Susceptible')
            ax.plot(infected_history, label='Infection')
            ax.plot(minimal_history, label='Minimal')
            ax.plot(subclinical_history, label='Subclinical')
            ax.plot(clinical_history, label='Clinical')
            ax.plot(recovered_history, label='Recovered')
            ax.plot(death_history, label='Death')
            ax.set_xlabel('Days')
            ax.set_ylabel('Population')
            ax.legend()
            ax.set_title('TB Transmission Simulation')

            return fig
        
        @render.download(label='Download Plot', filename='TB_Simulation.png')
        def download_plot():
           
           # Get input values
            population = input.population()
            initial_infected = input.initial_infected()
            infection_rate = input.infection_rate()
            initial_minimal = input.initial_minimal()
            initial_subclinical = input.initial_subclinical()
            initial_clinical = input.initial_clinical()
            simulation_days = input.simulation_days()


            # Simulate virus transmission
            itom = 0.09516
            itosub = 0.03921
            itor = 0.83958
            mtor = 0.16472
            subtom = 0.73815
            subtoc = 0.13929
            ctod = 0.28107
            rtos = 0.58104
            susceptible = population - initial_infected - initial_minimal - initial_subclinical - initial_clinical
            infected = initial_infected
            minimal = initial_minimal
            subclinical = initial_subclinical
            clinical = initial_clinical
            recovered = 0
            death = 0

            susceptible_history = []
            infected_history = []
            minimal_history = []
            subclinical_history = []
            clinical_history = []
            recovered_history = []
            death_history = []
            population_history=[]

            for _ in range(simulation_days):
                new_susceptible = max(0, int(recovered * rtos))
                new_infected = max(0,int(infection_rate * (((infected+minimal+subclinical+clinical) * susceptible) / population)))
                new_minimal =max(0, int(itom * infected + subtom * subclinical))
                new_subclinical = max(0,int(itosub * infected))
                new_clinical =max(0, int(subtoc * subclinical))
                new_recovered = max(0,int(itor * infected + mtor * minimal))
                new_death =max(0, int(ctod * clinical))

                susceptible = max(0, int(susceptible - new_infected + new_susceptible))
                infected = max(0, int(infected + new_infected - (new_minimal * (itom / (subtom + itom))) - (new_recovered * (itor / (mtor + itor))) - new_subclinical))
                minimal = max(0, int(minimal + new_minimal - (new_recovered * (mtor / (mtor + itor)))))
                subclinical = max(0, int(subclinical + new_subclinical - new_clinical - (new_minimal * (subtom / (subtom + itom)))))
                clinical = max(0, int(clinical + new_clinical - new_death))
                recovered = max(0, int(recovered + new_recovered - new_susceptible))
                death = max(0, int(death + new_death))

                susceptible_history.append(susceptible)
                infected_history.append(infected)
                minimal_history.append(minimal)
                subclinical_history.append(subclinical)
                clinical_history.append(clinical)
                recovered_history.append(recovered)
                death_history.append(death)
                

            # Plot results
            fig, ax = plt.subplots()
            ax.plot(susceptible_history, label='Susceptible')
            ax.plot(infected_history, label='Infection')
            ax.plot(minimal_history, label='Minimal')
            ax.plot(subclinical_history, label='Subclinical')
            ax.plot(clinical_history, label='Clinical')
            ax.plot(recovered_history, label='Recovered')
            ax.plot(death_history, label='Death')
            ax.set_xlabel('Days')
            ax.set_ylabel('Population')
            ax.legend()
            ax.set_title('TB Transmission Simulation')
           
            if fig is None:
                return
            
            with io.BytesIO() as buf:
                plt.savefig(buf, format="png")
                yield buf.getvalue()
        
  

with ui.nav_panel("Data Table"):  
    with ui.layout_columns():  
        with ui.card():  
            ui.h4("Here is the data table after your simulation ", ui.HTML("&#128075;"))
            @render.data_frame
            def table():
                # Check if the button has been clicked
                if not input.simulate():
                    return pd.DataFrame()
                
                # Get input values
                population = input.population()
                initial_infected = input.initial_infected()
                infection_rate = input.infection_rate()
                initial_minimal = input.initial_minimal()
                initial_subclinical = input.initial_subclinical()
                initial_clinical = input.initial_clinical()
                simulation_days = input.simulation_days()


                # Simulate virus transmission
                itom = 0.09516
                itosub = 0.03921
                itor = 0.83958
                mtor = 0.16472
                subtom = 0.73815
                subtoc = 0.13929
                ctod = 0.28107
                rtos = 0.58104
                susceptible = population - initial_infected - initial_minimal - initial_subclinical - initial_clinical
                infected = initial_infected
                minimal = initial_minimal
                subclinical = initial_subclinical
                clinical = initial_clinical
                recovered = 0
                death = 0

                susceptible_history = []
                infected_history = []
                minimal_history = []
                subclinical_history = []
                clinical_history = []
                recovered_history = []
                death_history = []
                

                for _ in range(simulation_days):
                    new_susceptible = max(0, int(recovered * rtos))
                    new_infected = max(0,int(infection_rate * (((infected+minimal+subclinical+clinical) * susceptible) / population)))
                    new_minimal =max(0, int(itom * infected + subtom * subclinical))
                    new_subclinical = max(0,int(itosub * infected))
                    new_clinical =max(0, int(subtoc * subclinical))
                    new_recovered = max(0,int(itor * infected + mtor * minimal))
                    new_death =max(0, int(ctod * clinical))

                    susceptible = max(0, int(susceptible - new_infected + new_susceptible))
                    infected = max(0, int(infected + new_infected - (new_minimal * (itom / (subtom + itom))) - (new_recovered * (itor / (mtor + itor))) - new_subclinical))
                    minimal = max(0, int(minimal + new_minimal - (new_recovered * (mtor / (mtor + itor)))))
                    subclinical = max(0, int(subclinical + new_subclinical - new_clinical - (new_minimal * (subtom / (subtom + itom)))))
                    clinical = max(0, int(clinical + new_clinical - new_death))
                    recovered = max(0, int(recovered + new_recovered - new_susceptible))
                    death = max(0, int(death + new_death))
                   

                    susceptible_history.append(susceptible)
                    infected_history.append(infected)
                    minimal_history.append(minimal)
                    subclinical_history.append(subclinical)
                    clinical_history.append(clinical)
                    recovered_history.append(recovered)
                    death_history.append(death)
                  
                

                # Create a DataFrame to display the data
                data = {
                    "Days": list(range(1, simulation_days + 1)),
                    "Susceptible": susceptible_history,
                    "Infection": infected_history,
                    "Minimal": minimal_history,
                    "Subclinical": subclinical_history,
                    "Clinical": clinical_history,
                    "Recovered": recovered_history,
                    "Death": death_history,
                 
                }
                df = pd.DataFrame(data)
                return df
            
        
            
            

        
                
with ui.nav_panel("About Us"):
    with ui.layout_columns(height='80px'):
        
            @render.image
            def image4():
                from pathlib import Path

                dir = Path("D:\Desktop\TB Transmission\wlap.png").resolve().parent
                img4 = {"src": str(dir / "wlap.png"),"hight":"300px", "width": "300px"}
                return img4
        
            @render.image
            def image5():
                from pathlib import Path

                dir = Path("D:\Desktop\TB Transmission\SURFlogo.png").resolve().parent
                img5 = {"src": str(dir / "SURFlogo.png"), "hight":"300px","width": "250px"}
                return img5

            
    with ui.layout_columns():
        with ui.card():
            ui.h4('Principal Invesigator: Dr. Tenglong Li')
            ui.h5('Co-investigator: Mingming Chen, PhD')
            ui.markdown(
                """
                Team Members:\n
                Qinghao Meng, Bsc Biomedical Statistics\n
                Zixuan Qiu, Bsc Financial Mathematics\n
                Zihan Wang, Bsc Biomedical Statistics\n
                """)
           

    with ui.layout_columns():
        with ui.card(fill=True):
            ui.card_header("XJTLU Wisdom Lake Academy of Pharmacy", href="https://www.xjtlu.edu.cn/en/study/departments/academy-of-pharmacy", target="_blank")
            ui.markdown("""
                        Suzhou will be the site of a large biopharmaceutical ecosystem, featuring leading global pharmaceutical companies, premier healthcare providers, and world-class academic forums. The goal is to build, within 10 years, a Pharma Valley of China – a globally recognised, influential and best-in-class industry landmark in China. It is under this strategic background that Xi’an Jiaotong-Liverpool University and Suzhou Industrial Park government co-founded the XJTLU Wisdom Lake Academy of Pharmacy on 11 November 2020. In addition to the university-industry partnership, the Academy of Pharmacy added the notion of society to create a society-university-industry ecosystem, as an innovative and practice-based exploration of the national strategy. The University is able to take advantage of its multi-disciplinary expertise and global connectivity in building an academically rigorous Academy of Pharmacy that is uniquely positioned to train high-quality, internationally minded talents. Consequently, the Academy was proposed as part of the plan to execute this strategy. Recognised as the catalyst and enabler for building a first-rate and sustainable society-university-industry ecosystem, the Academy has reached full agreement with other parties in the ecosystem, and endeavours to help transform Suzhou into a world-class biopharmaceutical and healthcare hub by aligning its strategic positioning with the goal of the Pharma Valley of China.
                        """)
            ui.a("XJTLU Wisdom Lake Academy of Pharmacy", href="https://www.xjtlu.edu.cn/en/study/departments/academy-of-pharmacy", target="_blank")

        with ui.card(fill=True):
            ui.card_header('SURF-2024-0177')
            
            
            ui.markdown("""
                        We developed a Shiny-based interactive TB transmission simulation tool to help researchers and public health policy makers better understand and predict TB transmission dynamics for more effective control strategies through learning from Shiny development, systematic literature review, and evaluation and calibration of model parameters using GBD and WHO data
                        """)
    
    

