import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Generate common IDs
n_subjects = 100
id_list = [f'SUBJ{str(i).zfill(3)}' for i in range(1, n_subjects+1)]

# 1. Enhanced Lifestyle Questionnaire Data
diseases = ['Hypertension', 'Diabetes', 'CAD', 'Asthma', 'Hypothyroidism', 'None']
supplements = ['Multivitamin', 'Vitamin D', 'Omega-3', 'Probiotics', 'Calcium', 'None']
family_history = ['Diabetes', 'Hypertension', 'CAD', 'Dementia', 'Cancer', 'None']

lifestyle_data = pd.DataFrame({
    'id': id_list,
    'age': np.random.randint(18, 80, n_subjects),
    'gender': np.random.choice(['Male', 'Female'], n_subjects),
    'height_cm': np.round(np.random.normal(170, 10, n_subjects), 1),
    'weight_kg': np.round(np.random.normal(75, 15, n_subjects), 1),
    'bmi': lambda x: np.round(x.weight_kg / ((x.height_cm/100)**2), 1),
    'waist_circumference_cm': np.round(np.random.normal(90, 15, n_subjects), 1),
    'hip_circumference_cm': np.round(np.random.normal(100, 10, n_subjects), 1),
    'diet': np.random.choice(['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Mediterranean', 'Keto'], n_subjects),
    'alcohol_consumption': np.random.choice(['None', 'Occasional', 'Regular'], n_subjects),
    'smoking_status': np.random.choice(['Never', 'Former', 'Current'], n_subjects),
    'exercise_min_per_week': np.random.randint(0, 300, n_subjects),
    'sleep_hours_per_day': np.round(np.random.uniform(4, 10, n_subjects), 1),
    'stress_level': np.random.randint(1, 10, n_subjects),
    'current_diseases': np.random.choice(diseases, n_subjects),
    'supplements': [', '.join(np.random.choice(supplements, np.random.randint(0, 3))) for _ in range(n_subjects)],
    'family_history': [', '.join(np.random.choice(family_history, np.random.randint(0, 3))) for _ in range(n_subjects)]
})

# 2. Enhanced Scanning Data
scanning_data = pd.DataFrame({
    'id': id_list,
    'fibroscan_kpa': np.round(np.random.uniform(3.5, 18.0, n_subjects), 1),
    'oscilometry_resistance_kpa': np.round(np.random.uniform(0.2, 1.5, n_subjects), 2),
    'oscilometry_reactance_kpa': np.round(np.random.uniform(0.1, 0.8, n_subjects), 2),
    'bca_body_fat_percent': np.round(np.random.uniform(10.0, 40.0, n_subjects), 1),
    'bca_lean_mass_kg': np.round(np.random.normal(50, 10, n_subjects), 1),
    'anthro_waist_hip_ratio': np.round(np.random.uniform(0.7, 1.2, n_subjects), 2),
    'spirometry_fev1': np.round(np.random.normal(3.5, 1.0, n_subjects), 2),
    'spirometry_fvc': np.round(np.random.normal(4.0, 1.2, n_subjects), 2),
    'spirometry_fev1_fvc_ratio': np.round(np.random.uniform(0.7, 0.9, n_subjects), 2),
    'brain_volume_ml': np.round(np.random.normal(1400, 100, n_subjects)),
    'liver_fat_percent': np.round(np.random.uniform(1.0, 15.0, n_subjects), 1),
    'bone_density_hip_gcm2': np.round(np.random.normal(1.0, 0.2, n_subjects), 3)
})

