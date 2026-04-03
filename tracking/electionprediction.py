from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD

if __name__ == "__main__":
    model = DiscreteBayesianNetwork([
        ('Weather', 'Election-day Turnout'),
        ('Election-day Turnout', 'Turnout'),
        ('Talarico Ad Campaign', 'Turnout'),
        ('Social Sentiment', 'Policy Sentiment'),
        ('Economic Sentiment', 'Policy Sentiment'),
        ('Economic Sentiment', 'Gallup Confidence Index'),
        ('Policy Sentiment', 'Elected'),
        ('Turnout', 'Elected'),
        ('Unemployment', 'BLS Unemployment Rate'),
        ('Unemployment', 'Economic Sentiment'),
        ('Social Sentiment', 'Immigration Crackdown'),
        ('Popularity', 'GQR Poll'),
        ('Popularity', 'Quantus Poll'),
        ('Popularity', 'Elected')
    ])
    
    model.add_cpds(
        TabularCPD(
            variable="Weather", # Rainy, Sunny
            variable_card=2,
            values=[[0.1], [0.9]],
        ),
        TabularCPD(
            variable="Talarico Ad Campaign", # Don't do it / do it.
            variable_card=2,
            values=[[0.2], [0.8]],
        ),
        TabularCPD(
            variable="Unemployment", # Low / High.
            variable_card=2,
            values=[[0.4], [0.6]],
        ),
        TabularCPD(
            variable="Social Sentiment", # Liberal / Conservative.
            variable_card=2,
            values=[[0.4], [0.6]],
        ),
        TabularCPD(
            variable="Popularity", # Talarico / Paxton.
            variable_card=2,
            values=[[0.6], [0.4]],
        ),
        TabularCPD(
            variable="Election-day Turnout", # Low, High
            variable_card=2,
            values=[[0.5, 0.3],  # Low turnout. For rainy, then sunny.
                    [0.5, 0.7]],
            evidence=["Weather"],
            evidence_card=[2],
        ),
        TabularCPD(
            variable="Turnout", # Democrat, Republican
            variable_card=2,
            values=[[0.4, 0.1, 0.7, 0.4],  # Democrat turnout.
                    [0.6, 0.9, 0.3, 0.6]],
            evidence=["Talarico Ad Campaign", "Election-day Turnout"],
            evidence_card=[2, 2],
        ),
        TabularCPD(
            variable="BLS Unemployment Rate", # Low, High
            variable_card=2,
            values=[[0.9, 0.1],  # Low unemployment. Basically a 90% chance of the poll being correct.
                    [0.1, 0.9]],
            evidence=["Unemployment"],
            evidence_card=[2],
        ),
    )
    
    print(f"Model is valid: {model.check_model()}")
    
    inference = VariableElimination(model)
    print(inference.query(variables=['Elected']))
    print(inference.query(variables=['Elected'], evidence={
        "Weather": 0,
    }))