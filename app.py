import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
df=pd.read_csv("E:\MTech IN AI\CAMPUSX_PROGRAM\STREAMLIT\Indian_Startup_Ananalysis\startup_cleaned.csv")

st.set_page_config(layout='wide',page_title='StartupAnalysis')

df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month

#Creating overall analysis function:
def load_overall_analysis():
    st.title('Overall Analysis')
    
    #Total invested amount
    total_amount=round(df['amount'].sum(),2)
    st.metric('Total amount is',str(total_amount)+' Cr')
    
    #Maximum investmented company
    max_invest=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1)[0]
    company=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).index[0]
    st.metric('Max investment done by investor is', str(max_invest)+ ' Cr' + ' for company named' + company)
    
    #Avg investment
    avg_invest=round(df.groupby('startup')['amount'].sum().mean(),2)
    st.metric('AVG', str( avg_invest)+ ' Cr')
    
    #Total funded startups
    funded_startups=df['startup'].nunique()
    st.metric('Funded startups', funded_startups)
#Creating function to load selected investor details:
def load_investor_details(investor):
    st.title(investor)
    #Listing down investment details of selected investor
    investor_df=df[df['Name'].str.contains(investor)].sort_values('date',ascending=False).head(5)
    st.write("Latest investoments are:")
    st.dataframe(investor_df)
    
    #Listing top investments, investor has made:
    big_investment=df[df['Name'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
    st.subheader("Biggest investors")
    st.dataframe(big_investment)
    col1,col2=st.columns(2)
    with col1:

        #Plotting the data
        st.subheader('Bar chart')
        fig,ax=plt.subplots()
        ax.bar(big_investment.index,big_investment.values)
        st.pyplot(fig)

    with col2:
        vertical_wise=df[df['Name'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("Pie chart")
        #Plotting pie chart
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_wise,labels=vertical_wise.index,autopct='%0.01f')
        st.pyplot(fig1)
        
    col3,col4=st.columns(2)
    with col3:
        round_wise=df[df['Name'].str.contains(investor)].groupby('round')['amount'].sum()
        #Plotting pie chart round_wise:
        st.subheader('Pie_chart round wise')
        fig3,ax3=plt.subplots()
        ax3.pie(round_wise,labels=round_wise.index,autopct='%0.01f')
        st.pyplot(fig3)
    with col4:
        city_wise=df[df['Name'].str.contains(investor)].groupby('city')['amount'].sum()
        #Plotting pie chart city_wise:
        st.subheader('Pie_chart city wise')
        fig4,ax4=plt.subplots()
        ax4.pie(city_wise,labels=city_wise.index,autopct='%0.01f')
        st.pyplot(fig4)
        
    #Creating line chart to show YOY investment
    df['year']=df['date'].dt.year
    year_wise=df[df['Name'].str.contains(investor)].groupby('year')['amount'].sum()
    
    st.subheader('YOY investment')
    fig5,ax5=plt.subplots()
    ax5.plot(year_wise.index,year_wise.values)
    st.pyplot(fig5)
#Making sidebar for desired options
st.sidebar.title("Startup Funding Analysis")
options=st.sidebar.selectbox('Please choose your option',['overall analysis','Investors','Startups'])

if options=='overall analysis':
    bt0=st.sidebar.button("Find overall analysis")
    if bt0:
        load_overall_analysis()

elif options=='Startups':
    st.sidebar.selectbox('Please select startup',sorted(df['startup'].unique().tolist()))
    bt1=st.sidebar.button('Find startups details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('Investor will be',sorted(set(df['Name'].str.split(',').sum())))
    bt2=st.sidebar.button('Find Investors details')
    
    if bt2:
        load_investor_details(selected_investor)
    st.title('Investor Analysis')
    
