#!/usr/bin/env python3
"""
Autoresearch benchmark for deduplicate() optimization.
Generates 1000 papers with realistic dedup scenarios, measures timing.

Design:
- 600 papers with unique DOI + PMID (unique by DOI)
- 100 papers with duplicate DOI (dedup by DOI)
- 50 papers with unique PMID, no DOI (unique by PMID)
- 50 papers with duplicate PMID (dedup by PMID)
- 50 papers with distinct titles, no IDs (unique by title)
- 50 papers with exact duplicate titles (dedup by SequenceMatcher == 1.0)
- 100 papers with distinct topics, no IDs (unique by title)

Total unique expected: 600 + 50 + 50 + 100 = 800
Total dups expected: 100 + 50 + 50 = 200
"""

import time
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resources.scoring import deduplicate

N_RUNS = 5
random.seed(42)

papers: list[dict] = []

# ---------------------------------------------------------------------------
# 600 papers with unique DOI + PMID
# ---------------------------------------------------------------------------
for i in range(600):
    doi = f"10.1234/unique_{i:04d}"
    pmid = str(10000000 + i)
    title = f"Paper with DOI {i} about head and neck cancer outcomes"
    papers.append({"doi": doi, "pmid": pmid, "title": title})

# ---------------------------------------------------------------------------
# 100 papers that are EXACT DOI duplicates of the first 100
# ---------------------------------------------------------------------------
for i in range(100):
    doi = f"10.1234/unique_{i:04d}"
    papers.append({"doi": doi, "pmid": None, "title": f"DOI duplicate of paper {i}"})

# ---------------------------------------------------------------------------
# 50 papers with unique PMID only (no DOI)
# ---------------------------------------------------------------------------
pmid_only_titles = [
    "Voice handicap in laryngectomees using electrolarynx",
    "Quality of life after total laryngectomy: prospective cohort",
    "Telepractice for voice therapy outcomes in HNC survivors",
    "Swallowing function after transoral robotic surgery for OPSCC",
    "Depression and anxiety in patients awaiting laryngectomy",
]
for i, t in enumerate(pmid_only_titles):
    for copy in range(10):
        pmid = str(20000000 + i * 10 + copy)
        papers.append({"doi": None, "pmid": pmid, "title": t})

# ---------------------------------------------------------------------------
# 50 papers that are PMID duplicates of the 50 above
# ---------------------------------------------------------------------------
for i, t in enumerate(pmid_only_titles):
    for copy in range(10):
        pmid = str(20000000 + i * 10 + copy)
        papers.append({"doi": None, "pmid": pmid, "title": f"PMID duplicate of: {t}"})

