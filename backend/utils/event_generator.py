import random

def generate_event(player_state, context):
    """Generates a dynamic event based on player actions, world conditions, and reputation."""
    world_events = [
        "A rogue AI escapes containment, causing disruptions in the city grid.",
        "A black-market cyberware deal goes wrong, sparking a deadly shootout.",
        "Corporate enforcers launch a brutal crackdown in response to underground resistance.",
        "A mysterious data leak exposes corruption within high-ranking factions."
    ]
    
    player_triggered_events = [
        "Your latest actions have drawn unwanted attention from a powerful syndicate.",
        "A bounty has been quietly placed on your head, attracting mercenary interest.",
        "An ally warns you of an impending betrayal within your ranks.",
        "A rival faction attempts to sabotage your operations, forcing you to respond."
    ]
    
    environmental_events = [
        "A city-wide blackout plunges entire districts into chaos.",
        "Unrest erupts as rioters take to the streets, protesting corporate control.",
        "A sudden cyberattack cripples key communication networks.",
        "Police and corporate security increase patrols due to recent violence."
    ]
    
    rare_events = [
        "A hidden underground market is rumored to have resurfaced.",
        "An unknown hacker group offers you a lucrative, yet dangerous job.",
        "You stumble upon a long-abandoned data vault filled with encrypted secrets.",
        "A powerful AI entity contacts you with an enigmatic request."
    ]
    
    faction_specific_events = {
        "corporate": [
            "A megacorp CEO is rumored to be planning a hostile takeover.",
            "A corporate espionage mission goes wrong, and you're caught in the middle."
        ],
        "syndicate": [
            "A crime syndicate declares war on a rival faction, pulling you into the crossfire.",
            "A high-ranking syndicate boss offers you a dangerous but rewarding contract."
        ],
        "resistance": [
            "Underground rebels plan a major assault on a corporate stronghold.",
            "A resistance leader requests your help in smuggling vital supplies."
        ]
    }
    
    faction_diplomacy_shifts = [
        "A fragile alliance between two factions begins to crumble, increasing tensions.",
        "A surprising peace treaty is signed, changing the balance of power.",
        "A faction secretly negotiates with a rival, plotting against a common enemy."
    ]
    
    underground_intelligence_networks = [
        "A shadowy information broker offers you classified data—for a price.",
        "A hidden surveillance network is uncovered, revealing faction secrets.",
        "Underground spies infiltrate high-profile organizations, seeking leverage."
    ]
    
    covert_operations = [
        "An elite black ops unit is dispatched on a secret mission, altering faction power dynamics.",
        "A covert cyber-assault targets a faction’s mainframe, compromising valuable intel.",
        "You receive an encrypted message offering a high-risk stealth mission."
    ]
    
    assassination_missions = [
        "A faction offers you a contract to eliminate a high-value target.",
        "A political assassination shakes up the corporate hierarchy.",
        "A legendary assassin is rumored to be hunting a major faction leader."
    ]
    
    black_market_influence = [
        "A power struggle in the black market shifts control over valuable resources.",
        "A new supplier floods the market with high-tech contraband, affecting faction economies.",
        "A powerful fixer orchestrates an underground arms deal with global consequences."
    ]
    
    player_reputation_events = {
        "hero": [
            "Civilians rally around you, treating you as a symbol of hope.",
            "A faction leader offers you exclusive access to top-tier resources."
        ],
        "neutral": [
            "Merchants cautiously approach you with high-stakes deals.",
            "Fixers debate whether you can be trusted with sensitive jobs."
        ],
        "villain": [
            "Bounty hunters begin tracking your movements.",
            "Your reputation as a ruthless operator earns you a powerful, yet dangerous ally."
        ]
    }
    
    event_chain = {
        "hack": [
            "Your latest hack reveals a deeper conspiracy that requires further investigation.",
            "Your digital intrusion triggers an AI countermeasure that starts hunting you."
        ],
        "heist": [
            "A previous robbery puts you on the radar of corporate security forces.",
            "Your stolen tech attracts the attention of a shadowy underground collector."
        ]
    }
    
    dynamic_event_scaling = {
        "low": ["Minor street altercations break out but are quickly contained.", "A small-time fixer gets arrested, shaking up the market."],
        "medium": ["A faction expands its influence, taking control of a contested district.", "An underground fighting ring gains popularity, attracting attention from authorities."],
        "high": ["Full-scale riots erupt, overwhelming corporate security forces.", "A faction declares open war, reshaping the power structure of the city."]
    }
    
    ai_generated_consequences = [
        "An AI-generated prediction warns of an imminent cyberwarfare escalation.",
        "A rogue AI faction begins manipulating financial markets in real-time.",
        "AI-driven corporate security adapts to new threats, making future heists more difficult."
    ]
    
    faction_upheavals = [
        "A power struggle within a major faction leads to a leadership change.",
        "A faction's betrayal of an ally sparks a brutal civil war.",
        "A hidden faction emerges, challenging the established order."
    ]
    
    event_list = (world_events + player_triggered_events + environmental_events + rare_events +
                  faction_diplomacy_shifts + underground_intelligence_networks +
                  covert_operations + assassination_missions + black_market_influence)
    
    if context in faction_specific_events:
        event_list += faction_specific_events[context]
    
    if player_state.get("reputation_status") in player_reputation_events:
        event_list += player_reputation_events[player_state["reputation_status"]]
    
    if player_state.get("recent_action") in event_chain:
        event_list += event_chain[player_state["recent_action"]]
    
    event_list += dynamic_event_scaling[random.choice(["low", "medium", "high"])]
    event_list += ai_generated_consequences
    event_list += faction_upheavals
    
    return random.choice(event_list)

if __name__ == "__main__":
    player_state = {"reputation_status": random.choice(["hero", "neutral", "villain"]), "recent_action": random.choice(["hack", "heist", "none"])}
    context = random.choice(["combat", "trade", "exploration", "dialogue", "general", "corporate", "syndicate", "resistance"])
    print(f"Generated Event: {generate_event(player_state, context)}")
