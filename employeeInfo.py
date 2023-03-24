import pandas as pd

def minusones(employeeStats, pos):
    if pos == 'Production':
        employeeStats['Emissions']['Plane'] = -1
        employeeStats['Emissions']['Truck'] = -1
        employeeStats['Employment']['Turnover'] = -1
        employeeStats['Governance'] = -1
    elif pos == 'Driver':
        employeeStats['Emissions']['Plane'] = -1
        employeeStats['Water']['Machine'] = -1
        employeeStats['Water']['Graywater'] = -1
        employeeStats['Disposal']['recyclable/ biodegradable'] = -1
        employeeStats['Employment']['Turnover'] = -1
        employeeStats['Governance'] = -1
    elif pos == 'Sales':
        employeeStats['Emissions']['Truck'] = -1
        employeeStats['Disposal']['recyclable/ biodegradable'] = -1
        employeeStats['Employment']['Turnover'] = -1
        employeeStats['Governance'] = -1
    elif pos == 'Manager':
        employeeStats['Emissions']['Truck'] = -1
        employeeStats['Disposal']['recyclable/ biodegradable'] = -1
        employeeStats['Governance']['Diversity'] = -1
    return employeeStats

# Call the functions based on the dictionary values
def PayGrade():
    pass


def kwhPlant():
    pass


def Plane():
    pass


def Commute(df, employee_id):
    employee_df = df.loc[df['employee_id'] == employee_id]
    if not employee_df.empty and 'commute' in employee_df['type'].tolist():
        return 1
    else:
        return 0


def Truck():
    pass


def Machine():
    pass


def Graywater():
    pass


def Leakage(df, employee_id):
    employee_df = df.loc[df['employee_id'] == employee_id]
    if not employee_df.empty and 'leakage' in employee_df['type'].tolist() and '1' in employee_df['output'].tolist():
        return 1
    else:
        return 0


def Packaging(df, factory_id):
    # Calculate the average of "recicled" values based on "factory_id"
    factory_id = 15  # Replace with the desired factory_id
    avg_recicled = df[df['factory_id'] == factory_id]['recicled'].mean()

    # Print the result
    return 0 if avg_recicled < 0.5 else 1


def Foodloss(trashdf, purchasedf, produceddf, fact):
    # calculate the sum of weights for organic trash with factory_id 10
    fact = float(fact)
    organic_trash_sum = trashdf.loc[(trashdf['trash'] == 'organic') & (trashdf['factory_id'] == fact), 'weight'].sum()

    # calculate the sum of kg for purchases with factory_id 10
    purchases_sum = purchasedf.loc[purchasedf['factory_id'] == fact, 'kg'].sum()

    # calculate the sum of kg for productions with factory_id 10
    productions_sum = produceddf.loc[produceddf['factory_id'] == fact, 'kg'].sum()

    # calculate the final result by subtracting the sum of trash and purchases from the sum of productions
    final_result = productions_sum - (organic_trash_sum + purchases_sum)

    return 0 if final_result < 0 else 1


def Nonrecyclable(df, factory_id):
    # Calculate the sum of "weight" for all rows where "trash" equals "non-recycle" and "factory_id" equals the desired value
    non_recycle_weight_sum = df[(df['trash'] == 'non-recycle') & (df['factory_id'] == factory_id)]['weight'].sum()

    # Print the result
    return 0 if non_recycle_weight_sum < 300 else 1


def recyclable_biodegradable():
    pass


def Origin(df, factory_id):
    # Filter the DataFrame to only include rows where "factory_id" equals the desired value
    df = df[df['factory_id'] == factory_id]

    # Group the DataFrame by "origin" and calculate the count of instances for each origin
    origin_counts = df.groupby('origin')['kg'].count()

    # Calculate the final result based on the origin counts
    num_switzerland = origin_counts.get('switzerland', 0)
    num_italy = origin_counts.get('italy', 0)
    num_spain = origin_counts.get('spain', 0)
    num_morocco = origin_counts.get('morocco', 0)

    final_result = (9 * num_switzerland + 7 * num_italy + 4 * num_spain) / (
                num_switzerland + num_italy + num_spain + num_morocco)

    # Print the result
    return 0 if final_result/10<0.4 else 1

def Recommended():
    pass


def Label():
    pass


def Psychologist():
    pass


def Videos(df, id_employee):
    video_hours = df[(df['learning'] == 'video') & (df['id_employee'] == id_employee)]['hours'].sum()

    return 0 if 5>video_hours else 1


def Seminars(df, id_employee):
    seminar_hours = df[(df['learning'] == 'seminar') & (df['id_employee'] == id_employee)]['hours'].sum()

    return 0 if 15>seminar_hours else 1



