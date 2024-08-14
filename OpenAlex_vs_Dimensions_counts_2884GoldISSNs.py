# Compare counts of journal and year in OpenAlex and Dimensions
# Eric Schares, 8/12/24

import pandas as pd
import streamlit as st
# reset Plotly theme after streamlit import
import plotly.io as pio
import plotly.express as px

pio.templates.default = 'plotly' 

# had used plotly#==5.10.0
#streamlit#==1.13.0
#pandas#==1.4.2


#st. set_page_config(layout="wide")

st.header('Compare OpenAlex and Dimensions article counts')
st.write('Eric Schares, 8/12/24')
st.write('Using OpenAlex new `article` classification, released 7/29/24. Reclassifies articles into editorials, letters, erratum, etc.')
st.write('**How does this new mapping compare to Dimensions?**')
st.write('- Pulled the counts of articles in OpenAlex for 2,884 Gold journals as defined in the APC dataset, looking at years 2019-2023. Data collected was ISSN, Year, DocType, and Count.')
st.write('- Used API call `https://api.openalex.org/works?per_page=200&filter=primary_location.source.issn:XXXX-XXXX,publication_year:YYYY&group_by=type`')
st.write('- For **Dimensions**, previously pulled data for >8700 individual journals * 5 years each in April 2024. Used document type filters `(PT=Article, DT=Research Article OR Review Article)`, nothing for OpenAlex.')
st.write('Compare inner merge counts of OpenAlex `research + review` types with Dimensions `PT=article, DT=research or review`')

st.write('---')
st.subheader('Summary stats')
st.write('**OpenAlex**: 2,884 Gold ISSNs * 5 years, filtering to `article + review` types sum only = 11,821 ISSN-year combinations')
st.write('Inner merge with **Dimensions** results in 8,309 ISSN-year combinations that have data in both databases')

merged_wide = pd.read_csv('innermerged_Dimensions_and_OpenAlex_wideform.csv')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(merged_wide)

st.write('---')
st.header('Inner merge')



fig = px.scatter(merged_wide, x='count_Dimensions', y='count_OpenAlex',
                 hover_data='ISSN-year_tag',
                 title='X-Y Scatterplot of Dimensions vs. OpenAlex (new Doctypes), Research + Review Counts<br>Pulled 2,884 Gold ISSNs * 5 years, Inner merge results in 8,309 ISSN-years')
                 #template='plotly_dark')
# facet_row='DocType_normalized')

fig.add_shape(type="line",
              x0=1, y0=0, x1=23000, y1=23000,
              line=dict(color="Purple", width=1, dash="dot"), col='all', row='all')

fig.update_layout(height=600)#, width=1000)
#fig.update_layout(template='plotly')
#fig.update_layout(paper_bgcolor='rgb(0,0,0)', plot_bgcolor='rgb(0,0,0)')

st.plotly_chart(fig, theme=None)#, template='plotly'
#st.plotly_chart(fig, template='plotly_dark')#, template='plotly'
# theme can be 'streamlit' or None
#template can be plotly, plotly_dark, ggplot2, seaborn



to_color = {'0021-9258', '1053-8119', '1201-9712', '1935-861X', '1935-2735', '2041-4889', '2050-0904', '2059-7029', '2296-858X', '2352-4847', '2451-8301', '2468-0249', '2475-0379', '2475-2991', '2666-1683', '2667-2421', '2767-3375', '2772-4085'}
#group_color = {i: 'red' for i in subset}
#group_color = {i: 'red' for i not in to_color}
#group_color = {i: 'red' for i in merged_wide['ISSN']}
group_color = {i: 'blue' for i in merged_wide['ISSN'] if i not in to_color}
group_color
filt = (merged_wide['count_Dimensions']<=2200)
figzoomed = px.scatter(merged_wide[filt], x='count_Dimensions', y='count_OpenAlex', color='ISSN',
                 color_discrete_map = group_color,
                 hover_data='ISSN-year_tag',
                 title='<b>ZOOMED IN</b>: X-Y Scatterplot of Dimensions vs. OpenAlex (new Doctypes), Research + Review Counts<br>Pulled 2,884 Gold ISSNs * 5 years, Inner merge results in 8,309 ISSN-years<br>Colored by selected ISSN')
# facet_row='DocType_normalized')

figzoomed.add_shape(type="line",
              x0=1, y0=0, x1=23000, y1=23000,
              line=dict(color="Purple", width=1, dash="dot"), col='all', row='all')

figzoomed.update_layout(height=600)#, width=1000)
figzoomed.update_xaxes(range=[-300,2200])
figzoomed.update_yaxes(range=[-300,3200])
#fig.update_layout(template='plotly')
#fig.update_layout(paper_bgcolor='rgb(0,0,0)', plot_bgcolor='rgb(0,0,0)')

