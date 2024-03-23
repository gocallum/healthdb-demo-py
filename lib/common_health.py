import random

def generate_australian_gp_name():
    # Predefined GP practice names to simulate real names. You can add more or adjust as needed.
    predefined_names = [
        "Harbour City Medical Centre",
        "Springfield General Practice",
        "Green Valley Family Clinic",
        "Oceanview Medical Practice",
        "Mountain Ridge Health Centre",
        "Riverbank Family Health",
        "Sunnybank Community Clinic",
        "Bayview Medical Associates",
        "Outback Health Services",
        "Coastline Primary Care",
        "Blue Mountains Medical Group",
        "Gold Coast Health Partners",
        "Urban Wellness Clinic",
        "Coral Sea Healthcare",
        "Desert Springs Medical Practice",
        "Rainforest Medical Network",
        "Sunshine State Health Centre",
        "Great Barrier Reef Medical Clinic",
        "Red Centre Family Practice",
        "Tropical North Health Services",
        "Southern Cross Medical Care",
        "East Coast Family Medicine",
        "West End Medical Practice",
        "Northern Rivers Healthcare",
        "Surfside Community Health"
    ]
    # Append a state abbreviation to make it more specific
    return random.choice(predefined_names)


def generate_healthcare_concern():
    # Predefined list of healthcare concern templates
    healthcare_concerns = [
        "Patient has a broken shoulder.",
        "Complaints of chronic back pain.",
        "Suspected case of viral infection.",
        "Experiencing severe migraines.",
        "Requires evaluation for possible diabetes.",
        "Symptoms suggest acute bronchitis.",
        "High blood pressure needing management.",
        "Potential allergic reaction identified.",
        "Injury from a recent fall.",
        "Consultation for anxiety and depression.",
        "Routine check-up for heart disease risk.",
        "Follow-up on previous surgical procedure.",
        "Early signs of osteoporosis observed.",
        "Assessment for autoimmune diseases.",
        "Examination for skin rash and eczema.",
        "Concerns regarding childhood vaccinations.",
        "Dental pain and possible cavity.",
        "Screening for breast cancer.",
        "Evaluating nutritional deficiencies.",
        "Symptoms of sleep disorders.",
        "Review of medication side effects.",
        "Consultation requested for weight management.",
        "Testing for thyroid function abnormalities.",
        "Consideration for vision and eye health.",
        "Hearing loss and tinnitus evaluation.",
        "Chronic fatigue and possible fibromyalgia.",
        "Pregnancy check-up and prenatal care.",
        "Suspected gastrointestinal issues.",
        "Investigation into frequent headaches.",
        "Concerns about aging and memory loss.",
        "Fitness assessment for sports participation.",
        "Risk assessment for genetic conditions.",
        "Evaluation for chronic kidney disease.",
        "Symptoms of urinary tract infection.",
        "Monitoring for liver function abnormalities.",
        "Assessment for reproductive health issues.",
        "Concerns about vitamin D deficiency.",
        "Possible concussion from recent head injury.",
        "Screening for prostate cancer.",
        "Consultation for sleep apnea.",
        "Evaluation of joint pain for arthritis.",
        "Treatment options for acid reflux and GERD.",
        "Investigation of unexplained weight loss.",
        "Check-up for asthma control and management.",
        "Preventive vaccination for seasonal flu.",
        "Assessment for attention deficit hyperactivity disorder.",
        "Counseling for stress management and burnout.",
        "Diagnostic testing for Lyme disease.",
        "Management of menopause symptoms.",
        "Follow-up on abnormal blood test results.",
        "Therapy options for chronic sinusitis.",
        "Pre-operative evaluation for elective surgery.",
        "",  # Represents a potential for no specific concern listed
    ]

    # Randomly select from the predefined list
    return random.choice(healthcare_concerns)

def generate_comorbidity():
    comorbidity_options = [
        "Hypertension",
        "Type 2 Diabetes Mellitus",
        "Chronic Obstructive Pulmonary Disease (COPD)",
        "Asthma",
        "Obesity",
        "Ischemic Heart Disease",
        "Chronic Kidney Disease",
        "Major Depressive Disorder",
        "Generalized Anxiety Disorder",
        "Osteoarthritis",
        "Rheumatoid Arthritis",
        "Hyperlipidemia",
        "None"  # Represents no comorbidity
    ]
    # Choose one or more comorbidities randomly. Here, we're choosing one for simplicity.
    # To select multiple, you could use random.sample(comorbidity_options, k=number_of_comorbidities) with k > 1
    return random.choice(comorbidity_options)





def get_target_organisation_name():
    specialist_clinics = [
        "Sydney Cardiology Group",
        "Melbourne Neurology Centre",
        "Brisbane Orthopedics Clinic",
        "Perth Paediatrics Practice",
        "Adelaide Oncology Associates",
        "Canberra Radiology Network",
        "Gold Coast Emergency Specialists",
        "Hobart Endocrinology & Diabetes Service",
        "Darwin Gastroenterology Group",
        "Sunshine Coast Rheumatology Clinic",
        "Geelong Pulmonary and Sleep Medicine",
        "Cairns Allergy Clinic",
        "Alice Springs Pain Management Center",
        "Townsville Dermatology Clinic",
        "Launceston Urology Practice",
        "Bendigo Women's Health Institute",
        "Toowoomba Cardiac Centre",
        "Mackay Mental Health Services",
        "Rockhampton Eye Clinic",
        "Wollongong ENT Specialists"
    ]
    return random.choice(specialist_clinics)