# 3. Comprehensive Blood Biochemistry Data
blood_data = pd.DataFrame({
    'id': id_list,
    'Alkaline_Phosphatase_U_L': np.random.randint(40, 150, n_subjects),
    'TSH_Ultrasensitive_mIU_L': np.round(np.random.lognormal(0, 0.5, n_subjects), 2),
    'APO_B_mg_dL': np.random.randint(50, 150, n_subjects),
    'APO_A1_mg_dL': np.random.randint(100, 200, n_subjects),
    'Absolute_Basophil_Count_cells_uL': np.random.randint(0, 200, n_subjects),
    'Absolute_Eosinophil_Count_cells_uL': np.random.randint(0, 500, n_subjects),
    'Absolute_Lymphocyte_Count_cells_uL': np.random.randint(1000, 4000, n_subjects),
    'Absolute_Monocyte_Count_cells_uL': np.random.randint(200, 1000, n_subjects),
    'Absolute_Neutrophil_Count_cells_uL': np.random.randint(1500, 8000, n_subjects),
    'ALT_SGPT_U_L': np.random.randint(10, 60, n_subjects),
    'Albumin_Globulin_Ratio': np.round(np.random.uniform(0.8, 2.0, n_subjects), 2),
    'AST_SGOT_U_L': np.random.randint(10, 50, n_subjects),
    'Estimated_Glucose_mg_dL': np.random.randint(70, 140, n_subjects),
    'Basophils_percent': np.round(np.random.uniform(0, 2, n_subjects), 1),
    'Blood_Urea_mg_dL': np.random.randint(10, 50, n_subjects),
    'BUN_mg_dL': np.random.randint(5, 25, n_subjects),
    'BUN_Creatinine_Ratio': np.random.randint(10, 20, n_subjects),
    'ESR_mm_hr': np.random.randint(0, 30, n_subjects),
    'Eosinophils_percent': np.round(np.random.uniform(0, 6, n_subjects), 1),
    'Ferritin_ng_mL': np.random.randint(20, 400, n_subjects),
    'GFR_estimated_ml_min': np.random.randint(60, 120, n_subjects),
    'GGT_U_L': np.random.randint(10, 80, n_subjects),
    'Glucose_Fasting_mg_dL': np.random.randint(70, 126, n_subjects),
    'HDL_LDL_Ratio': np.round(np.random.uniform(0.2, 0.6, n_subjects), 2),
    'Hemoglobin_g_dL': np.round(np.random.normal(14, 2, n_subjects), 1),
    'HbA1c_percent': np.round(np.random.uniform(4.5, 8.0, n_subjects), 1),
    'Hematocrit_percent': np.round(np.random.normal(42, 5, n_subjects), 1),
    'LDL_HDL_Ratio': np.round(np.random.uniform(1.5, 4.0, n_subjects), 1),
    'Lymphocytes_percent': np.random.randint(20, 50, n_subjects),
    'MPV_fL': np.round(np.random.uniform(7.5, 11.5, n_subjects), 1),
    'MCH_pg': np.random.randint(26, 34, n_subjects),
    'MCHC_g_dL': np.random.randint(32, 36, n_subjects),
    'MCV_fL': np.random.randint(80, 100, n_subjects),
    'Monocytes_percent': np.random.randint(2, 10, n_subjects),
    'Neutrophils_percent': np.random.randint(40, 80, n_subjects),
    'Non_HDL_Cholesterol_mg_dL': np.random.randint(100, 200, n_subjects),
    'Platelet_Count_x10e3_uL': np.random.randint(150, 450, n_subjects),
    'RDW_CV_percent': np.round(np.random.uniform(11.5, 15.0, n_subjects), 1),
    'RBC_Count_x10e6_uL': np.round(np.random.normal(4.7, 0.5, n_subjects), 2),
    'SGOT_SGPT_Ratio': np.round(np.random.uniform(0.8, 1.5, n_subjects), 2),
    'Serum_Albumin_g_dL': np.round(np.random.normal(4.0, 0.5, n_subjects), 1),
    'Serum_Bilirubin_Direct_mg_dL': np.round(np.random.uniform(0.1, 0.4, n_subjects), 2),
    'Serum_Bilirubin_Total_mg_dL': np.round(np.random.uniform(0.2, 1.2, n_subjects), 2),
    'Serum_Calcium_mg_dL': np.round(np.random.normal(9.5, 0.5, n_subjects), 1),
    'Serum_Chloride_mEq_L': np.random.randint(95, 110, n_subjects),
    'Serum_Creatinine_mg_dL': np.round(np.random.uniform(0.6, 1.3, n_subjects), 2),
    'Serum_Globulin_g_dL': np.round(np.random.normal(2.5, 0.5, n_subjects), 1),
    'Serum_HDL_Cholesterol_mg_dL': np.random.randint(35, 80, n_subjects),
    'Serum_Iron_ug_dL': np.random.randint(50, 180, n_subjects),
    'Serum_LDL_Cholesterol_mg_dL': np.random.randint(70, 180, n_subjects),
    'Serum_Phosphorus_mg_dL': np.round(np.random.uniform(2.5, 4.5, n_subjects), 1),
    'Serum_Potassium_mEq_L': np.round(np.random.normal(4.0, 0.5, n_subjects), 1),
    'Serum_Sodium_mEq_L': np.random.randint(135, 145, n_subjects),
    'Serum_TIBC_ug_dL': np.random.randint(250, 450, n_subjects),
    'Serum_Total_Protein_g_dL': np.round(np.random.normal(7.0, 0.6, n_subjects), 1),
    'Serum_Triglycerides_mg_dL': np.random.randint(50, 200, n_subjects),
    'Serum_Uric_Acid_mg_dL': np.round(np.random.uniform(3.0, 7.0, n_subjects), 1),
    'Serum_VLDL_Cholesterol_mg_dL': np.random.randint(5, 40, n_subjects),
    'Total_Cholesterol_HDL_Ratio': np.round(np.random.uniform(3.0, 6.0, n_subjects), 1),
    'Total_Cholesterol_mg_dL': np.random.randint(150, 250, n_subjects),
    'Total_Leukocyte_Count_x10e3_uL': np.round(np.random.normal(7.0, 2.0, n_subjects), 1),
    'Transferrin_Saturation_percent': np.random.randint(20, 50, n_subjects),
    'UIBC_ug_dL': np.random.randint(150, 375, n_subjects),
    'Urea_Creatinine_Ratio': np.random.randint(10, 20, n_subjects),
    'Vitamin_B12_pg_mL': np.random.randint(200, 900, n_subjects),
    'Vitamin_D_25_OH_ng_mL': np.random.randint(10, 60, n_subjects)
})

