# POLICY FUNCTIONS
def staking_liquidity_mining_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent liquidity mining
    """
    # get parameters
    liquidity_mining_apr = params['liquidity_mining_apr']/100
    liquidity_mining_share = params['lock_share']/100
    
    # get state variables
    agents = prev_state['agents'].copy()
    utility_removal_perc = prev_state['token_economy']['te_remove_perc']/100

    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_removal_sum = 0
    agent_utility_rewards_sum = 0
    agents_liquidity_mining_allocations = {}
    agents_liquidity_mining_removal = {}
    agents_liquidity_mining_rewards = {}

    # calculate the staking apr token allocations and removals for each agent
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens'] # get the new agent utility token allocations from vesting, airdrops, and incentivisation
        tokens_apr_locked_cum = agents[agent]['a_tokens_liquidity_mining_cum'] # get amount of staked tokens for base apr from last timestep
        
        agents_liquidity_mining_allocations[agent] = utility_tokens * liquidity_mining_share # calculate the amount of tokens that shall be allocated to the staking apr utility from this timestep
        agents_liquidity_mining_removal[agent] = tokens_apr_locked_cum * utility_removal_perc # calculate the amount of tokens that shall be removed from the staking apr utility for this timestep based on the tokens allocated in the previous timestep
        agents_liquidity_mining_rewards[agent] = agents_liquidity_mining_allocations[agent] * liquidity_mining_apr/12 # calculate the amount of tokens that shall be rewarded to the agent for staking
        
        agent_utility_sum += agents_liquidity_mining_allocations[agent] # sum up the total amount of tokens allocated to the staking apr utility for this timestep
        agent_utility_removal_sum += agents_liquidity_mining_removal[agent] # sum up the total amount of tokens removed from the staking apr utility for this timestep
        agent_utility_rewards_sum += agents_liquidity_mining_rewards[agent] # sum up the total amount of tokens rewarded to the agent for staking for this timestep

    return {'agents_liquidity_mining_allocations': agents_liquidity_mining_allocations,'agents_liquidity_mining_removal':agents_liquidity_mining_removal,
            'agents_liquidity_mining_rewards': agents_liquidity_mining_rewards, 'agent_utility_sum': agent_utility_sum,
            'agent_utility_removal_sum': agent_utility_removal_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum}



# STATE UPDATE FUNCTIONS
def update_agents_after_liquidity_mining(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent liquidity mining allocations
    """
    # get parameters
    liquidity_mining_payout_source = params['liquidity_mining_payout_source']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_staking_apr_allocations = policy_input['agents_liquidity_mining_allocations']
    agents_staking_apr_removal = policy_input['agents_liquidity_mining_removal']
    agents_staking_apr_rewards = policy_input['agents_liquidity_mining_rewards']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_tokens_liquidity_mining'] = (agents_staking_apr_allocations[agent] - agents_staking_apr_removal[agent])
        updated_agents[agent]['a_tokens_liquidity_mining_cum'] += (agents_staking_apr_allocations[agent] - agents_staking_apr_removal[agent])
        updated_agents[agent]['a_tokens_liquidity_mining_remove'] = agents_staking_apr_removal[agent]
        updated_agents[agent]['a_tokens'] += agents_staking_apr_rewards[agent]

        # subtract tokens from payout source agent
        if updated_agents[agent]['a_name'].lower() in liquidity_mining_payout_source.lower():
            updated_agents[agent]['a_tokens'] -= agent_utility_rewards_sum

    return ('agents', updated_agents)



def update_utilties_after_liquidity_mining(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta liquidity mining allocations
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_removal_sum = policy_input['agent_utility_removal_sum']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    updated_utilities['u_liquidity_mining_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_liquidity_mining_allocation'] = (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_liquidity_mining_allocation_cum'] += (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_liquidity_mining_allocation_remove'] = agent_utility_removal_sum

    return ('utilities', updated_utilities)