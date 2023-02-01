import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import lxml
import plotly.graph_objects as go
import plotly.express as px
import html5lib

from PIL import Image

logo_let = Image.open('data//C-La.png')
logo_ic = Image.open('data//C-L5.png')
st.set_page_config(page_title="ClutchWare-Player",page_icon=logo_ic)
Select_Pos=['PG','SG','SF','PF','C']
Select_Stat=['PTS','TRB','AST','3P','STL','BLK','TOV']
Write_Player = ""
Select_Last_Games = [10]
Write_Bt_Line=0
Select_OPP=["Atlanta Hawks","Brooklyn Nets","Boston Celtics","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets",
        "Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat",
        "Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns",
        "Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]
Select_Opti = ['Adam','Adadelta','Adagrad','Adamax','Nadam','Ftrl','RMSprop']

st.image(logo_let)

st.header("Player Analyzer")
st.markdown("Artificial Intelligence NBA Player Prop Predictor")
st.caption('Created by @maldonavi  &  @Guiller0701')



Player_nm=st.sidebar.text_input("Player Name", Write_Player)
Opp_Percentage=st.sidebar.multiselect('VS.',Select_OPP)
Pos=st.sidebar.multiselect('Position',Select_Pos)
Prop_in=st.sidebar.multiselect('Prop',Select_Stat)
Last_n_Games_b=st.sidebar.text_input('Last Games',10)
Bt_line=st.sidebar.text_input("Bet Line")
opt= st.sidebar.multiselect("Optimizer",Select_Opti,"Adam")
Last_n_Games=np.dot(Last_n_Games_b, -1)
def Extraer_nombre(cadena, n1=5, n2=2):
    esp = Player_nm.index(' ')
    return cadena[esp + 1:esp + n1 + 1] + cadena[:n2]
def Extraer_inicial(cadena, n1=1):
    esp1 = Player_nm.index(' ')
    return cadena[esp1 + 1:esp1 + n1 + 1]
Player_nm_l = Player_nm.lower()

a=st.sidebar.button("Analyze")
if a:
        
        
        try:
            urlpla = ('https://www.basketball-reference.com/players/' + Extraer_inicial(Player_nm_l) + '/' + Extraer_nombre(
            Player_nm_l) + '01/gamelog/2023')
            print(urlpla)
            df = pd.read_html(urlpla, header=0)
        except ValueError:
              
            urlpla = ('https://www.basketball-reference.com/players/' + Extraer_inicial(Player_nm_l) + '/' + Extraer_nombre(
            Player_nm_l) + '02/gamelog/2023')
            df = pd.read_html(urlpla, header=0)
                
                                
                
         
         
                
          

        if Pos[0]=='PG':
            urldef = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT66hjhOQ8WyIQL67ihWKOcukBbwPVUUAt8cvYqTkGbnZTgo4XNPtgIknKyleZBL9O_KatA05BJECBl/pub?gid=0&single=true&output=csv'
        elif Pos[0]=='SG':
            urldef = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT66hjhOQ8WyIQL67ihWKOcukBbwPVUUAt8cvYqTkGbnZTgo4XNPtgIknKyleZBL9O_KatA05BJECBl/pub?gid=503690944&single=true&output=csv'
        elif Pos[0]== 'SF':
            urldef ='https://docs.google.com/spreadsheets/d/e/2PACX-1vT66hjhOQ8WyIQL67ihWKOcukBbwPVUUAt8cvYqTkGbnZTgo4XNPtgIknKyleZBL9O_KatA05BJECBl/pub?gid=1088550471&single=true&output=csv'
        elif Pos[0] == 'PF':
            urldef ='https://docs.google.com/spreadsheets/d/e/2PACX-1vT66hjhOQ8WyIQL67ihWKOcukBbwPVUUAt8cvYqTkGbnZTgo4XNPtgIknKyleZBL9O_KatA05BJECBl/pub?gid=1638733906&single=true&output=csv'
        elif Pos[0] == 'C':
            urldef ='https://docs.google.com/spreadsheets/d/e/2PACX-1vT66hjhOQ8WyIQL67ihWKOcukBbwPVUUAt8cvYqTkGbnZTgo4XNPtgIknKyleZBL9O_KatA05BJECBl/pub?gid=831757291&single=true&output=csv'

        Pos_vs_def = pd.read_csv(urldef)
        
        len(df)
        dftb = df[7]

        try:
            dfplayer = dftb.drop(dftb.index [[20,41,62]])
        except IndexError:
            dfplayer = dftb.drop(dftb.index [[20]])


        if Prop_in[0] == "PTS":
            pr_ex = 1

        elif Prop_in[0] == "TRB":
            pr_ex = 2

        elif Prop_in[0] == "AST":
            pr_ex = 3

        elif Prop_in[0] == "3P":
            pr_ex = 4

        elif Prop_in[0] == "STL":
            pr_ex = 5

        elif Prop_in[0] == "BLK":
            pr_ex = 6

        elif Prop_in[0] == "TOV":
            pr_ex = 7


        Opp = dfplayer["Opp"].iloc[Last_n_Games[0]:]
        N_Ga = dfplayer["Rk"].iloc[Last_n_Games[0]:]
        PropPr = dfplayer[Prop_in].iloc[Last_n_Games[0]:]
        N_Ga_A = np.asarray(N_Ga)
        riv = np.asarray(Opp)
        Ar_Def = np.zeros(0)
        Ar_Player = np.zeros(0)

        for rival in riv:

            if rival == 'ATL':
                tm_ex = 0

            elif rival == "BRK":
                tm_ex = 1

            elif rival == "BOS":
                tm_ex = 2

            elif rival == "CHO":
                tm_ex = 3

            elif rival == "CHI":
                tm_ex = 4

            elif rival == "CLE":
                tm_ex = 5

            elif rival == "DAL":
                tm_ex = 6

            elif rival == "DEN":
                tm_ex = 7

            elif rival == "DET":
                tm_ex = 8

            elif rival == "GSW":
                tm_ex = 9

            elif rival == "HOU":
                tm_ex = 10

            elif rival == "IND":
                tm_ex = 11

            elif rival == "LAC":
                tm_ex = 12

            elif rival == "LAL":
                tm_ex = 13

            elif rival == "MEM":
                tm_ex = 14

            elif rival == "MIA":
                tm_ex = 15

            elif rival == "MIL":
                tm_ex = 16

            elif rival == "MIN":
                tm_ex = 17

            elif rival == "NOP":
                tm_ex = 18

            elif rival == "NYK":
                tm_ex = 19

            elif rival == "OKC":
                tm_ex = 20

            elif rival == "ORL":
                tm_ex = 21

            elif rival == "PHI":
                tm_ex = 22

            elif rival == "PHO":
                tm_ex = 23

            elif rival == "POR":
                tm_ex = 24

            elif rival == "SAC":
                tm_ex = 25

            elif rival == "SAS":
                tm_ex = 26

            elif rival == "TOR":
                tm_ex = 27

            elif rival == "UTA":
                tm_ex = 28

            elif rival == "WAS":
                tm_ex = 29

            Loc_def = Pos_vs_def.iloc[[tm_ex], [pr_ex]]
            Loc_def_Ar = np.asarray(Loc_def)
            Ar_Def = np.append(Ar_Def, [Loc_def_Ar])

        Ar_Player=np.asarray(PropPr)

        Ar_num = np.where(Ar_Player == "Inactive")
        Ar_num= np.asarray(Ar_num)
        Ar_num1 = np.where(Ar_Player == "Did Not Play")
        Ar_num1 = np.asarray(Ar_num1)
        Ar_num2 = np.where(Ar_Player == "Did Not Dress")
        Ar_num2 = np.asarray(Ar_num2)
        Ar_num3 = np.where(Ar_Player == "Not With Team")
        Ar_num3 = np.asarray(Ar_num3)
        
        
        for Ar_i in Ar_Player:

            if Ar_i == "Inactive" or Ar_i == "Did Not Play" or Ar_i == "Did Not Dress" or Ar_i == "Not With Team":
               Ar_Player[Ar_num[0]] = 0
               Ar_Def[Ar_num[0]] = 0
               Ar_Player[Ar_num1[0]] = 0
               Ar_Def[Ar_num1[0]] = 0
               Ar_Player[Ar_num2[0]] = 0
               Ar_Def[Ar_num2[0]] = 0
               Ar_Player[Ar_num3[0]] = 0
               Ar_Def[Ar_num3[0]] = 0



        if Opp_Percentage[0] == 'Atlanta Hawks':
            tm_ex = 0

        elif Opp_Percentage[0] == "Brooklyn Nets":
            tm_ex = 1

        elif Opp_Percentage[0] == "Boston Celtics":
            tm_ex = 2

        elif Opp_Percentage[0] == "Charlotte Hornets":
            tm_ex = 3

        elif Opp_Percentage[0]== "Chicago Bulls":
            tm_ex = 4

        elif Opp_Percentage[0] == "Cleveland Cavaliers":
            tm_ex = 5

        elif Opp_Percentage[0] == "Dallas Mavericks":
            tm_ex = 6

        elif Opp_Percentage[0] == "Denver Nuggets":
            tm_ex = 7

        elif Opp_Percentage[0] == "Detroit Pistons":
            tm_ex = 8

        elif Opp_Percentage[0] == "Golden State Warriors":
            tm_ex = 9

        elif Opp_Percentage[0] == "Houston Rockets":
            tm_ex = 10

        elif Opp_Percentage[0] == "Indiana Pacers":
            tm_ex = 11

        elif Opp_Percentage[0] == "Los Angeles Clippers":
            tm_ex = 12

        elif Opp_Percentage[0] == "Los Angeles Lakers":
            tm_ex = 13

        elif Opp_Percentage[0] == "Memphis Grizzlies":
            tm_ex = 14

        elif Opp_Percentage[0] == "Miami Heat":
            tm_ex = 15

        elif Opp_Percentage[0] == "Milwaukee Bucks":
            tm_ex = 16

        elif Opp_Percentage[0] == "Minnesota Timberwolves":
            tm_ex = 17

        elif Opp_Percentage[0] == "New Orleans Pelicans":
            tm_ex = 18

        elif Opp_Percentage[0] == "New York Knicks":
            tm_ex = 19

        elif Opp_Percentage[0] == "Oklahoma City Thunder":
            tm_ex = 20

        elif Opp_Percentage[0] == "Orlando Magic":
            tm_ex = 21

        elif Opp_Percentage[0] == "Philadelphia 76ers":
            tm_ex = 22

        elif Opp_Percentage[0] == "Phoenix Suns":
            tm_ex = 23

        elif Opp_Percentage[0] == "Portland Trail Blazers":
            tm_ex = 24

        elif Opp_Percentage[0] == "Sacramento Kings":
            tm_ex = 25

        elif Opp_Percentage[0] == "San Antonio Spurs":
            tm_ex = 26

        elif Opp_Percentage[0] == "Toronto Raptors":
            tm_ex = 27

        elif Opp_Percentage[0] == "Utah Jazz":
            tm_ex = 28

        elif Opp_Percentage[0] == "Washington Wizards":
            tm_ex = 29

        Loc_def_P = Pos_vs_def.iloc[[tm_ex], [pr_ex]]
        Opp_P_r = Loc_def_P.astype(np.float64)
        Opp_plt= np.asarray(Opp_P_r)

        Player = Ar_Player.astype(np.int64)
        Defense = Ar_Def.astype(np.float64)


        Player_df=pd.DataFrame(Player, columns = ["Player"])
        Defense_nm_df = pd.DataFrame(riv, columns=["Team"])
        N_Ga_df = pd.DataFrame(N_Ga_A, columns=["N°"])
        Defense_df = pd.DataFrame(Defense, columns=["Defense Avg."])
        Tabla_chido = pd.concat([Player_df, Defense_nm_df,Defense_df,N_Ga_df],axis=1)
        Opp_P = pd.DataFrame(Opp_plt, columns=["%"])
        
        
        if opt[0] =="Adam":
           optimizer=tf.keras.optimizers.Adam(0.01)
        elif opt[0] =="Adadelta":
           optimizer=tf.keras.optimizers.Adadelta(0.001)
        elif opt[0] =="Adagrad":
           optimizer=tf.keras.optimizers.Adagrad(0.001)
        elif opt[0] =="Adamax":
          optimizer=tf.keras.optimizers.Adamax(0.001)
        elif opt[0] =="Nadam":
          optimizer=tf.keras.optimizers.Nadam(0.001)
        elif opt[0] =="Ftrl":
          optimizer= tf.keras.optimizers.Ftrl(0.001)
        elif opt[0] =="RMSprop":
          optimizer= tf.keras.optimizers.RMSprop(0.001)





        capa = tf.keras.layers.Dense(units=1, input_shape=[1])
        modelo = tf.keras.Sequential([capa])

        oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
        oculta2 = tf.keras.layers.Dense(units=3)
        salida = tf.keras.layers.Dense(units=1)
        modelo = tf.keras.Sequential([oculta1, oculta2, salida])
        modelo.compile(
            optimizer,
            loss='mean_squared_error'
        )





        with st.spinner("Starting training..."):
            historial = modelo.fit(Defense, Player, epochs=1000, verbose=False)
        st.success("Model trained!")
        resultado = modelo.predict([Opp_P_r])
        resultado = np.round(resultado, 3)
        Res = pd.DataFrame(resultado, columns=["Result"])
        Tabla_chido2 = pd.concat([Res, Opp_P], axis=1)

        fig = px.bar(Tabla_chido, x='N°', y=["Player", "Defense Avg."],
                     color_discrete_sequence=['#66FCF1', '#45A29E'] * len(Tabla_chido), barmode='group',
                     title="Last " + str(Last_n_Games_b[0]) + " games")
        fig.add_hline(y=Bt_line, line_color="#00ECFF", line_width=4)
        texts = [riv, riv]



        for i, t in enumerate(texts):
            fig.data[i].text = t
            fig.data[i].textposition = 'inside'

        fig2 = px.bar(Tabla_chido2, x=Opp_Percentage, y=["Result", "%"],
                      color_discrete_sequence=['#66FCF1', '#45A29E'] * len(Tabla_chido), barmode='group',
                      title="A.I. Prediction")
        fig2.add_hline(y=Bt_line, line_color="#00ECFF", line_width=4)

        st.write("\n\n\n\n\n")
        m2, m3, m4 = st.columns(3)


        AVG_c = 0
        for n_Ar_Player in Player:

            if n_Ar_Player >= float(Bt_line):
                AVG_c = AVG_c + 1

            else:
                AVG_c = AVG_c

        AVG_Cf = (AVG_c * 100) / Last_n_Games_b[0]
        m2.metric(label="Has happened in the", value=str(round(AVG_Cf, 3)) + "%", delta="of the times",delta_color="off")


        Total = 0
        Num = 0
        for n_Ar_Player in Player:
            if n_Ar_Player >= float(Bt_line):
                Dif_OV = n_Ar_Player - float(Bt_line)
                Total = Dif_OV + Total
                Num = Num + 1
        if Total == 0:
            Avg_OV = 0
            text_OV = "Never has been OVER the line"
            m3.metric(label=text_OV, value="0"+" " + str(Prop_in[0]) , delta="with an average of ",delta_color="off")
        else:
            Avg_OV = Total / Num
            text_OV = "Did the OVER "+ str(Bt_line) + " -  " + str(Num) + " time(s)"
            m3.metric(label=text_OV, value=str(np.round(Avg_OV[0], 3)) + " " + str(Prop_in[0]),delta="with an average of ", delta_color="off")
        Sum = 0
        Cant = 0
        for n_Ar_Player in Player:
            if n_Ar_Player <= float(Bt_line):
                Dif_UN = float(Bt_line) - n_Ar_Player
                Sum = Dif_UN + Sum
                Cant = Cant + 1
        if Sum == 0:
            Avg_UN = 0
            text_UN = "Never has been UNDER the line"
            m4.metric(label=text_UN, value="0" + " " + str(Prop_in[0]), delta="with an average of ",delta_color="off")
        else:
            Avg_UN = Sum / Cant
            text_UN = "Did the UNDER "+ str(Bt_line) + "  - " + str(Cant) + " time(s)"
            m4.metric(label=text_UN, value=str(np.round(Avg_UN[0], 3)) + " " + str(Prop_in[0]), delta="with an average of ",delta_color="off")









        st.info(Player_nm + " is expected to make " + str(resultado[0][0]) + " " + str(Prop_in[0]) + " vs " + Opp_Percentage[0])
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.write(urlpla)

st.sidebar.image(logo_ic,width=73)
