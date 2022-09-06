import pandas as pd 
import datetime
import streamlit as st 
import pickle 
from pickle import load
import datetime
import plotly.express as px
from pandas.tseries.offsets import DateOffset


data = pd.read_csv('CO2 dataset.csv',parse_dates=True)
data=data.set_index('Year')
data.index=pd.to_datetime(data.index,format='%Y')
df = data
validation = pd.read_csv('CO2_resultls.csv')
validation=validation.drop("Unnamed: 0",axis=1)

arima = load(open('CO2_forecast_ARIMA.sav','rb'))
# sarima = load(open('CO2_forecast_SARIMA.sav','rb'))
hw = load(open("CO2_forecast_Holt-Winter.sav",'rb'))
# future = (range(2015,2025))
# select_year = pd.to_datetime(future,format='%Y')
# future = pd.DataFrame(future)


def main(): 

    st.set_page_config(
        page_title= "Forecasting Web Application",
        layout= "wide"
    )
    st.title('Forecasting Web Application')
    Menu = ["ARIMA",'SARIMA','Holt-Winter','Compare Models'] 

    col1,col2 = st.columns(2)
    with col1:
        st.write("Original Data")
        st.write(df)
#         st.write(validation)
    with col2:
        fig = px.line(df,x=df.index,y='CO2',title="Line plot of Origina Data")
        st.plotly_chart(fig)

    load= st.button("Select Model")
    if "load_state" not in st.session_state :
        st.session_state.load_state = False
        
        st.warning('Click on the select model button to choose different options')

    if load or st.session_state.load_state:
        st.session_state.load_state= True

        choice = st.sidebar.selectbox("select model", Menu)
        st.sidebar.warning('''Please close the side bar to get better view after choosing any one option
                            you can access side bar by clicking on ">" symbol on top left corner''')
        if choice == 'ARIMA' :
            st.subheader("Forecasting with ARIMA model")
        #data= st.number_input("Insert number of Years",min_value=1, max_value=15)
            st.write('Click on Forecast button to get results')
            lod = st.button('Forecast')
            if "lod_sate" not in st.session_state:
                st.session_state.lod_sate = False
                
                st.warning('Click on the Forecast button to get results')

            if lod or st.session_state.lod_sate:
                st.session_state.lod_sate= True    
                st.warning("Starting Year is Default please choose ending Year")            
                end = st.date_input("End",min_value= pd.to_datetime('2022-01-01'),
                                        max_value = None )
                # end = len(df)+len(future)
                predicted = arima.predict(start=df.index[-1],end=end)
                CO2_forecast=[]
                for i in predicted:
                    CO2_forecast.append(i)
                ARIMA_forecast=pd.DataFrame(predicted)
                ARIMA_forecast['Year'] = predicted.index
                ARIMA_forecast= ARIMA_forecast.set_index('Year')
                # ARIMA_forecast.index=pd.to_datetime(ARIMA_forecast.index,format='%Y')
                # ARIMA_forecast.index.astype(dtype = 'datetime64[ns]')
                ARIMA_forecast["CO2_forecast"]=CO2_forecast
                ARIMA_forecast.drop('predicted_mean',axis=1,inplace=True)
                frames = [df, ARIMA_forecast]
                result = pd.concat(frames)
                # st.write(result)
                
                
                col4,col5=st.columns(2)       
                with col4:
                    st.write('Results of ARIMA Model')
                    st.write(ARIMA_forecast)
                # fig = px.line(df,x='Year',y='CO2')
                # Year = ARIMA_forecast.index
                with col5:
                    
                    fig_arima = px.line(result,title= "Line chart of CO2 Forecasted by ARIMA")
                    st.plotly_chart(fig_arima)
                
                st.write("ARIMA model scores")
                arirma_results = validation[validation['Model']=='ARIMA']
                arirma_results = arirma_results.reset_index(None)
                arirma_results = arirma_results.drop('index',axis = True)
                st.write(arirma_results)    

        elif choice == 'SARIMA' :
            # if 'SARIMA' not in st.session_state:
            #     st.session_state.SARIMA = False
            # if SARIMA or st.session_state.SARIMA_state:
            #     st.session_state.SARIMA_state = True
            st.subheader("Forecasting with SARIMA Model")
            #data= st.number_input("Insert number of Years",min_value=1, max_value=15)
            #future_year = st.selectbox('select year',select_year)
            st.write('Click on Forecast button to get results')
            lod = st.button('Forecast')
            if "lod_state" not in st.session_state:
                st.session_state.lod_state = False
                
                st.warning('Click on the Forecast button to get results')

            if lod or st.session_state.lod_state:
                st.session_state.lod_state= True
                
                # start = st.select_year("Start",value =pd.to_datetime(df[-1]) )
                st.warning("Starting Year is Default please choose ending Year")
                end = st.date_input("Select End Year",min_value= pd.to_datetime('2022-01-01'),
                                        max_value = None )
                # end = len(df)+len(future)
                predicted = sarima.predict(start=df.index[-1],end=end)
                CO2_forecast=[]
                for i in predicted:
                    CO2_forecast.append(i)
                SARIMA_forecast=pd.DataFrame(predicted)
                SARIMA_forecast['Year'] = predicted.index
                SARIMA_forecast= SARIMA_forecast.set_index('Year')
                # ARIMA_forecast.index=pd.to_datetime(ARIMA_forecast.index,format='%Y')
                # ARIMA_forecast.index.astype(dtype = 'datetime64[ns]')
                SARIMA_forecast["CO2_forecast"]=CO2_forecast
                SARIMA_forecast.drop('predicted_mean',axis=1,inplace=True)
                frames = [df, SARIMA_forecast]
                result = pd.concat(frames)
                col4,col5=st.columns(2)
                with col4:
                    st.write('Results of SARIMA Model')
                    st.write(SARIMA_forecast)
                # fig = px.line(df,x='Year',y='CO2')
                # Year = ARIMA_forecast.index
                with col5:
                    fig_sarima = px.line(result,title="Line chart of CO2 Forecasted by SARIMA")
                    st.plotly_chart(fig_sarima)
                    # fig_sarima = px.line(SARIMA_forecast,x= SARIMA_forecast.index,y='CO2_forecast',
                    #             title=)
                st.write("SARIMA model scores")
                sarirma_results = validation[validation['Model']=='SARIMA']
                sarirma_results = sarirma_results.reset_index(None)
                sarirma_results = sarirma_results.drop('index',axis = True)
                st.write(sarirma_results)

        elif choice == 'Holt-Winter':
            st.subheader("Forecasting with Holt-Winter model")
            st.write('Click on Forecast button to get results')
            lod = st.button('Forecast')
            if "lod_sate" not in st.session_state:
                st.session_state.lod_sate = False

                st.warning('Click on the Forecast button to get results')

            if lod or st.session_state.lod_sate:
                st.session_state.lod_sate= True    
                st.warning("Starting Year is Default please choose ending Year")            
                end = st.date_input("End",min_value= pd.to_datetime('2022-01-01'),
                                        max_value = None )
                # end = len(df)+len(future)
                predicted = hw.predict(start=df.index[-1],end=end)
                CO2_forecast=[]
                for i in predicted:
                    CO2_forecast.append(i)
                # hw_forecast=pd.DataFrame(predicted)
                hw_forecast=pd.DataFrame(predicted,columns={"CO2_forecast"})
                hw_forecast['Year'] = predicted.index
                hw_forecast= hw_forecast.set_index('Year')
                # hw_forecast["CO2_forecast"]=CO2_forecast
                # hw_forecast.drop('predicted_mean',axis=1,inplace=True)
                frames = [df, hw_forecast]
                result = pd.concat(frames)

                col4,col5=st.columns(2)
                
                with col4:
                    st.write('Results of Holt-Winter Model')
                    st.write(hw_forecast)
                with col5:
                    fig_hw = px.line(result,title="Line chart of CO2 Forecasted by Holt-Winter")
                    st.plotly_chart(fig_hw)
                    # fig_hw = px.line(hw_forecast,x= hw_forecast.index,y='CO2_forecast',
                    #             )
                st.write("Holt-Winter model scores")
                hw_results = validation[validation['Model']=='Holt-Winter']
                hw_results = hw_results.reset_index(None)
                hw_results = hw_results.drop('index',axis = True)
                st.write(hw_results)
                    
        elif choice == "Compare Models" :

            button = st.button("Compare")
            if "button_state" not in st.session_state:
                st.session_state.button_sate = False
                st.warning('Click on the Compare button to get results')
            if button or st.session_state.button_sate:
                st.session_state.button_sate= True 
                st.warning("Choose the model whose test data score is lower than other models")
                col6,col7,col8 = st.columns(3)
                with col6:
                    st.write("ARIMA model scores")
                    arirma_results = validation[validation['Model']=='ARIMA']
                    arirma_results = arirma_results.reset_index(None)
                    arirma_results = arirma_results.drop('index',axis = True)
                    st.write(arirma_results)
                    # st.write('Results of ARIMA Model')
                    # st.write(ARIMA_forecast)
                    # st.plotly_chart(fig_arima)
                with col7:
                    st.write("SARIMA model scores")
                    sarirma_results = validation[validation['Model']=='SARIMA']
                    sarirma_results = sarirma_results.reset_index(None)
                    sarirma_results = sarirma_results.drop('index',axis = True)
                    st.write(sarirma_results)
                    # st.write('Results of SARIMA Model')
                    # st.write(SARIMA_forecast)
                    # st.plotly_chart(fig_sarima)
                with col8 :
                    st.write("Holt-Winter model scores")
                    hw_results = validation[validation['Model']=='Holt-Winter']
                    hw_results = hw_results.reset_index(None)
                    hw_results = hw_results.drop('index',axis = True)
                    st.write(hw_results)
                    # st.write("Results of Holt-Winter Model")
                    # st.write(hw_forecast)
                    # st.plotly_chart(fig_hw)

if __name__=='__main__':
    main()
