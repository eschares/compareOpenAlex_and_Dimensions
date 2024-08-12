# Compare counts of journal and year in OpenAlex and Dimensions
# Eric Schares, 8/12/24

import pandas as pd
import plotly.express as px
import streamlit as st

# had used plotly#==5.10.0
#streamlit#==1.13.0
#pandas#==1.4.2


st. set_page_config(layout="wide")

st.header('Compare OpenAlex and Dimensions article counts')
st.write('Eric Schares, 8/12/24')
st.write('Using OpenAlex new `article` classification, released 7/29/24. Reclassifies articles into editorials, letters, erratum, etc.')
st.write('How does this new mapping compare to Dimensions?')
st.write('Pulled the counts of articles in OpenAlex for 1,069 Gold journals as defined in the APC dataset having APCs for all five years, 2019-2023. Data was ISSN, Year, DocType, and Count.')
st.write('`https://api.openalex.org/works?per_page=200&filter=primary_location.source.issn:XXXX-XXXX,publication_year:YYYY&group_by=type`')
st.write('For **Dimensions** data, previously pulled for >8700 individual journals * 5 years each. Used document type filters `(PT=Article, DT=Research Article OR Review Article)`, nothing for OpenAlex.')
st.write('Compared counts of OpenAlex research + review types with Dimensions PT=article, DT=research or review')

merged_wide = pd.read_csv('innermerged_Dimensions_and_OpenAlex_wideform.csv')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write('n_works is from OpenAlex, Dim_count is from Dimensions')
    st.write(first10)

st.write('---')
st.header('Inner merge')


issn = '2475-0379'
fig = px.bar(merged_wide[merged_wide['ISSN-year_tag'].str.contains(issn)], x='year', y=['count_Dimensions', 'count_OpenAlex'], barmode='group',
       title=f'ISSN {issn} Research and Practice in Thrombosis and Haemostasis')  # facet_col='DocType_normalized')

st.plotly_chart(fig)




fig2 = px.scatter(merged_wide, x='count_Dimensions', y='count_OpenAlex',
                 hover_data='ISSN-year_tag',
                 title='X-Y Scatterplot of 2884 Gold ISSNs*5years, Research+Review Counts, Dimensions vs. OpenAlex (new Doctypes)')
# facet_row='DocType_normalized')

fig2.add_shape(type="line",
              x0=1, y0=0, x1=20000, y1=20000,
              line=dict(color="Purple", width=1, dash="dot"), col='all', row='all')

fig2.update_layout(height=600)

st.plotly_chart(fig2)


fig3 = px.histogram(merged_wide, x='Dim/OpenAlex', marginal='box',
             hover_data='ISSN-year_tag',
             title='Histogram and boxplot of Dim/OpenAlex count, research + review articles for 4824 Gold ISSN-years<br>>1 means Dimensions found more')

st.plotly_chart(fig3)


st.subheader('Data sorted by Dim/OpenAlex column, biggest difference first')
st.write(merged_wide.sort_values(by='Dim/OpenAlex', ascending=False))










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


