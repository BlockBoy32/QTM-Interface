import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import time

#NEW IMPORTS
from UserInterface.helpers import *
from Model.parts.utils import *


def userAdoptionInput(sys_param, tav_return_dict):
    with st.expander("**User Adoption**"):
        st.markdown("### User Adoption")
        # adoption style choice | user numbers | revenues
        col61, col62, col63 = st.columns([0.2,0.3,0.5])
        with col61:
            adoption_style_choices = ['Weak', 'Medium', 'Strong', 'Custom']
            adoption_style = st.radio('Adoption Assumption',tuple(adoption_style_choices), index=adoption_style_choices.index(sys_param['adoption_style'][0]) if 'adoption_style' in sys_param else 0, help='The adoption style determines the scaling velocity for the product revenue and token demand. Moreover it influences the average agent sentiment in terms of selling and utility adoption behavior.')
            show_full_adoption_table = st.toggle('Show Full Table', value=False, help="Show the full adoption parameter set.")
        with col62:
            initial_product_users = st.number_input('Initial Product Users', label_visibility="visible", min_value=0, value=int(sys_param['initial_product_users'][0]), disabled=False, key="initial_product_users", help="The initial product users generating revenue in diverse assets -> $.")
            initial_token_holders = st.number_input('Initial Token Holders', label_visibility="visible", min_value=0, value=int(sys_param['initial_token_holders'][0]), disabled=False, key="initial_token_holders", help="Initial token holders that regularly buy tokens from the DEX liquidity pool.")

        adoption_dict = {
            "Weak" : {
                "avg_product_user_growth_rate" : 0.5,
                "avg_token_holder_growth_rate" : 0.5,
                "product_adoption_velocity" : 0.5,
                "token_adoption_velocity" : 0.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 0.5,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 0.5,
                "avg_token_utility_allocation" : 20.0,
                "avg_token_selling_allocation" : 70.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 10.0,

            },
            "Medium" : {
                "avg_product_user_growth_rate" : 3.5,
                "avg_token_holder_growth_rate" : 3.5,
                "product_adoption_velocity" : 1.5,
                "token_adoption_velocity" : 1.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 2.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 2.0,
                "avg_token_utility_allocation" : 60.0,
                "avg_token_selling_allocation" : 30.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 6.0,

            },
            "Strong" : {
                "avg_product_user_growth_rate" : 8.0,
                "avg_token_holder_growth_rate" : 8.0,
                "product_adoption_velocity" : 2.5,
                "token_adoption_velocity" : 2.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 6.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 6.0,
                "avg_token_utility_allocation" : 75.0,
                "avg_token_selling_allocation" : 20.0,
                "avg_token_holding_allocation" : 5.0,
                "avg_token_utility_removal" : 3.0,
            }
        }

        if adoption_style == 'Custom' or show_full_adoption_table:
            col71, col72 = st.columns(2)
            with col71:
                avg_product_user_growth_rate = st.number_input('Avg. Product Users Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['product_users_after_10y'][0]) / float(sys_param['initial_product_users'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_product_user_growth_rate']][0], disabled=False, key="product_users_growth_rate", help="The average monthly growth rate of product users.")
                product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
                st.write(f"Projected Product Users (10y): {int(np.ceil(product_users_after_10y)):+,}")
                product_adoption_velocity = st.number_input('Product Adoption Velocity', label_visibility="visible", min_value=0.1, value=[float(sys_param['product_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['product_adoption_velocity']][0], disabled=False, key="product_adoption_velocity", help="The velocity of product adoption. The higher the velocity, the faster the product adoption in the early years towards market saturation.")
                regular_product_revenue_per_user = st.number_input('Regular Product Revenue / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_product_revenue_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0], disabled=False, key="regular_product_revenue_per_user", help="The average regular monthly product revenue per user. This will accrue to the different revenue share buckets.")                
                
                    
            with col72:
                avg_token_holder_growth_rate = st.number_input('Avg. Token Holder Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['token_holders_after_10y'][0]) / float(sys_param['initial_token_holders'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holder_growth_rate']][0], disabled=False, key="avg_token_holder_growth_rate", help="The average monthly growth rate of token holders.")
                token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
                st.write(f"Projected Token Holders (10y): {int(np.ceil(token_holders_after_10y)):+,}")
                token_adoption_velocity = st.number_input('Token Adoption Velocity', label_visibility="visible", min_value=0.1, value=[float(sys_param['token_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['token_adoption_velocity']][0], disabled=False, key="token_adoption_velocity", help="The velocity of token adoption. The higher the velocity, the faster the token adoption in the early years towards market saturation.")
                regular_token_buy_per_user = st.number_input('Regular Token Buy / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_token_buy_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_token_buy_per_user']][0], disabled=False, key="regular_token_buy_per_user", help="The average regular monthly token buy per token holder. This will accrue directly to the token via buys from the DEX liquidity pool.")
        else:
            avg_product_user_growth_rate = adoption_dict[adoption_style]['avg_product_user_growth_rate']
            product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
            avg_token_holder_growth_rate = adoption_dict[adoption_style]['avg_token_holder_growth_rate']
            token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
        
        # revenue share settings
        col71a, col71b, col71c, col71d = st.columns(4)
        with col71a:
            business_rev_share = st.number_input('Business Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['business_rev_share'][0]) if 'business_rev_share' in sys_param else 75.0][0], disabled=False, key="business_rev_share", help="The share of revenue that will accrue to the business funds.")
        with col71b:
            staker_rev_share = st.number_input('Staker Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['staker_rev_share'][0]) if 'staker_rev_share' in sys_param else 25.0][0], disabled=False, key="staker_rev_share", help="The share of revenue that will accrue to token stakers. This requires staking to be one of the token utilities.")
            if staker_rev_share > 0.0:
                staker_rev_share_buyback = st.checkbox('Buyback Tokens', value=[float(sys_param['staker_rev_share_buyback'][0]) if 'staker_rev_share_buyback' in sys_param else False][0], key="staker_rev_share_buyback", help="Check this box if the staker revenue share should be used to buy back tokens from the market (DEX liquidity pool) and distribute them instead of the revenue in diverse assets. Diverse assets are any assets that will be collected as revenue and depend on the product. They can be any assets apart from the token itself.")
            else:
                staker_rev_share_buyback = False
        with col71c:
            service_provider_rev_share = st.number_input('Service Provider Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['service_provider_rev_share'][0]) if 'service_provider_rev_share' in sys_param else 0.0][0], disabled=False, key="service_provider_rev_share", help="The share of revenue that will accrue to service providers.")
        with col71d:
            incentivisation_rev_share = st.number_input('Incentivisation Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['incentivisation_rev_share'][0]) if 'incentivisation_rev_share' in sys_param else 0.0][0], disabled=False, key="incentivisation_rev_share", help="The share of revenue that will be used to incentivise the ecosystem.")
            if incentivisation_rev_share > 0.0:
                incentivisation_rev_share_buyback = st.checkbox('Buyback Tokens', value=[float(sys_param['incentivisation_rev_share_buyback'][0]) if 'incentivisation_rev_share_buyback' in sys_param else False][0], key="incentivisation_rev_share_buyback", help="Check this box if the incentivisation revenue share should be used to buy back tokens from the market (DEX liquidity pool) and distribute them instead of the revenue in diverse assets. Diverse assets are any assets that will be collected as revenue and depend on the product. They can be any assets apart from the token itself.")
            else:
                incentivisation_rev_share_buyback = False
            if incentivisation_rev_share > 0.0 or tav_return_dict['incentivisation_allocation'] or tav_return_dict['airdrop_allocation'] > 0.0:
                # add user adoption boost per incentivisation (in USD)
                user_adoption_target = st.number_input('Incentive USD per User Target / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['user_adoption_target'][0]) if 'user_adoption_target' in sys_param else 550.0][0], disabled=False, key="user_adoption_target", help="Target incentivisation to onboard one more product users. A value of 0 disables this feature!")
            else:
                user_adoption_target = 0.0

        rev_share_sum = business_rev_share + staker_rev_share + service_provider_rev_share + incentivisation_rev_share
        if rev_share_sum != 100.0:
            st.error(f"The revenue shares must sum up to 100%. Currently they sum up to {rev_share_sum}%.", icon="⚠️")

        st.markdown("#### Market Simulation")
        switch = st.toggle('Activate', value = False, help="This section allows you to make your Token Adoption (i.e. how many people buy your token) dependent on simulated market returns. In its current specification, the amount of users buying the token of the economy will increase/decrease based on the simulated market returns. E.g. If the market shows positive returns, token purchases increase correspondingly, and viceversa. You can select the token you want to use to represent the market in your simulation (i.e. market beta). The simulation is performed using Brownian Motions.") 
        
        if switch:
            # Choose token to use as proxy for market sentiment
            token_choice_predefined = ['bitcoin', 'ethereum']
            token_choice = st.radio("###### Select Token", tuple(token_choice_predefined))
            
            # Checks
            today = datetime.today().date()
            default_start_date = today - timedelta(days=365)
            
            # Define the start and end date inputs with restrictions
            sim_start_date = st.date_input(
                "Start Date",
                value=default_start_date,
                max_value=today,  
                help="Select the start date for the simulation. The start date must be at least 180 days before the end date to provide sufficient data for the simulation."
            )

            sim_end_date = st.date_input(
                "End Date",
                value=today,
                min_value=sim_start_date,  
                max_value=today,
                help="Select the end date for the simulation. The end date must be at least 180 days after the start date to provide sufficient data for the simulation."
            )

            # Button to trigger the simulation
            simulate_button = st.button("Simulate Returns")

            # Initialize variables with a default value
            start_date_unix = int(time.mktime(sim_start_date.timetuple()))
            end_date_unix = int(time.mktime(sim_end_date.timetuple()))
            active = 1

            if simulate_button:
                # Check if the dates meet the conditions
                if sim_start_date > sim_end_date - timedelta(days=180):
                    st.warning("The selected date range is too small to run the simulation. Please adjust the dates to include at least 6 MONTHS of historical price data.", icon="⚠️")

                else:
                    # Display spinner and perform computations only if conditions are met
                    with st.spinner("Please wait while the simulation chart is loading..."):

                        # Fetch and simulate market returns
                        result = simulate_market_returns(token_choice, start_date_unix, end_date_unix)
                        simulation_df = result['market']

                        # Plotting and displaying the figure in Streamlit
                        fig = plot_simulation_results(simulation_df, token_choice) 
                        st.plotly_chart(fig, use_container_width=True)

        else:
            token_choice = 0
            start_date_unix = 0
            end_date_unix = 0
            active = 0 
        
    
    product_adoption_velocity = [product_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['product_adoption_velocity']][0]
    token_adoption_velocity = [token_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['token_adoption_velocity']][0]
    regular_product_revenue_per_user = [regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0]
    regular_token_buy_per_user = [regular_token_buy_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_token_buy_per_user']][0]

    ua_return_dict = {
        "adoption_style" : adoption_style,
        "show_full_adoption_table" : show_full_adoption_table,
        "initial_product_users" : initial_product_users,
        "initial_token_holders" : initial_token_holders,
        "avg_product_user_growth_rate" : avg_product_user_growth_rate,
        "product_users_after_10y" : product_users_after_10y,
        "product_adoption_velocity" : product_adoption_velocity,
        "regular_product_revenue_per_user" : regular_product_revenue_per_user,
        "avg_token_holder_growth_rate" : avg_token_holder_growth_rate,
        "token_holders_after_10y" : token_holders_after_10y,
        "token_adoption_velocity" : token_adoption_velocity,
        "regular_token_buy_per_user" : regular_token_buy_per_user,
        "adoption_dict" : adoption_dict,
        "business_rev_share" : business_rev_share,
        "staker_rev_share" : staker_rev_share,
        "service_provider_rev_share" : service_provider_rev_share,
        "incentivisation_rev_share" : incentivisation_rev_share,
        "rev_share_sum" : rev_share_sum,
        "staker_rev_share_buyback" : staker_rev_share_buyback,
        "incentivisation_rev_share_buyback" : incentivisation_rev_share_buyback,
        "user_adoption_target": user_adoption_target,
        "token": token_choice,
        "sim_start": start_date_unix,
        "sim_end": end_date_unix,
        "market": active
    }

    return ua_return_dict