# ---------------------------------------------------------------------------
# 50 papers with distinct titles (no DOI/PMID)
# ---------------------------------------------------------------------------
title_only_unique = [
    "Acoustic analysis of tracheoesophageal speech after total laryngectomy",
    "Validation of the SECEL questionnaire in Chilean laryngectomy patients",
    "Electrolarynx speech enhancement using deep convolutional neural networks",
    "Caregiver communication burden in head and neck cancer: qualitative study",
    "Patterns of recurrence after transoral laser microsurgery for T1-T2 glottic cancer",
    "Machine learning for automated detection of dysphonia in HNC survivors",
    "Voice restoration outcomes: TEP versus electrolarynx in developing countries",
    "Social participation and community reintegration after total laryngectomy",
    "Comparing VHI-10 and VRQOL in post-treatment HNC patients",
    "Mobile health interventions for symptom monitoring in HNC radiotherapy",
    "Dysphagia-related quality of life after chemoradiotherapy for NPC",
    "Augmentative and alternative communication needs in acute care settings",
    "Voice prosthesis device life: retrospective analysis of 500 patients",
    "Psychological distress trajectories in newly diagnosed HNC patients",
    "Cough effectiveness and airway clearance after total laryngectomy",
    "Clinical practice guidelines for voice rehabilitation in HNC: systematic review",
    "Barriers to speech therapy access in rural HNC populations",
    "Photographic documentation of stoma care complications after laryngectomy",
    "Patient-clinician communication preferences in advanced HNC decision-making",
    "Occupational voice use after partial laryngectomy: longitudinal study",
    "Speech recognition accuracy for alaryngeal speech: commercial ASR evaluation",
    "Nutrition impact symptoms and dietary intake during HNC radiotherapy",
    "Shared decision-making tools for laryngectomy surgical candidates",
    "Telepractice feasibility for post-laryngectomy voice therapy in Chile",
    "Cross-cultural adaptation of the SHI for Spanish-speaking HNC survivors",
    "Multidimensional assessment of communication participation in HNC",
    "Risk factors for pharyngocutaneous fistula after salvage laryngectomy",
    "Prosthetic rehabilitation timing after total laryngectomy: cohort study",
    "Voice-related workplace limitations in HNC survivors returning to work",
    "Speech intelligibility assessment using automatic speech recognition systems",
    "Laryngectomy tube weaning protocols: a Delphi consensus study",
    "Family-centered communication intervention for HNC caregiver-patient dyads",
    "Functional outcomes after near-total laryngectomy: twenty-year experience",
    "Neural plasticity in the speech motor system after laryngectomy: fMRI evidence",
    "Automated analysis of connected speech samples in alaryngeal speakers",
    "Peer mentoring for communication confidence in laryngectomy support groups",
    "Alternative text input methods for AAC in motor neuron disease",
    "Graft-versus-host disease manifestations in the oral cavity after stem cell transplant",
    "Intraoperative nerve monitoring during thyroid surgery for voice preservation",
    "Voice changes in professional singers after thyroidectomy: perceptual analysis",
    "Radiological predictors of swallowing dysfunction after radiotherapy for HNC",
    "Open-source toolkit for acoustic analysis of pathological voices",
    "Economic evaluation of voice rehabilitation programs after laryngectomy",
    "Development of a communication needs assessment tool for HNC patients",
    "Vocal fold vibration analysis using high-speed videoendoscopy",
    "Electropalatography for articulation therapy in glossectomy patients",
    "Burnout and compassion fatigue in speech-language pathologists working in oncology",
    "Culturally responsive telepractice for Hispanic HNC patients and families",
    "Intelligent voice assistant customization for users with speech impairments",
    "Biofeedback-enhanced swallowing therapy for post-radiotherapy dysphagia",
]
for t in title_only_unique:
    papers.append({"doi": None, "pmid": None, "title": t})

# ---------------------------------------------------------------------------
# 50 papers that are EXACT title duplicates of the 50 above (no IDs)
# ---------------------------------------------------------------------------
for t in title_only_unique:
    papers.append({"doi": None, "pmid": None, "title": t})

