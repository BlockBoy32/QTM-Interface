# POLICY FUNCTIONS
def generate_agent_behavior(params, substep, state_history, prev_state, **kwargs):
    """
    Define the agent behavior for each agent type
    """
    if params['agent_behavior'] == 'stochastic':
        """
        Define the agent behavior for each agent type for the stochastic agent behavior
        Agent actions are based on a weighted random choices.
        """
        agent_behavior_dict = {
            'angle': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'seed': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'presale_1': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'presale_2': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'public_sale': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'team': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'reserve': {
                'trade': 0,
                'hold': 50,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 50
            },
            'community': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'foundation': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'placeholder_1': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'placeholder_2': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'market_investors': {
                'trade': 60,
                'hold': 10,
                'utility': 25,
                'remove_locked_tokens': 5,
                'incentivise': 0
            }
        }
    
    elif params['agent_behavior'] == 'static':
        """
        Define the agent behavior for each agent type for the static 1:1 QTM behavior
        """
        agents = prev_state['agents'].copy()
        
        # initialize agent behavior dictionary
        agent_behavior_dict = {}

        # populate agent behavior dictionary
        for agent in agents:
            agent_behavior_dict[agents[agent]['type']] = {
                'trade': params['avg_token_selling_allocation'],
                'hold': params['avg_token_holding_allocation'],
                'utility': params['avg_token_utility_allocation'],
                'remove_locked_tokens': params['avg_token_utility_removal'],
                'incentivise': 0
            }

    return {'agent_behavior_dict': agent_behavior_dict}

def meta_bucket_token_allocations(params, substep, state_history, prev_state, **kwargs):
    """
    Define the meta bucket token allocations of all agents with respect to 'sell' 'hold' and 'utility'
    """
    updated_agents = prev_state['agents'].copy()

    # initialize meta bucket token allocations
    meta_bucket_allocations= {
        'selling': 0,
        'holding': 0,
        'utility': 0,
        'removed': 0
    }

    # update agent token allocations and update the meta bucket allocations w.r.t. each agents contribution
    # note that protocol buckets are not used for meta bucket allocations
    for agent in updated_agents:
        if updated_agents[agent]['type'] != 'protocol_bucket':
            
            # get agent static behavior indices for behavior list
            behavior_lst_sell_index = updated_agents[agent]['action_list'].index('trade')
            behavior_lst_utility_index = updated_agents[agent]['action_list'].index('utility')
            behavior_lst_remove_index = updated_agents[agent]['action_list'].index('remove_locked_tokens')

            # get agent static behavior percentages
            selling_perc = updated_agents[agent]['action_weights'][behavior_lst_sell_index]
            utility_perc = updated_agents[agent]['action_weights'][behavior_lst_utility_index]
            remove_perc = updated_agents[agent]['action_weights'][behavior_lst_remove_index]

            # calculate corresponding absolute token amounts for meta buckets
            sold_tokens = updated_agents[agent]['tokens'] * selling_perc/100
            utility_tokens = updated_agents[agent]['tokens'] * utility_perc/100
            removed_tokens = updated_agents[agent]['tokens'] * utility_perc/100
            
            updated_agents[agent]['tokens'] -= (sold_tokens + utility_tokens)

        

    return {'meta_bucket_token_allocations': meta_bucket_token_allocations}


# STATE UPDATE FUNCTIONS
def update_agent_behavior(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent behaviors
    """
    updated_agents = prev_state['agents']
    agent_behavior_dict = policy_input['agent_behavior_dict']

    for key, value in updated_agents.items():
        updated_agents[key]['action_list'] = list(agent_behavior_dict[updated_agents[key]['type']].keys())
        updated_agents[key]['action_weights'] += tuple(agent_behavior_dict[updated_agents[key]['type']].values())

    return ('agents', updated_agents)