def HumanRights():
    pass


def Turnover(df, fact):
    count = len(df[(df["Factory_id"] == fact) & (df["Left"] == "31/12/9999")])
    return 0 if count<70 else 1


def ExtraHours():
    pass


def ESG():
    pass


def Ethical():
    pass


def Diversity():
    pass



def dicEmployee(id):
    employeeStats = {
        'Emissions': {
            'kwhPlant': {},
            'Plane': {},
            'Commute': {},
            'Truck': {}
        },
        'Water': {
            'Machine': {},
            'Graywater': {},
            'Leakage': {}
        },
        'Disposal': {
            'Foodloss': {},
            'Packaging': {},
            'Nonrecyclable': {},
            'recyclable/ biodegradable': {}
        },
        'Ecosystems': {
            'Origin': {},
            'Recommended': {}
        },
        'Animalwelfare': {
            'Label': {}
        },
        'Safety': {
            'Psychologist': {},
            'Videos': {},
            'Seminars': {}
        },
        'Employment': {
            'HumanRights': {},
            'Turnover': {},
            'ExtraHours': {}
        },
        'Governance': {
            'ESG': {},
            'Ethical': {},
            'Diversity': {},
            'PayGrade': {}
        }
    }

    dfEmpl = pd.read_csv('employee_data.csv')
    employee_df = dfEmpl.loc[dfEmpl['Id'] == id]
    pos = employee_df['position'].iloc[0]
    fact = employee_df['Factory_id'].iloc[0]
    employeeStats = minusones(employeeStats, pos)
    dfApp = pd.read_csv('app_data.csv')
    trashdf = pd.read_csv('trash_factories.csv')
    purchasedf = pd.read_csv('purchase.csv')
    produceddf = pd.read_csv('produced_food.csv')
    learndf = pd.read_csv('learning.csv')

    for category, values in employeeStats.items():
        if values == -1:
            break
        for key, val in values.items():
            # Check if the value is not -1
            if val != -1:
                # Call the function corresponding to the key
                if key == 'kwhPlant':
                    employeeStats['Emissions']['kwhPlant'] =kwhPlant()
                elif key == 'Plane':
                    employeeStats['Emissions']['Plane'] =Plane()
                elif key == 'Commute':
                    employeeStats['Emissions']['Commute'] =Commute(dfApp, id)
                elif key == 'Truck':
                    employeeStats['Emissions']['Truck'] =Truck()
                elif key == 'Machine':
                    employeeStats['Water']['Machine'] =Machine()
                elif key == 'Graywater':
                    employeeStats['Water']['Graywater'] =Graywater()
                elif key == 'Leakage':
                    employeeStats['Water']['Leakage'] =Leakage(dfApp, id)
                elif key == 'Foodloss':
                    employeeStats['Disposal']['Foodloss'] =Foodloss(trashdf, purchasedf, produceddf, fact)
                elif key == 'Packaging':
                    employeeStats['Disposal']['Packaging'] =Packaging(produceddf, fact)
                elif key == 'Nonrecyclable':
                    employeeStats['Disposal']['Nonrecyclable'] =Nonrecyclable(trashdf, fact)
                elif key == 'recyclable/ biodegradable':
                    employeeStats['Disposal']['recyclable/ biodegradable'] =recyclable_biodegradable()
                elif key == 'Origin':
                    employeeStats['Ecosystems']['Origin'] =Origin(purchasedf, fact)
                elif key == 'Recommended':
                    employeeStats['Ecosystems']['Recommended'] =Recommended()
                elif key == 'Label':
                    employeeStats['Animalwelfare']['Label'] =Label()
                elif key == 'Psychologist':
                    employeeStats['Safety']['Psychologist'] =Psychologist()
                elif key == 'Videos':
                    employeeStats['Safety']['Videos'] =Videos(learndf, id)
                elif key == 'Seminars':
                    employeeStats['Safety']['Seminars'] =Seminars(learndf, id)
                elif key == 'HumanRights':
                    employeeStats['Employment']['HumanRights'] =HumanRights()
                elif key == 'Turnover':
                    employeeStats['Employment']['Turnover'] =Turnover(dfEmpl, fact)
                elif key == 'ExtraHours':
                    employeeStats['Employment']['ExtraHours'] =ExtraHours()
                elif key == 'ESG':
                    employeeStats['Governance']['ESG'] =ESG()
                elif key == 'Ethical':
                    employeeStats['Governance']['Ethical'] =Ethical()
                elif key == 'Diversity':
                    employeeStats['Governance']['Diversity'] =Diversity()
                elif key == 'PayGrade':
                    employeeStats['Governance']['PayGrade'] =PayGrade()
    return employeeStats


