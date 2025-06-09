# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

# Write directly to the app
st.title(f" :cup_with_straw: Pending Smoothie Orders! :cup_with_straw:")
st.write(
  """Order that need to be filled.
  """
)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    #st.dataframe(data=my_dataframe, use_container_width=True)
    submitted = st.button('Submit')
    
    if submitted:
        st.success('Someone clicked the button', icon = "\U0001F44D")
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success('Order(s) updated!', icon = "\U0001F44D")
        except:
            st.success('Something went wrong!')
else:
    st.success('There are no pending orders right now!', icon = '\U0001F44D')