# 4. Gut Microbiome Data
genera = [
    'Bacteroides', 'Faecalibacterium', 'Bifidobacterium', 
    'Roseburia', 'Eubacterium', 'Akkermansia',
    'Prevotella', 'Ruminococcus', 'Clostridium',
    'Lactobacillus'
]
microbiome_data = pd.DataFrame(
    np.random.dirichlet(np.ones(10), size=n_subjects).round(4),
    columns=genera
)
microbiome_data.insert(0, 'id', id_list)

# 5. Proteomics Data
proteins = [
    'C-reactive Protein (CRP)', 'Interleukin-6 (IL-6)',
    'Tumor Necrosis Factor-alpha (TNF-a)',
    'Insulin-like Growth Factor 1 (IGF-1)',
    'Leptin', 'Adiponectin', 'Fibrinogen',
    'Brain-derived Neurotrophic Factor (BDNF)',
    'Vascular Endothelial Growth Factor (VEGF)',
    'C-peptide'
]
proteomics_data = pd.DataFrame({
    'id': id_list,
    **{protein: np.random.lognormal(mean=3, sigma=1, size=n_subjects).round(2) 
       for protein in proteins}
})

# 6. Metabolomics Data
metabolites = [
    'Glucose', 'Lactate', 'Pyruvate', 'Alanine',
    'Glutamine', 'Glutamate', 'Citrate', 'Succinate',
    'Acetate', 'Butyrate', 'Propionate', 'Valine',
    'Leucine', 'Isoleucine', 'Phenylalanine', 'Tyrosine'
]
metabolomics_data = pd.DataFrame({
    'id': id_list,
    **{metabolite: np.random.gamma(shape=2, scale=1.5, size=n_subjects).round(4)
       for metabolite in metabolites}
})

