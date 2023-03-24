# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 06:50:47 2023

@author: pacos
"""
from flask import Flask, request, jsonify
from datetime import timedelta, date


app = Flask(__name__)

# ... (keep existing calculate_ecological_footprint function)

def calculate_ecological_footprint(data):
    # Add your custom logic for calculating ecological footprint based on the 8 criteria
    # For demonstration purposes, we will return dummy results.
    return {
        "greenhouse_gas_emissions_and_energy": 0.8,
        "water": 0.7,
        "disposal_and_recycling": 0.9,
        "ecosystems": 0.85,
        "animal_welfare": 0.75,
        "safety_and_health_in_workplace": 0.95,
        "conditions_of_employment": 0.9,
        "governance": 0.8,
    }



@app.route("/api/v1/footprint", methods=["GET"])
def footprint():
    try:
        value = request.args.get("value")
        # Validate input data (you can add your custom validation logic here)
        
        # Calculate ecological footprint based on the input data
        footprint = calculate_ecological_footprint(value)

        return jsonify({"success": True, "footprint": footprint})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/v1/emissions", methods=["GET"])
def emissions():
    try:
        energy_consumption = float(request.args.get("energy_consumption"))
        renewable_percentage = float(request.args.get("renewable_percentage"))
        non_renewable_percentage = 1 - renewable_percentage

        # Simplified calculation: Assume 1 kWh of non-renewable energy generates 0.5 kg CO2 emissions
        co2_emissions = energy_consumption * non_renewable_percentage * 0.5

        return jsonify({"success": True, "co2_emissions": co2_emissions})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/v1/water", methods=["GET"])
def water():
    try:
        water_consumption = float(request.args.get("water_consumption"))
        risk_area_percentage = float(request.args.get("risk_area_percentage"))

        # Simplified calculation: Assume risk area water consumption as critical
        critical_water_consumption = water_consumption * risk_area_percentage

        return jsonify({"success": True, "critical_water_consumption": critical_water_consumption})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/v1/recycling", methods=["GET"])
def recycling():
    try:
        waste_generated = float(request.args.get("waste_generated"))
        recyclable_percentage = float(request.args.get("recyclable_percentage"))

        # Simplified calculation: Recyclable waste amount
        recyclable_waste = waste_generated * recyclable_percentage

        return jsonify({"success": True, "recyclable_waste": recyclable_waste})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/v1/ecosystems", methods=["GET"])
def ecosystems():
    try:
        raw_materials = float(request.args.get("raw_materials"))
        deforestation_free_percentage = float(request.args.get("deforestation_free_percentage"))

        # Simplified calculation: Deforestation-free raw materials amount
        deforestation_free_materials = raw_materials * deforestation_free_percentage

        return jsonify({"success": True, "deforestation_free_materials": deforestation_free_materials})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/api/v1/animal_welfare", methods=["GET"])
def animal_welfare():
    try:
        animal_products = float(request.args.get("animal_products"))
        certified_percentage = float(request.args.get("certified_percentage"))

        # Simplified calculation: Certified animal products amount
        certified_animal_products = animal_products * certified_percentage
        
        return jsonify({"success": True, "certified_animal_products": certified_animal_products})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
        
        
@app.route("/api/v1/workplace_safety", methods=["GET"])
def workplace_safety():
    try:
        employees = int(request.args.get("employees"))
        trained_percentage = float(request.args.get("trained_percentage"))
        
        # Simplified calculation: Number of employees trained in safety and health
        trained_employees = int(employees * trained_percentage)

        return jsonify({"success": True, "trained_employees": trained_employees})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
    
    
@app.route("/api/v1/employment_conditions", methods=["GET"])
def employment_conditions():
    try:
        suppliers = int(request.args.get("suppliers"))
        audited_percentage = float(request.args.get("audited_percentage"))
        
        # Simplified calculation: Number of suppliers with valid social standard audit/certificate
        audited_suppliers = int(suppliers * audited_percentage)
    
        return jsonify({"success": True, "audited_suppliers": audited_suppliers})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/api/v1/governance", methods=["GET"])
def governance():
    try:
        total_investments = float(request.args.get("total_investments"))
        esg_percentage = float(request.args.get("esg_percentage"))  
        
        # Simplified calculation: Amount of investments incorporating ESG criteria
        esg_investments = total_investments * esg_percentage
    
        return jsonify({"success": True, "esg_investments": esg_investments})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
    
@app.route("/api/v1/overshoot_day", methods=["GET"])
def overshoot_day():
    try:
        ecological_footprint = float(request.args.get("ecological_footprint"))
        biocapacity = float(request.args.get("biocapacity"))

        if biocapacity == 0:
            return jsonify({"success": False, "message": "Biocapacity cannot be zero."})

        # Simplified calculation: (Ecological Footprint / Biocapacity) * Days in a Year
        overshoot_ratio = ecological_footprint / biocapacity
        overshoot_day = int(overshoot_ratio * 365)
        overshoot_date = date.today().replace(month=1, day=1) + timedelta(days=overshoot_day)

        return jsonify({"success": True, "overshoot_day": overshoot_day, "overshoot_date": overshoot_date.isoformat()})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



if __name__ == "__main__":
    app.run(debug=True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