st.plotly_chart(figzoomed, theme=None)#, template='plotly'
#st.plotly_chart(fig, template='plotly_dark')#, template='plotly'
# theme can be 'streamlit' or None
#template can be plotly, plotly_dark, ggplot2, seaborn



st.subheader('Residuals, Dim/OpenAlex ratio')
fig2 = px.histogram(merged_wide, x='Dim/OpenAlex', marginal='box',
             hover_data='ISSN-year_tag',
             title='Histogram and boxplot of Dim/OpenAlex count, research + review articles for 4824 Gold ISSN-years<br>>1 means Dimensions found more<br>Click and zoom in')

fig2.update_layout(height=500)#, width=1000)
st.plotly_chart(fig2, theme=None)



st.write('---')
st.header("Look at some ISSNs that don't match well")

issn = '2468-0249'
fig7 = px.bar(merged_wide[merged_wide['ISSN-year_tag'].str.contains(issn)], x='year', y=['count_Dimensions', 'count_OpenAlex'], barmode='group',
             title=f'ISSN {issn} Kidney International Reports',
             color_discrete_map = {'count_Dimensions': px.colors.qualitative.Plotly[0], #blue
                                   'count_OpenAlex': px.colors.qualitative.Plotly[1]},
            template = 'plotly') #red  # facet_col='DocType_normalized')

st.plotly_chart(fig7, theme=None)


issn = '2475-0379'
fig3 = px.bar(merged_wide[merged_wide['ISSN-year_tag'].str.contains(issn)], x='year', y=['count_Dimensions', 'count_OpenAlex'], barmode='group',
             title=f'ISSN {issn} Research and Practice in Thrombosis and Haemostasis',
             color_discrete_map = {'count_Dimensions': px.colors.qualitative.Plotly[0], #blue
                                   'count_OpenAlex': px.colors.qualitative.Plotly[1]},
            template = 'plotly') #red  # facet_col='DocType_normalized')

st.plotly_chart(fig3, theme=None)


issn = '2590-177X'
fig4 = px.bar(merged_wide[merged_wide['ISSN-year_tag'].str.contains(issn)], x='year', y=['count_Dimensions', 'count_OpenAlex'], barmode='group',
             title=f'ISSN {issn} Journal of Biomedical Informatics: X',
             color_discrete_map = {'count_Dimensions': px.colors.qualitative.Plotly[0], #blue
                                   'count_OpenAlex': px.colors.qualitative.Plotly[1]},
            template = 'plotly') #red  # facet_col='DocType_normalized')

st.plotly_chart(fig4, theme=None)

issn = '2590-1583'
fig5 = px.bar(merged_wide[merged_wide['ISSN-year_tag'].str.contains(issn)], x='year', y=['count_Dimensions', 'count_OpenAlex'], barmode='group',
             title=f'ISSN {issn} Gene: X',
             color_discrete_map = {'count_Dimensions': px.colors.qualitative.Plotly[0], #blue
                                   'count_OpenAlex': px.colors.qualitative.Plotly[1]},
            template = 'plotly') #red  # facet_col='DocType_normalized')

st.plotly_chart(fig5, theme=None)

issn = '2772-4085'
fig6 = px.bar(merged_wide[merged_wide['ISSN-year_tag'].str.contains(issn)], x='year', y=['count_Dimensions', 'count_OpenAlex'], barmode='group',
             title=f'ISSN {issn} Neuroscience Applied',
             color_discrete_map = {'count_Dimensions': px.colors.qualitative.Plotly[0], #blue
                                   'count_OpenAlex': px.colors.qualitative.Plotly[1]},
            template = 'plotly') #red  # facet_col='DocType_normalized')

st.plotly_chart(fig6, theme=None)




st.subheader('Data sorted by Dim/OpenAlex column, biggest difference first')
st.write(merged_wide.sort_values(by='Dim/OpenAlex', ascending=False))


st.header('Outer merge')







# fig.update_traces(marker=dict(size=10))

# fig.add_annotation(x=550, y=120,
#                         text="Lots of Letters to Editor",
#                         showarrow = False,
#                         ax=-120,
#                         ay=100)

# fig.add_annotation(x=200, y=50,
#                         text="Lots of LtE",
#                         showarrow = False,
#                         ax=-120,
#                         ay=100)

# fig.add_annotation(x=700, y=750,
#                         text="OpenAlex finds non-gold for some Gold journals",
#                         showarrow = True,
#                         ax=-100,
#                         ay=-80)
# fig.add_annotation(x=1280, y=1350,
#                         text="",
#                         showarrow = True,
#                         ax=-250,
#                         ay=80)
# fig.add_annotation(x=200, y=250,
#                         text="",
#                         showarrow = True,
#                         ax=50,
#                         ay=-200)

# fig.add_shape(type="line",
#     x0=1, y0=0, x1=2000, y1=2000,
#     line=dict(color="Purple", width=1, dash="dot"))

# fig.update_layout(width=800, height=800)
# st.plotly_chart(fig, use_container_width=True)