# 7. Metallomics Data
metals = [
    'Iron_ug_L', 'Zinc_ug_L', 'Copper_ug_L', 
    'Selenium_ug_L', 'Magnesium_mg_L',
    'Calcium_mg_L', 'Potassium_mg_L', 'Sodium_mg_L'
]
metallomics_data = pd.DataFrame({
    'id': id_list,
    **{metal: np.random.lognormal(mean=2, sigma=0.5, size=n_subjects).round(2)
       for metal in metals}
})

# 8. Lipidomics Data
lipids = [
    'PC(32:0)', 'PE(18:0/20:4)', 'TG(16:0/18:1/18:2)',
    'SM(d18:1/16:0)', 'Cer(d18:1/24:0)', 'LPC(18:0)',
    'LPE(18:1)', 'DG(36:2)', 'CE(18:1)'
]
lipidomics_data = pd.DataFrame({
    'id': id_list,
    **{lipid: np.random.exponential(scale=1e4, size=n_subjects).round(2) 
       for lipid in lipids}
})

# 9. Immuno and Biochemistry Biomarkers
immuno_data = pd.DataFrame({
    'id': id_list,
    'CD4_Count_cells_uL': np.random.randint(300, 1500, n_subjects),
    'CD8_Count_cells_uL': np.random.randint(200, 1000, n_subjects),
    'CD4_CD8_Ratio': np.round(np.random.uniform(0.5, 3.0, n_subjects), 2),
    'IgG_mg_dL': np.random.randint(700, 1600, n_subjects),
    'IgA_mg_dL': np.random.randint(70, 400, n_subjects),
    'IgM_mg_dL': np.random.randint(40, 230, n_subjects),
    'IgE_IU_mL': np.random.randint(0, 200, n_subjects),
    'C3_mg_dL': np.random.randint(90, 180, n_subjects),
    'C4_mg_dL': np.random.randint(10, 40, n_subjects),
    'ANA_Titer': np.random.choice(['Negative', '1:40', '1:80', '1:160'], n_subjects),
    'RF_IU_mL': np.random.randint(0, 20, n_subjects),
    'Anti_CCP_U_mL': np.random.randint(0, 30, n_subjects),
    'CRP_mg_L': np.round(np.random.uniform(0.1, 10.0, n_subjects), 1),
    'ESR_mm_hr': np.random.randint(0, 30, n_subjects),
    'Ferritin_ng_mL': np.random.randint(20, 400, n_subjects),
    'Vitamin_B12_pg_mL': np.random.randint(200, 900, n_subjects),
    'Vitamin_D_ng_mL': np.random.randint(10, 60, n_subjects),
    'Homocysteine_umol_L': np.round(np.random.uniform(5.0, 15.0, n_subjects), 1)
})

# Save all data to CSV files
lifestyle_data.to_csv('data/example/lifestyle_data.csv', index=False)
scanning_data.to_csv('data/example/scanning_data.csv', index=False)
blood_data.to_csv('data/example/blood_biochemistry.csv', index=False)
microbiome_data.to_csv('data/example/gut_microbiome.csv', index=False)
proteomics_data.to_csv('data/example/proteomics_data.csv', index=False)
metabolomics_data.to_csv('data/example/metabolomics_data.csv', index=False)
metallomics_data.to_csv('data/example/metallomics_data.csv', index=False)
immuno_data.to_csv('data/example/immuno_biochemistry.csv', index=False)
# Note: The data generation process is random and may not reflect real-world distributions.
# The CSV files will be saved in the current working directory.