# ---------------------------------------------------------------------------
# 100 papers with fully unique topics (no DOI/PMID, diverse titles)
# ---------------------------------------------------------------------------
diverse_topics = [
    "Acoustic analysis of voice after partial laryngectomy",
    "Swallowing outcomes in oropharyngeal cancer survivors",
    "Telepractice for voice therapy in head and neck cancer",
    "Electrolarynx speech intelligibility with deep learning enhancement",
    "Patient-reported outcomes after transoral robotic surgery",
    "Caregiver burden in advanced head and neck cancer",
    "Nutritional interventions during radiotherapy for HNC",
    "Social participation after total laryngectomy",
    "Mobile health apps for cancer survivor self-management",
    "AI for early detection of oral cancer",
    "Fatigue during chemoradiotherapy for HNC",
    "Voice restoration with TEP: long-term outcomes",
    "Sarcopenia and treatment tolerance in elderly HNC",
    "Dysphagia screening in head and neck oncology",
    "Telemedicine follow-up for laryngectomized patients",
    "Speech perception in noise for alaryngeal speakers",
    "Health literacy and shared decision making in HNC",
    "Photobiomodulation for radiation-induced mucositis",
    "Return to work after laryngeal cancer treatment",
    "Psychosocial interventions for HNC patients and partners",
    "Validated instruments for communication assessment in HNC",
    "Cost-effectiveness of early palliative care in HNC",
    "Microbiome changes during radiation therapy for HNC",
    "Trismus prevention in oral cancer",
    "AR for patient education before laryngectomy",
    "Pain management in head and neck oncology",
    "Second primary after HNC treatment",
    "Exercise for radiation-induced fibrosis",
    "Voice after transoral laser microsurgery",
    "Culturally adapted tools for indigenous HNC patients",
    "Wound complications after salvage laryngectomy",
    "Lymphedema after head and neck cancer treatment",
    "VHI cutoff in Spanish-speaking populations",
    "Rehabilitation timing after laryngectomy",
    "Social media support for HNC caregivers",
    "Depression screening in HNC clinics",
    "Immunonutrition before head and neck surgery",
    "Alaryngeal speech: patient preferences survey",
    "Automated speech assessment for clinical practice",
    "Radiomics for HNC treatment response prediction",
    "Shared care between primary care and oncology",
    "Dysgeusia impact on QoL in HNC",
    "Opioid prescribing after head and neck surgery",
    "Artificial saliva for xerostomia",
    "Peer support for laryngectomy patients",
    "Music therapy for mood in HNC patients",
    "fMRI of speech after laryngectomy",
    "Workforce capacity for SLP in Latin America",
    "NLP of patient-reported outcomes in HNC",
    "Prehabilitation before head and neck surgery",
    "Financial toxicity in HNC",
    "VR exposure for communication anxiety",
    "HPV detection in oropharyngeal cancer",
    "Acupuncture for radiation-induced xerostomia",
    "Decision aids for laryngeal cancer treatment",
    "Cochlear implant in irradiated temporal bone",
    "Oral health during head and neck RT",
    "Family as communication partner after laryngectomy",
    "Biofeedback for voice after partial laryngectomy",
    "Chemoprevention in oral premalignant lesions",
    "Hearing loss after platinum chemo in HNC",
    "Neural adaptation to electrolarynx",
    "Connected speech in alaryngeal speakers",
    "Ultrasound for laryngeal cancer detection",
    "Gender-affirming voice care in HNC",
    "HPV testing in community oral screening",
    "Smoking cessation in newly diagnosed HNC",
    "Sentiment analysis of online HNC forums",
    "Pectoralis flap in salvage settings",
    "Cortical reorganization after laryngectomy",
    "Wearable sensors for dysphagia rehab",
    "Genetics of radiation-induced dysphagia",
    "Psychological first aid for oncology nurses",
    "Minimally invasive esophagectomy",
    "Communication partner training for families",
    "Outcome after free flap reconstruction in HNC",
    "Non-invasive brain stimulation for dysphagia",
    "Circadian rhythm during chemoradiotherapy",
    "Airway CFD after partial laryngectomy",
    "Handgrip as predictor of treatment tolerance",
    "Ultrasound botox for post-laryngectomy spasms",
    "Patient navigation for Hispanic HNC patients",
    "Gastric tube dependence prediction in HNC",
    "Oral hygiene during radiotherapy",
    "De-intensification in HPV OPSCC",
    "Mucoadhesive films for mucositis",
    "Social cognition after brain radiation",
    "Pharmacogenomics of cisplatin ototoxicity",
    "Adaptive RT for parotid sparing",
    "Pharyngeal motor neuron tracing",
    "Smart inhaler after laryngectomy",
    "Artificial pancreas for steroid hyperglycemia",
    "OCT for oral lesion margin",
    "NIRS for flap monitoring",
    "Sentinel node biopsy in oral cancer",
    "Voice dosimetry after HNC treatment",
    "ICU without tracheostomy in HNC",
    "Biomarkers for HNC recurrence",
    "End-of-life communication in HNC",
    "EORTC QLQ-HN43 Chilean validation",
    "Community palliative care for rural HNC in Chile",
]
for t in diverse_topics:
    papers.append({"doi": None, "pmid": None, "title": t})

# ---------------------------------------------------------------------------
random.shuffle(papers)

# Warmup
_dummy_u, _dummy_l = deduplicate(papers)
del _dummy_u, _dummy_l

# Timed runs
times: list[float] = []
unique: list[dict] = []
log: list[dict] = []

for _ in range(N_RUNS):
    start = time.perf_counter_ns()
    unique, log = deduplicate(papers)
    elapsed_ns = time.perf_counter_ns() - start
    times.append(elapsed_ns / 1000)  # microseconds

times.sort()
median = times[len(times) // 2]

# Verify: 600 + 50 + 50 + 100 distinct = 800 unique, 100 + 50 + 50 = 200 duplicates
expected_unique = 600 + 50 + 50 + len(diverse_topics)
expected_dups = 100 + 50 + 50
actual = len(unique)
if actual != expected_unique:
    msg = f"ERROR: Expected {expected_unique} unique, got {actual}"
    print(msg, file=sys.stderr)
    sys.exit(1)
if len(log) != expected_dups:
    msg = f"ERROR: Expected {expected_dups} duplicates, got {len(log)}"
    print(msg, file=sys.stderr)
    sys.exit(1)

print(f"METRIC dedup_us={int(median)}")
print(f"METRIC throughput_papers_s={int(1000 / (median / 1_000_000))}")
